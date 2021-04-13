from django.shortcuts import render
from django.utils import html
from . import util
from markdown2 import Markdown
from django.http import HttpResponse
from django import forms
import re
import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if util.get_entry(title) == None:
        content=None
    else:
        content=markdowner.convert(util.get_entry(title))
    return render(request, "wiki/index.html",{
        "content" : content,
        "title" : title
    })
def rdom(request):
    return title(request, random.choice(util.list_entries()))
    
def edit(request):
    content = util.get_entry(request.POST['titlepass'])
    return render(request, "wiki/edit.html",{
        "content" : content,
        "title" : request.POST['titlepass'],
        "disabled" : "readonly"
    })
def saveedit(request):
    if request.method == "POST":
        util.save_entry(request.POST['newtitle'], request.POST['newcontent'])
        return title(request, request.POST['newtitle'] )
    else:
        return title(request, None )

def addpage(request):
    if request.method == "POST":
        if util.get_entry(request.POST['newtitle']) == None:
            util.save_entry(request.POST['newtitle'], request.POST['newcontent'])
            return title(request, request.POST['newtitle'] )
        else:
            return title(request, None )
    else:
        return render(request, "wiki/addpage.html")

def search(request):
    title = request.POST['q']
    if request.method == "POST":

            if util.get_entry(title) == None:
                slist=util.list_entries()
                entries = [x for x in slist if re.match(title, x, re.IGNORECASE)]
                if not entries:
                    content = None
                    return render(request, "wiki/index.html",{
                        "content" : content,
                        "title" : title
                    })
                else:
                    return render(request, "encyclopedia/index.html", {
                    "entries": entries
                     })
            else:
                content=markdowner.convert(util.get_entry(title))
                return render(request, "wiki/index.html",{
                "content" : content,
                "title" : title
                })   
    else:
        return(title(request, None))
