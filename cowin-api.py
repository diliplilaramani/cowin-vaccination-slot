import requests
import json
import smtplib, ssl
# import schedule
import time
import datetime
from dateutil.relativedelta import relativedelta

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "xxxxxxx@gmail.com"
receiver_email = "xxxxxx"
password = "xxxxxxxx"
success_message = """\
Subject: Cowin Vaccination Slots Available

LOGIN: https://selfregistration.cowin.gov.in/

"""

failed_message = """\
Subject: Cowin Request FAILED

"""



def send_email(is_success):
    print('SENDING EMAIL....')
    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        if is_success:
            print('SENDING EMAIL......SUCCESS')
            server.sendmail(sender_email, receiver_email.split(','), success_message)
        else:
            print('SENDING EMAIL......FAILED')
            server.sendmail(sender_email, 'dilip.ajm@gmail.com', failed_message)
            import sys
            sys.exit("ERRORS.......")


def get_cowin_data():
    print('\n\n==== get_cowin_data: =======\n\n')
    date_formated = datetime.datetime.today().strftime("%d-%m-%Y")
    print(date_formated)
    session = requests.Session()
    session.headers.update({'User-Agent': 'Custom user agent'})
    response = session.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=507&date='+date_formated)

    print('\n\n==== response: {} =======\n\n'.format(response))

    if response.status_code == 200:
        json = response.json()
        centers = json['centers']
        print('First center for testing: ', centers[0])

        for i in range(len(centers)):
            center = centers[i]
            # print(center)
            sessions = center['sessions']
            for j in range(len(sessions)):
                session = sessions[j]
                # print(session)
                slot = session['available_capacity']
                # print(slot)
                if slot > 0:
                    send_email(1)
                    return
    else:
        send_email(0)

if __name__ == '__main__':

    while True:
        get_cowin_data()
        time.sleep(10)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)
    # while 1:
    #     schedule.run_pending()
    #     time.sleep(1)
