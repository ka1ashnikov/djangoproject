from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from .models import links_db, users, codes
from datetime import datetime
import validators
import smtplib
import random

gmail_login = 'ka1ashsrvc@gmail.com'
gmail_password = 'knlk gqsx nwxo qnkd'
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

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
    #Запись юзера в БД
    user_ip = get_ip(request)
    user_information = f'{request.user_agent.os.family} {request.user_agent.os.version_string}, {request.user_agent.browser.family} Ver. {request.user_agent.browser.version_string}'
    try:
        users(date=datetime.now(), information=user_information, ip_1=user_ip).save()
        print('Данные занесены в БД.')
    except:
        print('Данные не занесены в БД.')
    user = codes.objects.filter(ip=user_ip)
    if user.exists():
        for i in user:
            if i.ip == user_ip:
                if i.code == 'None':
                    gmail_code = random.randint(100001, 999999)
                    user.update(code=gmail_code)
                    server.ehlo()
                    server.login(gmail_login, gmail_password)
                    server.sendmail(gmail_login, i.gmail, f'Your auth code is: "{gmail_code}"')
                    user.update(code_sended=1)
                    return render(request, 'gmail_verif.html')
                else:
                    if i.code_sended == 1:
                        print('123')
                        return render(request, 'gmail_verif.html')
    else:
        if request.POST.get('clicked') == 'val':
            email = request.POST.get('user_mail')
            if email.count('@') == 1 \
                    and email[0] != '@' \
                    and email.count('.') > 0 \
                    and email.find('@') < email.find('.') \
                    and email.find('com') > email.find('.'):
                print(request.POST.get('user_mail'))
                codes(user_agent=user_information, ip=user_ip, code='None', gmail=email, code_sended=0).save()
                return gmail_subm(request)
            else:
                return render(request, 'gmail_subm.html')
        else:
            return render(request, 'gmail_subm.html')


