from django import forms
from django.contrib.auth.models import User
from .models import Profile, Workout, Exercise


class UserAccountForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=(('male', 'Male'), ('female', 'Female')))

    class Meta:
        model = Profile
        exclude = ['username', ]
        fields = ('weight', 'body_fat', 'avatar', 'about', )


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ('id', 'date_for_completion', 'title', 'workout_image', 'target_muscle', 'training_type', 'slug', 'user')


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = '__all__'