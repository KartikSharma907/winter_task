from __future__ import unicode_literals


from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseForbidden
from .models import Profile , Post, Comment
from . import models
from .forms import SignUpForm, EditProfileForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .post_records import keep_record
from django.contrib.auth import update_session_auth_hash

import datetime


def home(request):
    return render(request, 'blog/home.html')


def signup(request):
     if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:login_page')
     else:
         form = SignUpForm()
     return render(request, 'blog/signup.html', {'form': form})

#Method of html forms

#def signup(request):
#
#     if request.method == 'GET':
#        return render(request, 'blog/signup.html')
#
#     elif request.method == 'POST':
#        first_name = request.POST['first_name']
#        last_name = request.POST['last_name']
#        username = request.POST['username']
#        email = request.POST['email']
#        password = request.POST['password']
#        password_again = request.POST['password_again']


#        if first_name.isalpha() and last_name.isalpha() and username.isalnum():
#            if password == password_again:
#                user = User(username = username, email = email, first_name = first_name, last_name = last_name)
#                user.set_password(password)
#                user.save()
#                profile = Profile(user=user)
#                profile.save()
#
#                return render(request, 'blog/login_page.html')
#
#            else:
#                messages.error(request, "Your passwords don't match!")
#                return redirect('blog:signup')
#
#        else:
#            messages.error(request, "Please fill all the fields!")
#            return redirect('blog:signup')



def login_page(request):
    if request.method == 'GET':
        return render(request, 'blog/login_page.html')

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)


        if user is not None:
            django_login(request, user)
            return redirect('blog:user_page',user.id)

        else:
            messages.error(request, "Entered Username/Password does not match.")
            return redirect('blog:login_page')


def logout_page(request):
    django_logout(request)
    return redirect('blog:home')


@login_required
def user_page(request,id):
    current_user = User.objects.get(pk=id)
    return render(request, 'blog/user_page.html', {'user':current_user})


@login_required
def newsfeed(request):
    current_user = request.user
    follow_list = current_user.profile.following.all()
    post_list = list()
    for user in follow_list:
        for post in user.post_set.all():
            post_list.append(post)
    for i in range(0, len(post_list)-1):
        for j in range(i+1, len(post_list)):
            if post_list[i].date_published < post_list[j].date_published:
                post_list[i], post_list[j] = post_list[j], post_list[i]
    return render(request, 'blog/newsfeed.html', {'post_list': post_list})



@login_required
def list_of_users(request):
    current_user = request.user
    list_of_users = User.objects.exclude(pk = current_user.pk)
    return render(request, 'blog/list_of_users.html', {'list_of_users':list_of_users})


@login_required
def follow_user(request, username):
    current_user = request.user
    user = User.objects.get(username = username)
    current_userprofile = current_user.profile
    current_userprofile.following.add(user)
    return redirect('blog:following', user.id)


@login_required
def following(request,id):
    current_user = request.user
    userprofile = current_user.profile
    follow_list = userprofile.following.all()
    return render(request, 'blog/following.html', {'follow_list':follow_list})


@login_required
def unfollow(request, username):
    to_unfollow = User.objects.get(username=username)
    current_user = request.user
    userprofile = current_user.profile
    userprofile.following.remove(to_unfollow)
    return redirect('blog:newsfeed')


@login_required
def write_post(request):
    if request.method == 'GET':
        return render(request, 'blog/write_post.html')

    elif request.method == 'POST':
        current_user = request.user
        title = request.POST['title']
        text = request.POST['text']
        pub_date = datetime.datetime.now()
        post = Post(user = current_user, title = title, text = text)
        post.save()
        return redirect('blog:post_detail', post_pk = post.pk)


@login_required
def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.comments.all()
    return render(request, 'blog/post_detail.html', {'post':post, 'comments':comments,})



@login_required
def user_posts(request):
    current_user = request.user
    posts = current_user.post_set.all().order_by('date_published')
    return render(request, 'blog/user_posts.html', {'posts':posts})


@login_required
def delete_post(request, post_pk):
    user = request.user
    post = Post.objects.get(pk=post_pk)
    keep_record("post","delete",post_pk)
    post.delete()
    return user_page(request, user.id)


@login_required
def edit_profile(request):

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid:
            form.save()
            return redirect('blog:user_page', request.user.id)

    else:
        form=EditProfileForm(instance=request.user)
        return render(request, 'blog/edit_profile.html', {'form':form})

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('blog:user_page', request.user.id)

    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'blog/password.html', {'form':form})



@login_required
def comment(request, post_pk):
    current_user = request.user
    post = Post.objects.get(pk = post_pk)
    comment_text = request.POST['comment']
    comment = Comment(user = current_user, post = post, comment = comment_text)
    comment.save()
    return post_detail(request, post_pk)
