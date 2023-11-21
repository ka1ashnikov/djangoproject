from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from .models import links_db, users, codes, gmail_tokens
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime
import validators
import smtplib, ssl
import random
import sys
import secrets

sys.setrecursionlimit(999999)

gmail_login = 'ka1ashsrvc@gmail.com'
gmail_password = 'knlk gqsx nwxo qnkd'
email_from = 'sender_email@gmail.com'
email_to = 'receiver_email@gmail.com'
server = smtplib.SMTP('smtp.gmail.com', 587)



def redirect_to_main(request):
    return show_1st(request)


def show_1st(request):

    data = {
        'pg': 1,
        'change_pg': 'NEXT PAGE',
    }
    if data['pg'] == 1:
        data['switch_pg'] = data['pg'] + 1
    return render(request, 'leaf.html', context=data)


def show_2nd(request):
    data = {
        'pg': 2,
        'change_pg': 'GO BACK',
    }
    if data['pg'] != 1:
        data['switch_pg'] = data['pg'] - 1
    return render(request, 'leaf.html', context=data)


def redirect_link(request):
    if request.method == 'POST':
        user_link = request.POST.get('link')
        user_information = f'{request.user_agent.os.family} {request.user_agent.os.version_string}, {request.user_agent.browser.family} Ver. {request.user_agent.browser.version_string}'
        if validators.url(f'https://{user_link}') == 1:
            data = {
                'link': user_link,
            }
            try:
                print(datetime.now())
                links_db(link=user_link, date=datetime.now(), information=user_information).save()
                print('Данные занесены в БД.')
            except:
                print('Данные не занесены в БД.')

            return render(request, 'redirect.html', context=data)
    data = {
        'pg': 'Request',
    }
    return render(request, 'redirect_page.html', context=data)


def console(request):
    all_rows = links_db.objects.all()
    data = {
        'all_rows': all_rows,
    }
    return render(request, 'console.html', context=data)


def get_ip(request):
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip:
        ip = user_ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip.format(ip)


def gmail_subm(request):
    user_ip = get_ip(request)
    user_information = f'{request.user_agent.os.family} {request.user_agent.os.version_string}, {request.user_agent.browser.family} Ver. {request.user_agent.browser.version_string}'
    try:
        users(date=datetime.now(), information=user_information, ip_1=user_ip).save()
        print('Данные занесены в БД.')
    except:
        print('Данные не занесены в БД.')

    user = codes.objects.filter(ip=user_ip)
    if user.exists():
        # Take user from db
        for i in user:
            # Indificate user by ip
            if i.ip == user_ip:
                # Is code sended or not
                if i.code == 'None':
                    gmail_code = random.randint(100001, 999999)
                    user.update(code=gmail_code)
                    server.ehlo()
                    server.login(gmail_login, gmail_password)
                    server.sendmail(gmail_login, i.gmail, f'"{gmail_code}"')
                    user.update(code_sended=1)
                    return render(request, 'gmail_verif.html')
                else:
                    if i.gmail_verified == 0:
                        if i.code_sended == 1:
                            print('123')
                            if request.POST.get('code') == i.code:
                                user.update(gmail_verified=1)
                                return render(request, 'gmail_success.html')
                            else:
                                return render(request, 'gmail_verif.html')
                    else:
                        if request.POST.get('re-verify') == 'clicked':
                            user.update(gmail_verified=0, code='None')
                            return gmail_subm(request)
                        return render(request, 'gmail_success.html')
    else:
        if request.POST.get('clicked') == 'val':
            email = request.POST.get('user_mail')
            user_email = codes.objects.filter(gmail=email)
            if user_email.exists():
                if request.POST.get('gmail_used') == 'clicked':
                    return render(request, 'gmail_subm.html')
                return render(request, 'gmail_is_used.html')
            else:
                if email.count('@') == 1 \
                        and email[0] != '@' \
                        and email.count('.') > 0 \
                        and email.find('@') < email.find('.') \
                        and email.find('com') > email.find('.'):
                    print(request.POST.get('user_mail'))
                    codes(user_agent=user_information, ip=user_ip, code='None', gmail=email, code_sended=0, gmail_verified=0).save()
                    return gmail_subm(request)
                else:
                    return render(request, 'gmail_subm.html')

        else:
            return render(request, 'gmail_subm.html')


def html_def(token):

    html_str = f'''
    <html>
        <body>
            <h1>Press the button to verify your email!</h1>
            <form action="http://192.168.45.169:8000/link_gmail/{token}">
                <input type="submit" value="Verify" />
            </form>
        </body>
    </html>
    '''
    return html_str


def link_gmail_auth(request):

    user_ip = get_ip(request)
    user = gmail_tokens.objects.filter(ip=user_ip)

    # If exists
    if user.exists():
        # Take user from db
        for i in user:
            # Indificate user by ip and send mail
            if i.ip == user_ip:
                if i.gmail_verified == 0 and i.token == 'None':
                    token = secrets.token_urlsafe(nbytes=15)
                    user.update(token=token)
                    server.starttls()
                    server.login(gmail_login, gmail_password)
                    email_message = MIMEMultipart()
                    email_message['From'] = gmail_login
                    email_message['To'] = i.email
                    email_message['Subject'] = f'Verify email.'
                    html = html_def(token)
                    email_message.attach(MIMEText(html, "html"))
                    email_string = email_message.as_string()
                    server.sendmail(gmail_login, i.email, email_string)
                    server.close()
                    user.update(link_sended=1)
                    data = {
                        'email': i.email,
                    }
                    return render(request, 'gmail_link_sended.html', context=data)
                else:
                    data = {
                        'email': i.email,
                    }
                    if i.gmail_verified == 1:
                        return render(request, 'gmail_link_verified.html', context=data)
                    else:
                        return HttpResponse('Please, verify your email!')

    else:
        # Submit clicked
        if request.POST.get('clicked') == 'val':
            # Get email from form
            email = request.POST.get('user_mail')
            user_email = gmail_tokens.objects.filter(email=email)
            # Is email in db:
            # Yes
            if user_email.exists():
                return render(request, 'gmail_is_used.html')
            # No
            else:
                # Check email valid:
                # Yes
                if email.count('@') == 1 \
                        and email[0] != '@' \
                        and email.count('.') > 0 \
                        and email.find('@') < email.find('.') \
                        and email.find('com') > email.find('.'):
                    print(request.POST.get('user_mail'))
                    gmail_tokens(ip=user_ip, email=email, token='None', link_sended=0, gmail_verified=0).save()
                    return link_gmail_auth(request)
                # No
                else:
                    return render(request, 'gmail_subm.html')
        # Submit not clicked
        else:
            return render(request, 'gmail_subm.html')


def gmail_activate(request, token):
    user_ip = get_ip(request)
    user = gmail_tokens.objects.filter(ip=user_ip)

    # As user from his ip exists
    if user.exists():
        for i in user:
            if token == i.token:
                data = {
                    'email': i.email,
                }
                user.update(gmail_verified=1)
                user.update(token='None')
                return render(request, 'gmail_link_verified.html', context=data)

            else:
                return render(request, '404.html')
    else:
        return HttpResponse('Change ip/You need to verify email!')
