from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.index,
        name='index'
    ),
    url(
        r'^dashboard/$',
        views.dashboard,
        name='dashboard'
    ),
    url(
        r'^shorten/$',
        views.shorten_link,
        name='shorten-link'
    ),
    url(
        r'^edit/(?P<key>[(A-Za-z0-9)-]++)/$',
        views.edit_link,
        name='edit-link'
    ),
    url(
        r'^(?P<key>[(A-Za-z0-9)-]+)/$',
        views.redirect_to_link,
        name='redirect-to-link'
    ),
]
