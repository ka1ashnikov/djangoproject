from django.contrib import admin
from django.urls import path
from app1 import views as views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirect_to_main),
    path('1/', views.show_1st, name='first'),
    path('2/', views.show_2nd, name='second'),
    path('redirect/', views.redirect_link, name='redirect'),

]