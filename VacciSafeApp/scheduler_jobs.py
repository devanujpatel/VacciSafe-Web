import smtplib
import datetime
import json
from email.message import EmailMessage
from .models import VaccineRecords, Recipients, Vaccines


def reminder_emails():
    print("running")
    due_vaccine_records = VaccineRecords.objects.filter(
        reminder_date__lte=datetime.datetime.now(), vac_taken_date=None)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("vaccisafe.reminders@gmail.com", "zhrvsdpwswtvvrtx")

    all_users = {}
    for dvr in due_vaccine_records:
        all_users[dvr.recipient_pk.user_fk] = {"recipients":[]}

    for dvr in due_vaccine_records:
        for key in all_users:
            if dvr.recipient_pk.user_fk == key and dvr.recipient_pk not in all_users[key]["recipients"]:
                all_users[key]["recipients"].append(dvr.recipient_pk)
                all_users[key][dvr.recipient_pk] = []

    
    for dvr in due_vaccine_records:
        for key in all_users:
            for rec in all_users[key]["recipients"]:
                if dvr.recipient_pk == rec:
                    all_users[key][rec].append(dvr)

    print(all_users)

    for user in all_users.keys():
        for rec in all_users[user]["recipients"]:
            try:
                msg = EmailMessage()
                msg['Subject'] = 'VacciSafe Reminder'
                msg['From'] = "vaccisafe.reminders@gmail.com"
                print(user.email)
                msg['To'] = user.email
                content = f"Dear {user.username}\nThe following vaccines are due for {rec.fname + ' ' + rec.lname}: \n"
                for dvr in all_users[user][rec]:                        
                    content += f"-> {dvr.vaccine_fk.name} ({dvr.reminder_date})\n"
                msg.set_content(content)
                server.send_message(msg)
            except Exception as e:
                print(e)
    print("done")
    server.quit()
