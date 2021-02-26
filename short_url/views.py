from django.shortcuts import render, get_object_or_404, redirect

from .models import ShortUrl


def index(request):
    short_urls = ShortUrl.objects.all()
    context = {
        "short_urls": short_urls
    }
    return render(request, "short_url/index.html", context)


def show(request, short_id):
    short_url = get_object_or_404(ShortUrl, short_id=short_id)
    context = {
        "short_url": short_url,
        "full_short_url": short_url.full_url(),
    }
    return render(request, "short_url/show.html", context)

def new(request):
    if request.method == "GET":
        return render(request, "short_url/new.html")
    elif request.method == "POST":
        long_url = request.POST["long_url"]
        short_url = ShortUrl.get_short_for(long_url)
        short_url.save()
        return redirect(f"/short_url/{short_url.short_id}")

def new_with_short_specified(request):
    if request.method == "GET":
        context = {"error": bool(request.GET.get("error"))}
        return render(request, "short_url/new_with_short_specified.html", context)
    elif request.method == "POST":
        long_url = request.POST["long_url"]
        requested_short = request.POST["requested_short"]
        short_url = ShortUrl.get_short_for(long_url)

        try:
            ShortUrl.objects.get(short_id=requested_short)
        except ShortUrl.DoesNotExist:
            short_url = ShortUrl(long_url=long_url, short_id=requested_short)
            short_url.save()
            return redirect(f"/short_url/{short_url.short_id}")

        return redirect("/short_url/new_with_short_specified?error=true")


def use_url(request, short_id):
    short_url = get_object_or_404(ShortUrl, short_id=short_id)
    return redirect(short_url.long_url)
