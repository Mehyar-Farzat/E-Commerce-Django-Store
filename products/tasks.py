from celery import shared_task
import time


@shared_task                  # this decorator is used to make this function a celery task
def send_email_task():        # this is the task that will be executed by celery
    for i in range(10):       # this loop is just to simulate a long running task
        time.sleep(5)         # sleep for 5 seconds
        print(f'sending email to user number {i}')  # print a message to the console to show the progress of the task execution
        