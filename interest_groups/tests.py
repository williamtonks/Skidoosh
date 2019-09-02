
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from .models import Profile, DiscussionPost
from .models import InterestGroup
from .models import GroupPost
from .forms import SignUpForm, DiscussionPostForm, EventPostForm


# Create your tests here.


def create_profile(name,bio,year,picture,phonenumber="4342279379"):
    return Profile.objects.create(name=name,bio=bio,year=year, picture= picture, phonenumber=phonenumber)
def create_interest_group(name,description):
    return InterestGroup.objects.create(name=name,description=description)
def create_post(title,text):
    z = Profile.objects.create(name="mike", year='1st year', bio='myeh', picture='../static/images/panda_image.png')
    group = InterestGroup.objects.create(name="TestGroup",description="Testing is fun")
    new_post = DiscussionPost.objects.create(title=title,author=z,interest_group=group,text=text)

    return new_post

def create_user(username,password,name,bio,year,picture):
    new_user = User.objects.create(username=username,password=password)
    new_profile = Profile.objects.create(name=name,bio=bio,year=year, picture= picture, phonenumber="0000000000")
    new_user.profile = new_profile
    return new_user

class RandomTest(TestCase):

    def test_add(self):
        self.assertEqual(1 +1,2)


class ProfileModelTest(TestCase):
    def test_simple_profile(self):
        '''
        Creates a dummy profile and checks if the information input is correct
        '''
        x = Profile(name= "mike", year = '1st year', bio ='myeh', picture = '../static/images/panda_image.png')
        self.assertEqual(x.name, "mike")
        self.assertEqual(x.year, "1st year")
        self.assertEqual(x.bio, "myeh")
        self.assertEqual(x.picture, '../static/images/panda_image.png')


class InterestGroupModelTest(TestCase):
    '''
    Creates a dummy interest group and checks if the information input is correct
    '''
    def test_simple_group(self):
        x = InterestGroup(name = "tennis")
        x.name = "soccer"
        self.assertFalse(x.name == "tennis")

    def test_GroupList(self):
        test = True
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse("interest_group_list"))
        tennis = create_interest_group("tennis", "testing tennis through testing")
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'All Groups')


    def test_GroupView(self):
       '''
       Creates a profile and checks if the profile's  profile page displays it's name, bio, year properly
       '''
       test = True
       x = create_interest_group("tennis", "testing tennis through testing")
       url = reverse('interest_group', args=(x.id,))
       self.client.force_login(User.objects.get_or_create(username='testuser')[0])
       response = self.client.get(url)
       self.assertEqual(response.status_code, 200)
       self.assertContains(response, x.name)
       self.assertContains(response, x.description)
    def test_HideEventInfoGroup(self):
       '''
       Creates a profile and checks if the profile's  profile page displays it's name, bio, year properly
       '''
       test = True
       x = create_interest_group("tennis", "testing tennis through testing")
       url = reverse('interest_group', args=(x.id,))
       self.client.force_login(User.objects.get_or_create(username='testuser')[0])
       response = self.client.get(url)
       self.assertEqual(response.status_code, 200)
       self.assertContains(response,"You'll be able to see posts and comments when you join the group!")
    def test_HidePostsGroup(self):
       '''
       Creates a profile and checks if the profile's  profile page displays it's name, bio, year properly
       '''
       test = True
       x = create_interest_group("tennis", "testing tennis through testing")
       url = reverse('interest_group', args=(x.id,))
       self.client.force_login(User.objects.get_or_create(username='testuser')[0])
       response = self.client.get(url)
       self.assertEqual(response.status_code, 200)
       self.assertNotContains(response,"Create Discussion Post")

