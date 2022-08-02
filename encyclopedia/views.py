from genericpath import exists
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from . import util
from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_Entry(request ,entry):
    entry_html = util.get_entry(entry)
    if entry_html and request.method == "GET":
        markdowner = Markdown()
        entry_html = markdowner.convert(util.get_entry(entry))
        return render(request, "encyclopedia/title.html", {
            "entry": entry_html,
            "title" : entry
        })
    else:
        return render(request, "encyclopedia/error404.html")

def search(request):
    if request.method == "GET":
        query = request.GET.get("query")
        entries = util.search(query)
        return render(request, "encyclopedia/search.html", {
            "entries": entries,
            "query": query
        })
    else:
        return render(request, "encyclopedia/error404.html")