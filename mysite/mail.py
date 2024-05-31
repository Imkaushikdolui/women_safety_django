from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_email(name, dest, link, user):
    subject = "EMERGENCY"
    from_email = settings.EMAIL_HOST_USER
    to_email = dest

    # Render the HTML template with context
    html_content = render_to_string("mysite/email.html", {"name": name, "link": link, "user":user})
    text_content = strip_tags(html_content)  # Strip the HTML tags for the plain text alternative

    # Create the email message
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")

    # Send the email
    msg.send()
