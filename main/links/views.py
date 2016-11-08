from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.db.models import F
from django.http import JsonResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_http_methods

from .forms import LinkForm, LinkEditForm
from .models import Link


def index(request):
    site = Site.objects.get_current()
    form = LinkForm()
    return render(request, 'links/index.html', {'form': form, 'site': site})


@require_http_methods(['POST'])
def shorten_url(request):
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


def redirect_url(request, key):
    link = get_object_or_404(Link, key=key)

    # Update Link total clicks.
    link.total_clicks = F('total_clicks') + 1
    link.save()

    return HttpResponsePermanentRedirect(link.destination)


@login_required
def dashboard(request):
    links = Link.objects.filter(user=request.user)
    return render(
        request,
        'links/dashboard.html',
        {'links': links}
    )

@login_required
def edit_url(request, key):
    link = Link.objects.get(key=key)
    form = LinkEditForm(request.POST or None, instance=link)

    if request.method == 'POST':
        #import pdb; pdb.set_trace();
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard'))

    return render(request, 'links/edit_url.html', {'form': form})
