from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util
import markdown2
import random

md = markdown2.Markdown()

class searchForm(forms.Form):
    entry = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia', 'class':'search', 'autocomplete':'off'}))

class createForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title...', 'class':'form-control', 'id':'title', 'style':'margin-bottom: 20px; margin-top:30px; width: 95%'}))
    description = forms.CharField(label="Markdown content:", widget=forms.Textarea(attrs={'class':'form-control', 'rows':'15', 'style':'width: 95%'}))

class editForm(forms.Form):
    description = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control', 'rows':'15', 'style':'width: 95%'}))



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": searchForm()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "heading": "Page Not Found.",
            "message": "The requested URL was not found on this server.",
            "form": searchForm()
        })
    else:
        converted = md.convert(entry)
        context = {
            "title": title,
            "entry": converted,
            "form": searchForm()
        }
        return render(request, "encyclopedia/entry.html", context)

def search(request):
    if request.method == "POST":
        form = searchForm(request.POST)
        if form.is_valid():
            entries = util.list_entries()
            entry = form.cleaned_data["entry"]
            found = util.get_entry(entry)
            if found is not None:
                converted = md.convert(found)
                context = {
                    "title": entry,
                    "entry": converted, 
                    "form": searchForm()
                }
                return render(request, "encyclopedia/entry.html", context)
            elif any(entry in s for s in entries):
                res = [i for i in entries if entry in i]
                return render(request, "encyclopedia/search.html", {
                    "entries": res,
                    "title": entry,
                    "form": searchForm()
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "title": entry,
                    "heading": "Page Not Found.",
                    "message": "The requested URL was not found on this server.",
                    "form": searchForm()
                })

def new_page(request):
    if request.method == "POST":
        create_form = createForm(request.POST)
        if create_form.is_valid():
            entries = util.list_entries()
            title = create_form.cleaned_data["title"]
            description = create_form.cleaned_data["description"]
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    "heading": "Error.",
                    "message": "The entry already exists.",
                    "form": searchForm()
                })
            else:
                util.save_entry(title, description)
                entry = util.get_entry(title)
                converted = md.convert(entry)
                context = {
                    "title": title,
                    "entry": converted,
                    "form": searchForm()
                }
                return render(request, "encyclopedia/entry.html", context)

    return render(request, "encyclopedia/create.html", {
        "create_form": createForm(),
        "form": searchForm()
    })

def edit(request, title):
    entry = util.get_entry(title)
    if request.method == "POST":
        edit_form = editForm(request.POST)
        if edit_form.is_valid():
            description = edit_form.cleaned_data["description"]
            util.save_entry(title,description)
            edited = util.get_entry(title)
            converted = md.convert(edited)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": converted,
                "form": searchForm()
            })
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": searchForm(),
            "init_entry": editForm(initial={'description': entry}),
            "title": title,
            "edit_form": editForm()
        })

def random_entry(request):
    entries = util.list_entries()
    rand_entry = random.choice(entries)
    return HttpResponseRedirect(reverse('entry', args=[rand_entry]))


 






    



