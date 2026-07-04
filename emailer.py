from pathlib import Path
from email.message import EmailMessage
import mimetypes
import smtplib


class Emailer:

    def send(
        self,
        smtp_server,
        smtp_port,
        username,
        password,
        recipient,
        subject,
        body,
        attachment=None,
    ):

        msg = EmailMessage()

        msg["From"] = username
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.set_content(body)

        if attachment is not None:

            attachment = Path(attachment)

            ctype, encoding = mimetypes.guess_type(attachment)

            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            with open(attachment, "rb") as f:

                msg.add_attachment(
                    f.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=attachment.name,
                )

        with smtplib.SMTP_SSL(
            smtp_server,
            smtp_port,
        ) as smtp:

            smtp.login(
                username,
                password,
            )

            smtp.send_message(msg)

        print("Email sent successfully.")