from django.urls import path
from . import views


app_name="blog"

urlpatterns = [
    #path('', include('blog.urls')),
    path('', views.home, name="home"),
    #path('register/', views.register, name="register")
    path('signup/', views.signup, name="signup"),
    path('login_page/', views.login_page, name="login_page"),
    path('logout_page/', views.logout_page, name="logout_page"),
    path('<int:id>/user_page/', views.user_page, name="user_page"),
    path('list_of_users/', views.list_of_users, name="list_of_users"),
    path('follow_user/(?P<username>\w+)', views.follow_user, name="follow_user"),
    path('<int:id>/following/', views.following, name="following"),
    path('(?P<post_pk>[0-9]+)/', views.post_detail, name="post_detail"),
    path('write_post/', views.write_post, name="write_post"),
    path('newsfeed/', views.newsfeed, name="newsfeed"),
    path('user_posts/', views.user_posts, name="user_posts"),
    path('comment/(?P<post_pk>[0-9]+)/', views.comment, name="comment"),
    path('delete_post/(?P<post_pk>[0-9]+)/',views.delete_post, name="delete_post"),
    path('unfollow/(?P<username>\w+)', views.unfollow, name="unfollow"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('password/', views.change_password, name="password"),

]
