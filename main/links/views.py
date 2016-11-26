from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.db.models import F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template.loader import get_template
from django.utils import timezone
from django.utils.cache import patch_cache_control
from django.views.decorators.http import require_http_methods

from ipware.ip import get_ip

from .decorators import link_owner
from .forms import LinkForm, LinkEditForm
from .models import Link
from analytics.models import Referer


def index(request):
    site = Site.objects.get_current()
    form = LinkForm()
    return render(request, 'links/index.html', {'form': form, 'site': site})


@login_required
def dashboard(request):
    links = Link.objects.filter(user=request.user).order_by('-created_on')
    site = Site.objects.get_current()
    return render(
        request,
        'links/dashboard.html',
        {'links': links, 'site': site}
    )


@require_http_methods(['POST'])
def shorten_link(request):
    form = LinkForm(
        request.POST or None,
        user=request.user
    )

    if form.is_valid():
        link = form.save(commit=False)
        return JsonResponse({'url': link.key}, status=200)
    else:
        errors = form.errors
        return JsonResponse(errors, status=400)


@login_required
@link_owner
def edit_link(request, key):
    link = Link.objects.get(key=key)
    form = LinkEditForm(
        request.POST or None,
        user=request.user,
        instance=link,
    )

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard'))

    return render(request, 'links/edit_url.html', {'form': form})


@require_http_methods(['GET'])
def redirect_to_link(request, key):
    link = get_object_or_404(Link, key=key)
    ip_address = get_ip(request)

    # Get referer from request META object.
    referer_source = request.META.get('HTTP_REFERER', '')

    # If referer exists, normalize.
    if referer_source:
        referer_source = Referer.normalize_source(referer_source)

    # Get or create Referer object from kwargs.
    referer, created = Referer.objects.get_or_create(
        link=link,
        source=referer_source
    )

    # Update last visited for this referer.
    referer.last_visited = timezone.now()

    # Increment clicks for this referer.
    referer.total_clicks = F('total_clicks') + 1

    # Save Referer object.
    referer.save()

    # Update Link total clicks.
    link.total_clicks = F('total_clicks') + 1
    link.save()

    # Update Unique IP addresses.
    link.add_unique_ip(ip_address)

    # Prepare template response.
    template = get_template('links/redirect.html')
    context = {
        'site': Site.objects.get_current(),
        'link': link
    }

    response = HttpResponse(template.render(context, request), status=301)
    response['Location'] = link.destination

    # Set cache control to be private and to be contacted back after 60 seconds
    patch_cache_control(
        response,
        private=settings.CC_PRIVATE,
        max_age=settings.CC_MAX_AGE
    )

    return response
