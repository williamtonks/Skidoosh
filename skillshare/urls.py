from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import static
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

import interest_groups.views
import skillshare.settings as settings


app_name = 'interest_groups'
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', interest_groups.views.root_redirect, name='root'),
    path('', include('social_django.urls', namespace='social')),
    path('home/', interest_groups.views.home, name='home'),
    path('profiles/',interest_groups.views.ProfileListView.as_view(), name='profiles'),
    path('profile/<int:pk>/', interest_groups.views.ProfileView.as_view(),name='profile'),
    path('profile/', interest_groups.views.my_profile, name='my_profile'),
    path('profile/my_groups/', interest_groups.views.MyGroupsListView.as_view(), name='my_groups'),
    path('signup/', interest_groups.views.signup, name='signup'),
    path('edit_profile/', interest_groups.views.edit_profile, name='edit_profile'),
    path('logout/', interest_groups.views.CustomLogoutView.as_view(), name='logout'),

    path('privacy_policy/', interest_groups.views.privacy_policy, name='privacy_policy'),
    path('', include('django.contrib.auth.urls'), name='login'),
    path('group/list/', interest_groups.views.InterestGroupListView.as_view(), name='interest_group_list'),
    path('group/<int:pk>/', interest_groups.views.InterestGroupView.as_view(), name='interest_group'),
    path('addgroups/', interest_groups.views.add_groups, name='add_groups'),

    path('group/<int:pk>/create_discussion_post/', interest_groups.views.create_discussion_post, name='create_discussion_post'),
    path('group/<int:pk>/create_event_post/', interest_groups.views.create_event_post, name='create_event_post'),
    path('group/<int:pk>/create_comment/<int:parent>', interest_groups.views.create_comment, name='create_comment'),

    path('group/<int:pk>/edit_post/<post_id>', interest_groups.views.EditPost.as_view(), name='edit_post'),

    path('group/<int:pk>/like_post/<post_id>/', interest_groups.views.like_post, name='like_post'),
    path('group/<int:pk>/unlike_post/<post_id>/', interest_groups.views.unlike_post, name='unlike_post'),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
    url('search', interest_groups.views.search, name='search'),
]