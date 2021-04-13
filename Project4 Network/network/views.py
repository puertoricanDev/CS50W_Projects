from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Posts, Follow 
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def index(request):
    
    
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return load_post(request,"index")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))
        
@login_required
def load_post(request, fllw):

    if request.user.is_authenticated:
        
        if fllw == "following":
            flw=Follow.objects.filter(fuser=request.user)
            posts_view = Posts.objects.filter(postuser__in = flw[0].following.all())
            btnstyle = "text-align: center; display: none;"
        else:
            posts_view = Posts.objects.all()
            btnstyle = "text-align: center; display: block;"
        posts_view = posts_view.order_by("-timestamp").all()
        paginator = Paginator(posts_view, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
                
        return render(request, "network/index.html", {'page_obj': page_obj,
                "btnstyle":btnstyle})
    else:
        return HttpResponseRedirect(reverse("login"))



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

@login_required
@csrf_exempt
def New_Post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    body = data.get("body","")
    if body == [""]:
        return JsonResponse({
            "error": "The Post should contain something."
        }, status=400)
    post = Posts(
        postuser = request.user,
        body = body
    )
    post.save()
    return JsonResponse({"message": "Post created successfully."}, status=201)



@login_required
@csrf_exempt
def profile(request, profuser):
    fuserid = User.objects.get(username = profuser)
    following = Follow.objects.get(fuser=fuserid)
    posts_view = Posts.objects.filter(postuser=fuserid)
    posts_view = posts_view.order_by("-timestamp").all()
    paginator = Paginator(posts_view, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user in following.followed.all():
        btnclass = "btn btn-outline-danger"
        btnhtml = "Unfollow"
    else:
        btnclass = "btn btn-outline-success"
        btnhtml= "Follow"
    
    return render(request, "network/profile.html",{
        "profuser": profuser,
        "following": len(following.following.all()),
        "followers": len(following.followed.all()),
        "profuserid": fuserid.id,
        "btnclass": btnclass,
        "btnhtml": btnhtml,
        "page_obj": page_obj
    })

@login_required
@csrf_exempt
def Ifollow(request, uid):
    try:
        fwing = Follow.objects.get(fuser = request.user)
        uname = User.objects.get(id = uid)
        if uname in fwing.following.all():
            fl=Follow.objects.filter(fuser=uid, followed=request.user.id)
            fl[0].followed.remove(request.user)
            fl.update()
            fl=Follow.objects.filter(fuser=request.user.id, following=uid )
            fl[0].following.remove(uid)
            fl.update()
            return JsonResponse({"message": "Unfollow succesfully"}, status=201)
        else:
            fl=Follow.objects.filter(fuser=request.user.id)
            fl[0].following.add(uid)
            fl.update()
            fl=Follow.objects.filter(fuser=uid)
            fl[0].followed.add(request.user.id)
            fl.update()
            return JsonResponse({"message": "follow succesfully"}, status=201)  
    except:
        return JsonResponse({
                "error": "The Post should contain something."
            }, status=400)
 


@login_required
@csrf_exempt
def Ilike(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pid = int(data.get("id"))
        post = Posts.objects.get(id = pid)
        if request.user not in post.likes.all():
            post.likes.add(request.user)
            
        else:
            post.likes.remove(request.user)

        post.save()
        return HttpResponse(status=204)
    else:
       return JsonResponse({
            "error": "POST request required."
        }, status=400) 

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            fuser = Follow(fuser=username)
            fuser.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
@csrf_exempt
def saveedit(request,pid):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    body = data.get("body","")
    if body == [""]:
        return JsonResponse({
            "error": "The Post should contain something."
        }, status=400)
    post = Posts.objects.get(id=pid)
    post.body = body
    post.save()
    return JsonResponse({"message": "Post edited successfully."}, status=201)