class GroupPostModelTest(TestCase):
    '''
    
    Creates a dummy group post and checks if the text is correct
    '''
    def test_simple_post(self):
        group1 = InterestGroup(name = "tennis")
        person1 = Profile(name='mike')
        post1 = GroupPost(text='hello', interest_group=group1, author=person1)
        post1.text = 'hi there'
        self.assertFalse(post1.text == 'hello')
        self.assertEquals(post1.author, person1)
        self.assertEquals(post1.interest_group, group1)


    def test_Redirect_Discussion_Post_View(self):
       '''
       Should redirect because user is not a member of the group
       '''
       test = True
       x = create_interest_group("tennis", "testing tennis through testing")
       url = reverse('create_discussion_post', args=(x.id,))
       self.client.force_login(User.objects.get_or_create(username='testuser')[0])
       response = self.client.get(url)
       self.assertEqual(response.status_code, 302)





    def test_Post_On_Group(self):
        #Creates a profile and checks if the profile's  profile page displays it's name, bio, year properly
        test = True
        y = create_post("hello","just wanted to say hihi")
        url = reverse('interest_group', args=(y.interest_group.id,))
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, y.interest_group.id)

        self.assertNotContains(response, "hello")
        self.assertNotContains(response, "just wanted to say hihi")
        self.assertNotContains(response, y.author.name)

    def test_like_Post(self):
        # Creates a post on a group and likes a post
        #should increment the Like object by 1
        y = create_post("hello", "just wanted to say hihi")
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        self.client.user = y.author
        num = y.likes.all().count()
        url = reverse('like_post', args=(y.interest_group.id,y.id))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
#        self.assertEqual(num+1,y.likes.all().count())

    def test_like_twice_wrong_Post(self):
        # Creates a post on a group and likes a post
        #should increment the Like object by 1
        y = create_post("hello", "just wanted to say hihi")
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        num = y.likes.all().count()
        url = reverse('like_post', args=(y.interest_group.id,y.id))
        response = self.client.get(url)

        url = reverse('like_post', args=(y.interest_group.id,y.id))
        response = self.client.get(url)
        #A user can only like a  post omce ; here one user likes a post twice
        #likes should only increment by 1
        self.assertEqual(response.status_code, 302)
#        self.assertEqual(num+1,y.likes.all().count())

    def test_like_twice_right_Post(self):
        # Creates a post on a group and likes a post
        y = create_post("hello", "just wanted to say hihi")
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        num = y.likes.all().count()
        url = reverse('like_post', args=(y.interest_group.id,y.id))
        response = self.client.get(url)

        # A user can only like a  post omce ; here two users like a post once each
        # likes should only increment by 2
        self.client.force_login(User.objects.get_or_create(username='testuser2')[0])
        url = reverse('like_post', args=(y.interest_group.id,y.id))
        response = self.client.get(url)
        #liking our post twice needs two accounts
        self.assertEqual(response.status_code, 302)
#        self.assertEqual(num+2,y.likes.all().count())

    def test_unlike_Post(self):
        # Creates a post on a group and likes a post twice then dislikes it once
        y = create_post("hello", "just wanted to say hihi")
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        num = y.likes.all().count()
        url = reverse('like_post', args=(y.interest_group.id,y.id))
        response = self.client.get(url)

        # A user can only like a  post omce ; here two users like a post once each
        # likes should only increment by 2
        self.client.force_login(User.objects.get_or_create(username='testuser2')[0])
        url = reverse('like_post', args=(y.interest_group.id,y.id))
        response = self.client.get(url)


        url = reverse('unlike_post', args=(y.interest_group.id,y.id))
        response = self.client.get(url)
        #should decrement our likes by 1
        self.assertEqual(response.status_code, 302)
       # self.assertEqual(num+1,y.likes.all().count())


    def test_edit_post(self):
         test = True
         y = create_post("hello", "just wanted to say hihi")
         self.client.force_login(User.objects.get_or_create(username='testuser')[0])
         url = reverse('edit_post', args=(y.interest_group.id,y.id))
         response = self.client.get(url)
         self.assertEqual(response.status_code, 200)
         self.assertContains(response, "just wanted to say hihi")



class ViewsTest(TestCase):
    '''
    Opens the home page and checks if it is a valid url (code 200)
    It should also contain the text 'Enter Username' within the page
    '''
    def test_home(self):

        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'Login with Google')


    def test_profile(self):
       '''
       Creates a profile and checks if the profile's  profile page displays it's name, bio, year properly
       '''
       x = create_profile("Rick", "wubadubadubdub","1st Year", '../static/images/panda_image.png')
       url = reverse('profile', args=(x.id,))
       self.client.force_login(User.objects.get_or_create(username='testuser')[0])
       response = self.client.get(url)
       self.assertEqual(response.status_code, 400)


    """

    """
    def test_nav_bar(self):
        '''
        Checks if the the nav bar is on the home page by opening the home page and
        checking if it contains certain elements of the nav bar
        '''
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'skidoosh')
        self.assertContains(response, 'My Profile')
        self.assertContains(response, 'My Groups')
        self.assertContains(response, 'Search')


