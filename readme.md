# VacciSafe
VacciSafe is a website which helps in planning and keeping track of Vaccine Schedules with timely reminders. Right from Birth to 16 years of age, one is supposed to take 43 vaccines if male or 45 if female. Some are to be taken just after birth, some after 3 months, some after 6 months, some after 1 year and 6 months and so on. VacciSafe helps in maintaining such vaccine schedules. 
Each signed in user can create multiple 'Vaccine Recipients'. During the creation of a new Recipient, VacciSafe calculates the Due Date of a particular Vaccine by adding the required number of days, months and years to the recipient's date of birth. A user can toggle the status of a vaccine to 'Taken' or 'Not Taken' anytime to match their particular vaccination history given that the vaccine is already past its due date (meaning you can't mark a vaccine due next year as 'Taken'). VacciSafe sends reminder emails as the due date of a vaccine approaches or is already past the due date and yet not taken.
##  Models
### Vaccines
This table contains all the data about Vaccines. All the data has been taken from Government of India's Health Ministry website (https://www.nhp.gov.in/universal-immunisation-programme_pg). 
The columns are a follows:
<li>vaccine name
<br>To know when that particular vaccine is generally given at:
<li>given_at_age_from_year
<li>given_at_age_from_month
<li>given_at_age_from_weeks
<br>To show details when clicked on vaccine name.
<li>details
<li>gender (Since girls have to take two additional vaccines. Can be either 'ALL' or 'F')<br>
Even if in the future a new vaccine is launched then one can simply add that particular vaccine in this table and all new recipients created from then on will have that particular vaccine in the schedule. For old recipients, the VaccineRecords table can be easily manipulated to reflect the approriate changes.

### Users
I have implemented Google Log in as the mechanism for user authentication. I used Django's Social Authentication to make things easier since it automatically handles the data entry in the Users table. I primarily use this table to get the email address and full name of the signed in user. Also I already have created an Android Version of VacciSafe which currently doesn't implement Google Login or any sort of authentication since the main idea was to make it work without internet as well. So if in future I plan to use Google Authentication then both the Website and the App can operate from a common database with changes being reflected in both.
### Recipients
Each user can create as many Vaccine Recipients as they want. This table stores information about each Recipient. Columns are as follows:
    <li>user_fk (to distinguish which top-level-user that recipient belongs to)
    <li>fname
    <li>lname
    <li>Date of Birth
    <li>Gender<br>
According to the Date of Birth provided VacciSafe generates the due date of each vaccines. More on this in the 'Recipient Creation Process'.
Gender is also a required field since girls are supposed to take two additional vaccines.

### Vaccine Records
This table stores all the data about the vaccine schedule of recipients. It gets populated when a new recipient is created. 
This table contains the following columns:
<li>recipient_fk (to distinguish vaccine records from different recipients)
<li>vaccine_fk (to know which vaccine does that particular record refers to)
<li>reminder_date (to store the due date)
<li>vac_taken_date (stores the date at which the vaccine was taken; null if not yet taken)

## Recipient Creation Process
Each user can have multiple recipients. When a user is logged in then they get the option for creating a new recipient. The form asks for recipient's first and last name along with date of birth and gender.

If the gender is 'Female' then all the  vaccines from the Vaccines table are selected. If not, then all vaccines with 'ALL' as gender are selected (thereby leaving the two vaccines for girls). The three 'given_at_age_from' columns of the vaccine are added to the Date of Birth of the recipient. If the due date so calculated is before today, then it is assumed that the vaccine is already taken and reminder date as well as vac_taken_date is set to today's date. If the calculated due date is in the future then the reminder date is set to the due date and vac_taken_date as null.

## views.py, routes and front-end
### index
If the user is already logged in then the recipients_page is renderd.
Else the Google Log in page is rendered. I have override Django's Social Auth Templates (as is evident from the templates folder) to make my GUI cleaner and presentable.
### new_recipient and add_recipient
The new_recipient routes simply renders the form for the creation of a new recipient. The form's onsubmit has been altered using javascript to ensure that all fields are properly filled. Also no duplicate recipient names can be used under the same 'top-level-user'. Javascript is then used to add the new recipient by calling POST on add_recipient route.
The vaccines_page is then rendered which displays the newly created Vaccine Records in a tabular form.
### vaccines_page and get_vaccines
The vaccines_page route renders the HTML. But the Dnango's template aren't enough to dynamically create and set onclick listeners on the Vaccine Name (to show details when clicked on the table cell) and on the status buttons (set 'Taken' or not 'Taken' a vaccine)
### toggle_vaccine_status
Called when a Vaccine status is to be changed (i.e. changed to  'Taken' or 'Not Taken'). If vac_taken_date is null then it is set to today's date. If it is not null then it is set to null so as to indicate that the vaccine is not taken. 
The GUI also changes accordingly. If vaccine is already taken (or marked taken) then background is green and text is Taken. If vaccine is not taken (as indicated by the vac_taken_date) then background is orangish red with text on button as the reminder date.
## Reminder System
In production environment the code for checking due dates would typically run everday at say 9AM, but for the sake of testing and demonstration, I had scheduled it to run every ten seconds. To run the server without sending the reminder emails every 10 seconds, I would just comment out the import statement of execute.py file from the urls.py file.

When the code runs (at 9AM everyday or after every 10 seconds when not commented out), it first selects all the vaccine records with a null vac_taken_date. Then it gathers a list of all the top-level-users from those vaccine records. Now it associates every recipient in the query set to its respective top-level-user. Next every vaccine record is matched to a recipient.
This allows to send seperate emails (one for each recipient) to every top-level-user about their upcoming vaccines.
This has been made possible using the execute.py file which defines the job and its time-interval (eg: 10 seconds). The job_scheduler.py file has the code which sends the reminder emails using the smtp library.
## Other things to know
I have used Google Authentication and had to get a oauth client secret from Google Cloud Console's credentials tab. In the Authorized redirect URIs and Authorized JavaScript origins, I had first entered localhost. But now I could not run and test my website on other devices on the LAN. Google didn't allow to enter a private IP address either. So I made changes to the "host" file located at "C:\Windows\System32\drivers\etc\hosts" and configured my server's private IP (192.168.29.201) address to 'devpc.com'. So everytime I hit devpc.com on devices with the edited "host" file, it targets my server (i.e. 192.168.29.201). See https://www.liquidweb.com/kb/edit-host-file-windows-10/ for more information about the host file.
