"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('users.urls')),
    url(r'', include('links.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]


# root_urlconf = __import__(settings.ROOT_URLCONF)
# patterns = root_urlconf.urls.urlpatterns


def get_urls(raw_urls, nice_urls=[], urlbase=''):
    from operator import itemgetter
    for entry in raw_urls:
        fullurl = (urlbase + entry.regex.pattern).replace('^', '')
        if entry.callback:
            nice_urls.append({"pattern": fullurl})
        else:
            get_urls(entry.url_patterns, nice_urls, fullurl)
    nice_urls = sorted(nice_urls, key=itemgetter('pattern'))
    return nice_urls

# Parse urlconfigs.
blacklist = get_urls(urlpatterns)
blacklist = [d.get('pattern') for d in blacklist]
blacklist = list(set([
    s.split('/')[0]
    for s in blacklist
    if not s.startswith(('$', '(', '_'))]
))
settings.blacklist = blacklist
