from django.shortcuts import render, redirect

from .models import *


def index(request):
    query = request.GET.get("query")
    reactors = Reactor.objects.filter(name__icontains=query).filter(status=1) if query else Reactor.objects.filter(status=1)

    context = {
        "search_query": query if query else "",
        "reactors": reactors
    }

    return render(request, "home_page.html", context)


def reactor_details(request, reactor_id):
    context = {
        "reactor": Reactor.objects.get(id=reactor_id)
    }

    return render(request, "reactor_page.html", context)


def reactor_delete(request, reactor_id):
    reactor = Reactor.objects.get(id=reactor_id)
    reactor.delete()

    return redirect("/")
