import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from string import Template
import datetime

email_user = "<YOUR APARTMENT's EMAIL-ID>"
email_pass = "<YOUR APARTMENT's EMAIL-PASSWORD>"
smtp_url = (
    "<imap url of the respective  emailid>"  # you can get this by simply googling it
)

out_mail = smtplib.SMTP(smtp_url, port=587)
out_mail.starttls()
out_mail.login(email_user, email_pass)
current_date = datetime.date.today()
path = f"<the path where you want to download the bill attachments>"

# GET CONTACTS FROM TXT


def get_contacts(filename):
    names = []
    rooms = []
    emails = []

    with open(filename, mode="r", encoding="utf-8") as contacts_file:
        for contact in contacts_file:
            names.append(contact.split()[0])
            rooms.append(contact.split()[1])
            emails.append(contact.split()[2])

    return names, rooms, emails


# EMAIL TEMPLATE


def read_template(filename):
    with open(filename, "r", encoding="utf-8") as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_email():
    print("Sending Mails to Contacts... \n")
    # sending emails to respective owners
    names, rooms, emails = get_contacts("contacts.txt")
    message_template = read_template("message.txt")

    for name, room, email in zip(names, rooms, emails):
        msg = MIMEMultipart()

        message = message_template.substitute(PERSON_NAME=name.title(), ROOM=room)

        msg["From"] = email_user
        msg["To"] = email
        msg["Subject"] = f"Maintainance Bill for {room}"

        msg.attach(MIMEText(message, "plain"))

        attach_file_name = f"{path}/{room}.pdf"
        attach_file = open(attach_file_name, "rb")
        payload = MIMEBase("application", "octet-stream")
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)
        payload.add_header("Content-Disposition", f"attachment; filename= {room}.pdf")
        msg.attach(payload)

        out_mail.send_message(msg)
        del msg

    out_mail.quit()
    print("Mails Sent! \n")
