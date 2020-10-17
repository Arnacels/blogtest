from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_mail(new_post):
    emails = [user.email for user in new_post.blog.subscribers.all() if user.email is not None]
    link_on_post = f"http://127.0.0.1:8000/blog/{new_post.blog.owner.username}/{new_post.id}/"
    text_email = f"""<h1>Created new post from {new_post.blog.owner.username.is_title()}</h1>
<a href="{link_on_post}">{new_post.title.is_title()}</a>
"""
    msg = EmailMessage(text_email,
                       'from@example.com',
                       emails, )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
