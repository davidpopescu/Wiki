from email import message
from genericpath import exists
from logging import PlaceHolder
from re import I
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.contrib import messages

from . import util
from markdown2 import Markdown

import encyclopedia

class NewPageForm(forms.Form):
    title = forms.CharField( label = "Title", min_length = 3, max_length = 20)
    content = forms.CharField(widget = forms.Textarea(attrs={"placeholder" : "Enter the content that you want to introduce on the page\n Add # for title"}), label = "Content")
    def save(self):
        title = self.cleaned_data.get("title")
        content = self.cleaned_data.get("content")
        util.save_entry(title, content)

class editForm(forms.Form):
    content = forms.CharField(widget = forms.Textarea, label = "Content")
    def save(self):
        title = self.cleaned_data.get("title")
        content = self.cleaned_data.get("content")
        util.save_entry(title, content)

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

def search(request, entry_Title = None):
    querry = request.GET.get("q")
    counter = 0
    entries = [ entries.lower() for entries in util.list_entries()]
    if querry.lower() in entries:
        return HttpResponseRedirect(f"/wiki/{querry}")
    else:
        for entry in entries:
            if querry.lower() in entry:
                counter += 1
                return render(request, "encyclopedia/search.html", {
                    "similar_Entry": entry,
                })
            
        if counter == 0:
            return render(request, "encyclopedia/error404.html")

def create_Page(request):
    counter = 0
    entries = [ entries.lower() for entries in util.list_entries()]
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            for characters in content:
                if characters == "#":
                    counter += 1
            if counter == 0:
                messages.error(request, "You need to add # for title")
                return render(request, "encyclopedia/create.html", {
                    "form": NewPageForm()
                })
            if title.lower() in entries:
                messages.error(request, f"{title} already exists. Please create a new page.")
                return render(request, "encyclopedia/create.html", {
                    "form": NewPageForm()
                })
                
            else:
                form.save()
                return HttpResponseRedirect(f"/wiki/{title}")
        else:
            messages.error(request,"Invalid Form")
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
                "form": NewPageForm()
    })


def edit_Page(request,entry):
    entries = [ entries.lower() for entries in util.list_entries()]
    if entry.lower() not in entries:
        return render(request, "encyclopedia/error404.html")
    if request.method == "GET":
        content = util.get_entry(entry)
        form = editForm(initial={'content': content})
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "content": content,
            "title": entry
        })
    if request.method == "POST":
        form = editForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            return HttpResponseRedirect(f"/wiki/{entry}")
        return render(request, "encyclopedia/edit.html", {
            "form": editForm()
        })

def random_Page(request):
    entries = util.list_entries()
    import random
    random_entry = random.choice(entries)
    return HttpResponseRedirect(f"/wiki/{random_entry}")