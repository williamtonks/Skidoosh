from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from interest_groups.models import Profile, GroupPost, DiscussionPost, EventPost, Comment, InterestGroup

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

def validate_number(num):
    digits_only = ''.join([digit for digit in num if digit.isdigit()])
    if not len(digits_only) == 10:
        raise ValidationError(_('Phone Number not understood. Please provide 10 digits.'))

def popover_html(label, content):
    return label + ' <a tabindex="0" role="button" data-toggle="popover" data-html="true" \
                            data-trigger="hover" data-placement="auto" data-content="' + content + '"> \
                            <span class="glyphicon glyphicon-info-sign"></span></a>'

class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'John Doe'}))
    bio = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"rows":4}))
    phonenumber = forms.CharField(label='Phone number', max_length=20, validators=[validate_number],
                                  widget=forms.TextInput(attrs={'placeholder': 'xxxxxxxxxx'}))
    year = forms.ChoiceField(choices=Profile.year_choices)
    picture = forms.ImageField(required=True)
    password1 = None
    password2 = None

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields['name'].help_text = "This should be your legal name to help other users identify you"
            self.fields['bio'].help_text = "Enter a short bio describing your interests"
            self.fields['phonenumber'].help_text = "Please enter your full 10 digit phonenumber"
            self.fields['year'].help_text = "Please select from the list the option that best describes you"
            self.fields['picture'].help_text = "Upload a recent picture of yourself or something important to you"
            if help_text != '':
                self.fields[field].widget.attrs.update({'class':'has-popover', 'data-content':help_text, 'data-placement':'right', 'data-container':'body'})

    class Meta:
        model = User
        fields = ('name', 'bio', 'year','phonenumber', 'picture')
        labels = {
            'name': popover_html('name', "This should be your full legal name!"),
            'bio': popover_html('bio', "This should describe you and what your interests/expertise are!"),
            'year': popover_html('year', "This is what year in college you are!"),
            'phonenumber': popover_html('phonenumber', "Please provide a valid (10 digit) phonenumber!"),
            'picture': popover_html('picture', "Upload a picture you think captures your essence!"),
        }

class DiscussionPostForm(ModelForm):
    title = forms.TextInput()
    text = forms.TextInput()

    class Meta:
        model = DiscussionPost
        fields = ('title', 'text',)

    def __init__(self, *args, **kwargs):
        super(DiscussionPostForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields['title'].help_text = "This will appear at the top of your created discussion post"
            self.fields['text'].help_text = "Please describe your ideas on the matter"
            if help_text != '':
                self.fields[field].widget.attrs.update({'class':'has-popover', 'data-content':help_text, 'data-placement':'right', 'data-container':'body'})

class EventPostForm(ModelForm):
    title = forms.TextInput()
    text = forms.TextInput()
    event_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',
            'placeholder': 'DD/MM/YYYY',
        })
    )
    class Meta:
        model = EventPost
        fields = ('title', 'text', 'event_date',)

    def __init__(self, *args, **kwargs):
        super(EventPostForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields['title'].help_text = "This will appear at the top of your created event post"
            self.fields['text'].help_text = "Please describe your event (include any needed equipment, skills, difficulty level)"
            self.fields['event_date'].help_text = "Please enter the date of your event. Write the time of day in the Title or Text."
            if help_text != '':
                self.fields[field].widget.attrs.update({'class':'has-popover', 'data-content':help_text, 'data-placement':'right', 'data-container':'body'})


class JoinGroupsForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset = InterestGroup.objects.all(),
        widget  = forms.CheckboxSelectMultiple,
    )


class CommentForm(ModelForm):
    text= forms.TextInput()
    class Meta:
        model = Comment
        fields = ('text',)
