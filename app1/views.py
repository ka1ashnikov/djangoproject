from django.shortcuts import render
from django.shortcuts import redirect


def redirect_to_main(request):
    return show_1st(request)
dfsd


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
    request_data = request.POST.get('link')
    print(request_data)
    data = {
        'pg': 'Request',
        'request_data': request_data,
    }
    return render(request, 'redirect_page.html', context=data)

