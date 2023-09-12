from django.shortcuts import render
from django.shortcuts import redirect
from app1.models import links_db
from datetime import datetime
import validators


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
                print(datetime.now(),)
                links_db(link=user_link, date=datetime.now(), information=user_information).save()
                print('Данные занесены в БД.')
            except:
                print('Данные не занесены в БД.')

            return render(request, 'redirect.html', context=data)
    data = {
        'pg': 'Request',
    }
    return render(request, 'redirect_page.html', context=data)

# TODO: Сделать систему вывода всех строк из бд
# def console(request):