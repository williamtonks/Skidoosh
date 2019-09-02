from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View, generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q

from .forms import ProfileForm, SignUpForm, DiscussionPostForm, EventPostForm, JoinGroupsForm, CommentForm
from .models import Profile, InterestGroup, GroupPost, DiscussionPost, EventPost, Comment

def home(request):
    if request.user.is_authenticated:
        if request.user.profile.name:
            return render(request, 'interest_groups/home.html')
        else:
            return redirect('signup')
    else:
        return redirect('login')


def privacy_policy(request):
    return render(request, 'interest_groups/privacy_policy.html')


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.name = form.cleaned_data.get('name')
            user.profile.bio = form.cleaned_data.get('bio')

            def clean_number(num):
                num = ''.join(c for c in num if c.isdigit())
                return "({}) {}-{}".format(num[0:3], num[3:6], num[6:])

            user.profile.phonenumber = clean_number(form.cleaned_data.get('phonenumber'))
            user.profile.year = form.cleaned_data.get('year')
            user.profile.picture = form.cleaned_data.get('picture')
            user.save()
            return redirect('my_profile')
    else:
        profile = request.user.profile
        form = SignUpForm(instance=profile)
    return render(request, 'registration/signup.html', {'form': form})


def signup(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():

            user = request.user
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.name = form.cleaned_data.get('name')
            user.profile.bio = form.cleaned_data.get('bio')

            def clean_number(num):
                return "({}) {}-{}".format(num[0:3], num[3:6], num[6:])

            user.profile.phonenumber = clean_number(form.cleaned_data.get('phonenumber'))
            user.profile.year = form.cleaned_data.get('year')
            user.profile.picture = form.cleaned_data.get('picture')
            user.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class ProfileListView(View):
    template_name = 'interest_groups/profiles.html'
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        self.context['profile_list'] = Profile.objects.all()
        return render(request, self.template_name, self.context)

class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'interest_groups/profile.html'

def my_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('profile', pk=request.user.profile.pk)

class CustomLoginView(LoginView):
    redirect_authenticated_user = True


def root_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return redirect('home')


class CustomLogoutView(LogoutView):
    next_page  = 'login'


class InterestGroupListView(View):
    template_name = 'interest_groups/group_list.html'
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        self.context['page_title'] = 'All Groups'
        self.context['group_list'] = InterestGroup.objects.all()
        return render(request, self.template_name, self.context)

class MyGroupsListView(View):
    template_name = 'interest_groups/group_list.html'
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        self.context['page_title'] = 'My Groups'
        self.context['group_list'] = self.request.user.profile.groups.all()
        return render(request, self.template_name, self.context)

class InterestGroupView(View):

    template_name = 'interest_groups/interest_group.html'
    context = {}
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')
        if('leave_group' in request.POST):
            request.user.profile.groups.remove(get_object_or_404(InterestGroup, pk=pk))
        elif('join_group' in request.POST):
            request.user.profile.groups.add(get_object_or_404(InterestGroup, pk=pk))
        return self.get(request, pk)

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')
        if (request.user.is_authenticated):
            self.context['interest_group'] = get_object_or_404(InterestGroup, pk=pk)
            self.context['posts'] = GroupPost.objects.filter(interest_group=pk)
            #self.context['posts'] = self.context['interest_group'].grouppost_set.order_by('-creation_date').get_cached_trees()
            if request.user.profile.groups.filter(pk=pk): #already in group
                self.context['edit_group_membership'] = 'Leave Group'
                self.context['edit_group_action'] = 'leave_group'
            else:
                self.context['edit_group_membership'] = 'Join Group'
                self.context['edit_group_action'] = 'join_group'
            return render(request, self.template_name, self.context)
        else:
            self.context['interest_group'] = get_object_or_404(InterestGroup, pk=pk)
            self.context['posts'] = GroupPost.objects.filter(interest_group=pk)
            return render(request, self.template_name, self.context)

class EditPost(View):
    template_name = 'interest_groups/create_post.html'
    context = {}

    def get(self, request, pk, post_id):
        if not request.user.is_authenticated:
            return redirect('login')
        post = get_object_or_404(GroupPost, pk=post_id)
        if(hasattr(post, 'discussionpost')):
            post = post.discussionpost
            self.context['form'] = DiscussionPostForm(instance=post)
            self.context['page_title'] = 'Edit Discussion Post'
        elif(hasattr(post, 'eventpost')):
            post = post.eventpost
            self.context['form'] = EventPostForm(instance=post)
            self.context['page_title'] = 'Edit Event Post'
        elif(hasattr(post, 'comment')):
            post = post.comment
            self.context['form'] = CommentForm(instance=post)
            self.context['page_title'] = 'Edit Comment'
        if(self.context['form']):
            return render(request, self.template_name, self.context)
        else:
            return HttpResponseRedirect(reverse('interest_group', args=(pk,)))

    def post(self, request, pk, post_id):
        if not request.user.is_authenticated:
            return redirect('login')
        post = get_object_or_404(GroupPost, pk=post_id)
        if post.author != request.user.profile:
            return HttpResponseRedirect(reverse('interest_group', args=(pk,)))
        if(hasattr(post, 'discussionpost')):
            form = DiscussionPostForm(request.POST)
            if form.is_valid():
                # post = form.save(commit=False)
                post = get_object_or_404(DiscussionPost, pk=post_id)
                post.title = form.cleaned_data.get('title')
                post.author = request.user.profile
                post.text = form.cleaned_data.get('text')
                post.interest_group = get_object_or_404(InterestGroup, pk=pk);
                post.save()
                return HttpResponseRedirect(reverse('interest_group', args=(pk,)))
        elif(hasattr(post, 'eventpost')):
            form = EventPostForm(request.POST)
            if form.is_valid():
                # post = form.save(commit=False)
                post = get_object_or_404(EventPost, pk=post_id)
                post.title = form.cleaned_data.get('title')
                post.author = request.user.profile
                post.text = form.cleaned_data.get('text')
                post.event_date = form.cleaned_data.get('event_date')
                post.interest_group = get_object_or_404(InterestGroup, pk=pk);
                post.save()
                return HttpResponseRedirect(reverse('interest_group', args=(pk,)))
        elif(hasattr(post, 'comment')):
            form = CommentForm(request.POST)
            if form.is_valid():
                # post = form.save(commit=False)
                post = get_object_or_404(Comment, pk=post_id)
                post.author = request.user.profile
                post.text = form.cleaned_data.get('text')
                post.interest_group = get_object_or_404(InterestGroup, pk=pk);
                post.save()
                return HttpResponseRedirect(reverse('interest_group', args=(pk,)))
        return HttpResponseRedirect(reverse('interest_group', args=(pk,)))
'''
class DeletePost(View):
    def get(self, request, post_id):
        if not request.user.is_authenticated:
            return redirect('login')
        post = get_object_or_404(GroupPost, post_id)
        if post.author == request.user.profile:
            post.delete()
        return render(request, self.template_name, self.context)
'''

def create_discussion_post(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    group = get_object_or_404(InterestGroup, pk=pk)
    if group not in request.user.profile.groups.all():
        return redirect('interest_group', pk=pk)
    if request.method == 'POST':
        form = DiscussionPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.text = form.cleaned_data.get('text')
            post.interest_group = get_object_or_404(InterestGroup, pk=pk)
            post.save()
            return HttpResponseRedirect(reverse('interest_group', args=(pk,)))
    else:
        form = DiscussionPostForm
    return render(request, 'interest_groups/create_post.html', {'page_title': 'Create Discussion Post','form': form})


def create_event_post(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    group = get_object_or_404(InterestGroup, pk=pk)
    if group not in request.user.profile.groups.all():
        return redirect('interest_group', pk=pk)
    if request.method == 'POST':
        form = EventPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.text = form.cleaned_data.get('text')
            post.event_date = form.cleaned_data.get('event_date')
            post.interest_group = get_object_or_404(InterestGroup, pk=pk)
            post.save()
            post.likes.add(request.user.profile)
            return HttpResponseRedirect(reverse('interest_group', args=(pk,)))
    else:
        form = EventPostForm
    return render(request, 'interest_groups/create_post.html', {'page_title': 'Create Event Post', 'form': form})

def create_comment(request, pk, parent):
    if not request.user.is_authenticated:
        return redirect('login')
    group = get_object_or_404(InterestGroup, pk=pk)
    if group not in request.user.profile.groups.all():
        return redirect('interest_group', pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.profile
            comment.text = form.cleaned_data.get('text')
            comment.interest_group = get_object_or_404(InterestGroup, pk=pk)
            parent = get_object_or_404(GroupPost, pk=parent)
            comment.insert_at(parent, save=True)
            return HttpResponseRedirect(reverse('interest_group', args=(pk,)))
    else:
        form = CommentForm
    return render(request, 'interest_groups/create_post.html', {'page_title': 'Create Comment', 'form': form})

def like_post(request, pk, post_id,):
    if not request.user.is_authenticated:
        return redirect('login')
    group = get_object_or_404(InterestGroup, pk=pk)
    post = get_object_or_404(GroupPost, pk=post_id)
    try:
        if request.user.profile in group.profile_set.all() and request.user.profile not in post.likes.all():
            post.likes.add(request.user.profile)
            post.save()
    except Profile.DoesNotExist:
        pass;
    except Profile.MultipleObjectsReturned:
        pass;
    return HttpResponseRedirect(reverse('interest_group', args=(pk,)))

def unlike_post(request, pk, post_id,):
    if not request.user.is_authenticated:
        return redirect('login')
    group = get_object_or_404(InterestGroup, pk=pk)
    post = get_object_or_404(GroupPost, pk=post_id)
    try:
        if request.user.profile in group.profile_set.all() and request.user.profile in post.likes.all():
            post.likes.remove(request.user.profile)
            post.save()
    except Profile.DoesNotExist:
        pass;
    except Profile.MultipleObjectsReturned:
        pass;
    return HttpResponseRedirect(reverse('interest_group', args=(pk,)))

def add_groups(request):
    if not request.user.is_authenticated:
        return redirect('login')
    unjoined_groups = set(InterestGroup.objects.all()) - set(request.user.profile.groups.all())
    no_groups = len(unjoined_groups) == 0
    if request.method == 'POST':
        if request.POST.get('choices'):
            for choice in request.POST.getlist('choices'):
                request.user.profile.groups.add(InterestGroup.objects.get(id=int(choice)))
        return redirect('home')
    return render(request, 'interest_groups/add_groups.html', {'group_list':unjoined_groups, 'no_groups':no_groups})


def search(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request == None:
        return redirect('home')
    search_q = request.GET.get("q")
    group_list = InterestGroup.objects.all()
    if search_q:
        group_results = group_list.filter(Q(name__icontains=search_q) | Q(description__icontains=search_q))
        profile_results = Profile.objects.all().filter(Q(name__icontains=search_q) | Q(bio__icontains=search_q))
        context = {'search_q':search_q, 'group_results':group_results, 'profile_results':profile_results}
    else:
        group_results = None
        profile_results = None
        context = {'search_q':search_q, 'group_results':group_list, 'profile_results':profile_results}
    return render(request, 'interest_groups/search_results.html', context)
