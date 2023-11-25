from celery import shared_task
import time


@shared_task
def send_email_task():
    for i in range(10):
        time.sleep(5)
        print(f'sending email to user number {i}')
        