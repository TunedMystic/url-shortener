from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^shorten-url/$', views.shorten_url, name='shorten-url'),
]