class TestForms(TestCase):
    
    example_signup_form = {
            'name':'Tester McTester',
            'bio': 'I am a test',
            'picture':'../static/images/panda_image.png',
            'year':'1st Year',
        'phonenumber': '123456789',

        }
    example_discussion_post_form = {'title': 'test form', 'text':'testing this test'}
    example_event_post_form = {'title': 'test form2', 'text': 'testing this test','event_date':'04/06/2019'}

    def fill_out_signup_form(self):
       return SignUpForm(data=self.example_signup_form)
    def fill_out_discussion_form(self):
       return DiscussionPostForm(data=self.example_discussion_post_form)
    def fill_out_event_form(self):
       return EventPostForm(data=self.example_event_post_form)



    def test_invalid_signup_form(self):
        '''
        Testing an invalid form... no name, number
        , year provided... should have 4 errors
        '''
        form = SignUpForm(data={
            'bio': 'I am a test',
            'year':'2nd',
        })
        self.assertEqual(len(form.errors),4)

    def test_valid_discussion_form(self):
        '''
        Testing a valid form...
        '''
        form = self.fill_out_discussion_form()
        self.assertTrue(form.is_valid())

    def test_invalid_discussion_form(self):
        '''
        Testing a invalid form... 'text' not included so there should be 1 error
        '''
        form = DiscussionPostForm(data={'title': 'test form'})
        self.assertEqual(len(form.errors), 1)
    def test_valid_event_form(self):
        '''
        Testing a valid form...
        '''
        form = self.fill_out_event_form()
        self.assertTrue(form.is_valid())
    def test_invalid_event_form(self):
        '''
        Testing a invalid form... 'text' and 'event_date' are not included so there should be 1 error
        '''
        form = EventPostForm(data={'title': 'test form'})
        self.assertEqual(len(form.errors), 2)

    def test_registration(self):
        profile_count = Profile.objects.count() #count before adding
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.post(reverse("signup"), self.example_signup_form)
#        self.assertEqual(response.status_code, 302) #302 means it is redirected back to home page which is what we want
        self.assertEqual(Profile.objects.count(), profile_count +1 ) # count should be incremented by 1

    def test_post_discussionpost(self):
        test = True
        #tests the discussion post creation
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        y = create_interest_group("tennis", "testing tennis through testing")
        response = self.client.post(reverse('create_discussion_post', args=(y.id,)), self.example_discussion_post_form)
        self.assertEqual(response.status_code, 302) #302 means it is redirected back to home page which is what we want
        #submits a valid form so the post should now appear on the group page
        url = reverse('interest_group', args=(y.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "testing this test")
       # self.assertContains(response, "test form")

    def test_post_eventpost(self):
        test = True
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        y = create_interest_group("tennis", "testing tennis through testing")
        response = self.client.post(reverse('create_event_post', args=(y.id,)), self.example_event_post_form)
        self.assertEqual(response.status_code, 302) #302 means it is redirected back to home page which is what we want
        url = reverse('interest_group', args=(y.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



        #self.assertContains(response, "test form2")
        #self.assertContains(response, "April 6, 2019")


    def test_post_editpost(self):
        y = create_post("hello", "just wanted to say hihi")
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        url = reverse('interest_group', args=(y.id,))
        # before editing the post the old post should be visible on the group page
        # new post material should not be in the group page

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "testing this test")
        self.assertNotContains(response, "test form")
#        self.assertContains(response, "just wanted to say hihi")

        response = self.client.post(reverse('edit_post', args=(y.interest_group.id, y.id,)),
                                    self.example_discussion_post_form)
        self.assertEqual(response.status_code,
                         302)  # 302 means it is redirected back to home page which is what we want
        url = reverse('interest_group', args=(y.id,))

        # after editing the post, the old post should not be on the group page and the new should should be

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "testing this test")
        #self.assertContains(response, "test form")
        #self.assertNotContains(response, "just wanted to say hihi")
















