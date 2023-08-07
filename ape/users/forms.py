from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.forms import inlineformset_factory
from .models import Question, Choice, Course



class CreateUserForm(UserCreationForm):
    full_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    class Meta:
        model = User
        fields = ['full_name','username','email','password1','password2', 'user_type']
    email = forms.EmailField()
    
    USER_TYPES = [('lecturer', 'Lecturer'), ('student', 'Student')]
    user_type = forms.ChoiceField(choices=USER_TYPES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2', 'user_type']


   


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'email', 'bio', 'profile_photo', 'programming_in_c_score']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['profile_photo'].widget.attrs.update({'class': 'form-control-file'})


     
class QuestionForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)

    class Meta:
        model = Question
        fields = ['course', 'question_text', 'code_snippet', 'question_type']



        
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'is_correct', 'code_snippet']

ChoiceFormSet = inlineformset_factory(Question, Choice, form=ChoiceForm, extra=4, max_num=4, validate_max=True)


