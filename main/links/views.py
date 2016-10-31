import uuid

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import LinkForm


def index(request):
    form = LinkForm()
    return render(request, 'links/index.html', {'form': form})


@require_http_methods(["POST"])
def shorten_url(request, *args, **kwargs):
    form = LinkForm(request.POST or None)

    if request.is_ajax():
        if form.is_valid():
            link = form.save(commit=False)

            if request.user.is_authenticated:
                link.user = request.user
            link.save()

            data = {
                'url': uuid.uuid4().__str__().replace('-', '')
            }
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse(errors, status=400)

    return render(request, 'links/index.html', {'form': form})
