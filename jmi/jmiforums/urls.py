"""jmi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
# from .views import PostListView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView

app_name = "jmiforums"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search, name='search'),
    path("register/subforum/", views.create, name="create"),
    path("register/user/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("<slug:subforum_name>/question/", views.question, name="question"),
    path("question/", views.instant_question, name="instant_question"),
    path("<slug:subforum_name>/<int:ques_id>/view/", views.view_question, name="view_question"),
    path("<slug:subforum_name>/<int:ques_id>/update/", views.ques_update, name="ques_update"),
    path("<slug:subforum_name>/<int:ques_id>/delete/", views.ques_delete, name="ques_delete"),
    # path("<slug:subforum_name>/<int:ques_id>/answer/", views.answer, name='answer'),
    path("profile/edit/", views.edit_profile, name='edit_profile'),
    path("profile/edit/password/", views.change_password, name='change_password'),
    path("upvote/", views.upvote, name='upvote'),
    # path("article/<slug:subforum_name>", views.article, name='article'),
    # path("profile/reset/password/", PasswordResetView.as_view(), {'template_name':'jmiforums/reset_password.html', 'post_reset_redirect': 'jmiforums:reset_password_done', 'email_template_name': 'jmiforums/reset_password_email.html'}, name='reset_password'),
    # path("profile/reset/password/done/", PasswordResetDoneView.as_view(), name='reset_password_done'),
    # path("profile/reset/password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/", PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path("<slug:subforum_name>/", views.subforum, name='subforum'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
