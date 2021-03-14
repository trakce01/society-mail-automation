import imaplib, email
import os
import datetime
import base64
from zipfile import ZipFile
import traceback
import shutil

email_user = "<YOUR APARTMENT's EMAIL-ID>"
email_pass = "<YOUR APARTMENT's EMAIL-PASSWORD>"
imap_url = "<imap url of the respective  emailid>"


def read_email():
    file_found = False
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(email_user, email_pass)
        mail.select()

        data = mail.search(None, "ALL")
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        first_email_id = int(id_list[0])
        last_email_id = int(id_list[-1])

        print("Getting Attachments... \n")
        for i in range(last_email_id, first_email_id, -1):
            data = mail.fetch(str(i), "(RFC822)")
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1], "utf-8"))

                    for part in msg.walk():
                        if part.get_content_maintype() == "multipart":
                            continue
                        if part.get("Content-Disposition") is None:
                            continue
                        fileName = part.get_filename()
                        current_date = datetime.date.today()
                        focus_file_name = "pdf bills.zip"
                        if fileName == focus_file_name:
                            file_found = True
                            if bool(fileName):
                                path = f"<the path where you want to download the bill attachments>"
                                if os.path.isdir(path):
                                    pass
                                else:
                                    os.mkdir(path)

                                filePath = os.path.join(f"{path}/{fileName}")

                                if not os.path.isfile(filePath):
                                    fp = open(filePath, "wb")
                                    fp.write(part.get_payload(decode=True))
                                    fp.close()
                                with ZipFile(rf"{path}/{focus_file_name}", "r") as zip:
                                    print("Extracting Files... \n")
                                    zip.extractall(path)
                                    print("Done! \n")

                                print("Deleting zip file... \n")
                                os.remove(f"{path}/{focus_file_name}")
                                print("Done! \n")
                                break

            if file_found:
                break

        mail.close()
        mail.logout
    except Exception as e:
        traceback.print_exc()
        print(str(e))


def delete_og_folder():
    current_date = datetime.date.today()
    print("Deleting downloaded attachments... \n")
    path = f"<the path where you want to download the bill attachments>"
    shutil.rmtree(path)
    print("Done! \n")
