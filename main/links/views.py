from django.contrib.sites.models import Site
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import LinkForm


def index(request):
    site = Site.objects.get_current()
    form = LinkForm()
    return render(request, 'links/index.html', {'form': form, 'site': site})


@require_http_methods(["POST"])
def shorten_url(request, *args, **kwargs):
    form = LinkForm(
        request.POST or None,
        user=request.user
    )

    if request.is_ajax():
        if form.is_valid():
            link = form.save(commit=False)

            data = {
                'url': link.key
            }
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse(errors, status=400)

    return render(request, 'links/index.html', {'form': form})
