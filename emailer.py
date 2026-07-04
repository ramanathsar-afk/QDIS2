import smtplib

from email.message import EmailMessage


class Emailer:

    def send(

        self,

        smtp_server,

        port,

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

        if attachment:

            with open(attachment, "rb") as f:

                msg.add_attachment(

                    f.read(),

                    maintype="application",

                    subtype="octet-stream",

                    filename=attachment.name,

                )

        with smtplib.SMTP_SSL(

            smtp_server,

            port,

        ) as smtp:

            smtp.login(

                username,

                password,

            )

            smtp.send_message(msg)