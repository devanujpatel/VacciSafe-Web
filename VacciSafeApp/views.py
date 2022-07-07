from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
import datetime
from dateutil.relativedelta import relativedelta
import json
from django.shortcuts import render, redirect
from .models import VaccineRecords, Vaccines, Recipients
from social_django import models as oauth_models
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


def index(request):
    if request.user.is_authenticated:
        recipients = Recipients.objects.filter(
            user_fk=User.objects.get(id=request.user.id))
        return render(request, "recipients_page.html")
    else:
        return render(request, "./account/login.html")


def new_recipient(request):
    return render(request, "new_recipient.html")


def user_logout(request):
    logout(request)
    return redirect('/')


@csrf_exempt
@login_required
def add_recipient(request):
    post_data = json.loads(request.body.decode("utf-8"))
    d = int(post_data["dob"][9:11])
    m = int(post_data["dob"][5:7])
    y = int(post_data["dob"][0:4])
    dob = datetime.date(y, m, d)
    rec = Recipients(user_fk=User.objects.get(id=request.user.id),
                     fname=post_data["fname"], lname=post_data["lname"], dob=dob, gender=post_data["gender"])
    try:
        rec.save()
    except IntegrityError:
        return HttpResponse(json.dumps({"response": "unique_first_last_combo_error"}), content_type="application/json")
    print(post_data["gender"])
    if post_data["gender"] == "Female":
        print("female")
        vaccines = Vaccines.objects.all().order_by("id")
    else:
        print("not female")
        vaccines = Vaccines.objects.filter(gender="ALL").order_by("id")
    for vaccine in vaccines:
        to_be_taken_at = dob + \
            datetime.timedelta(vaccine.given_at_age_from_weeks * 7)
        to_be_taken_at = to_be_taken_at + \
            relativedelta(months=vaccine.given_at_age_from_month)
        to_be_taken_at = to_be_taken_at + \
            relativedelta(years=vaccine.given_at_age_from_year)

        to_be_taken_at = datetime.datetime.combine(
            to_be_taken_at, datetime.datetime.min.time())

        if to_be_taken_at < datetime.datetime.now() or to_be_taken_at == datetime.datetime.now():
            # already taken
            vaccine_record = VaccineRecords(vaccine_fk=vaccine, recipient_pk=rec,
                                            reminder_date=to_be_taken_at, vac_taken_date=datetime.datetime.now())
        else:
            # future pending vaccine
            vaccine_record = VaccineRecords(
                vaccine_fk=vaccine, recipient_pk=rec, reminder_date=to_be_taken_at, vac_taken_date=None)

        vaccine_record.save()
    return HttpResponse(json.dumps({"rec_id": rec.id, "response": "success"}), content_type="application/json")


@login_required
def get_recipients(request):
    recipients = Recipients.objects.filter(
        user_fk=User.objects.get(id=request.user.id))
    recs = []
    for rec in recipients:
        recs.append({"id": rec.id, "name": str(
            rec.fname) + " " + str(rec.lname)})
    return HttpResponse(json.dumps(recs), content_type="application/json")


@login_required
def vaccines_page(request, rec_id):
    recipient = Recipients.objects.get(id=rec_id)
    return render(request, "vaccines_page.html", {
        "rec_id": rec_id,
        "fname": recipient.fname,
        "lname": recipient.lname,
        "dob": recipient.dob
    })


@login_required
def get_vaccines(request, rec_id):
    try:
        recipient_owner_user = Recipients.objects.get(id=rec_id).user_fk
        if request.user.id == recipient_owner_user.id:
            vaccines = VaccineRecords.objects.filter(
                recipient_pk=Recipients.objects.get(id=rec_id)).order_by("id")
        else:
            return HttpResponse(json.dumps({"response": "err_no_matching_query"}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"response": "err_no_matching_query"}), content_type="application/json")

    vaccines_list = []
    for vaccine in vaccines:
        taken_at_string = ""

        if vaccine.vaccine_fk.given_at_age_from_year != 0:
            taken_at_string += str(vaccine.vaccine_fk.given_at_age_from_year) + "Y "
        if vaccine.vaccine_fk.given_at_age_from_month != 0:
            taken_at_string += str(vaccine.vaccine_fk.given_at_age_from_month) + "M "
        if vaccine.vaccine_fk.given_at_age_from_weeks != 0:
            taken_at_string += str(vaccine.vaccine_fk.given_at_age_from_weeks) + "W "

        if not taken_at_string:
            taken_at_string = "Birth"

        btn_state = "enabled"
        if vaccine.vac_taken_date == None:
            reminder_date = datetime.datetime.combine(
                vaccine.reminder_date, datetime.datetime.min.time())
            if reminder_date > datetime.datetime.now():
                btn_state = "disabled"

        vaccines_list.append({"id": vaccine.id, "vaccine_id": vaccine.vaccine_fk.id, "vaccine_name": vaccine.vaccine_fk.name, "reminder_date": str(
            vaccine.reminder_date.strftime("%d-%m-%Y")), "vac_taken_date": str(vaccine.vac_taken_date), "taken_at": taken_at_string, "details": vaccine.vaccine_fk.details, "btn_state": btn_state})

    return HttpResponse(json.dumps(vaccines_list), content_type="application/json")


@ csrf_exempt
@ login_required
def toggle_vaccine_status(request):
    # vaccine record = vaccine fk, recipient fk, btn text
    post_data = json.loads(request.body.decode("utf-8"))
    vaccine_record = VaccineRecords.objects.get(vaccine_fk=Vaccines.objects.get(
        id=post_data['vaccine_fk']), recipient_pk=Recipients.objects.get(id=post_data['recipient_fk']))

    if post_data["vac_taken_date"] != "None":
        vaccine_record.vac_taken_date = None
        vaccine_record.save()

    else:
        vaccine_record.vac_taken_date = datetime.datetime.now()
        vaccine_record.save()

    return HttpResponse(json.dumps({"response": "success"}), content_type="application/json")

def delete_recipient(request, rec_id):
    recipient = Recipients.objects.get(id=rec_id)
    recipient.delete()
    return redirect("/")