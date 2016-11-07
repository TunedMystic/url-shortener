from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.index,
        name='index'
    ),
    url(
        r'^shorten-url/$',
        views.shorten_url,
        name='shorten-url'
    ),
    url(
        r'^dashboard/$',
        views.dashboard,
        name='dashboard'
    ),
    url(
        r'^(?P<key>[\w-]+)/$',
        views.redirect_url,
        name='redirect-url'
    ),
]
