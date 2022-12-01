from django import forms
from allauth.socialaccount.forms import SignupForm


class CustomSocialSignupForm(SignupForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}),max_length=50, label='Name')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}), label='Password')
    email = forms.EmailField(widget=forms.HiddenInput())
    def save(self, request):
        user = super(CustomSocialSignupForm, self).save(request)
        user.set_password(request.POST['password'])
        user.active = True
        user.name = request.POST['name']
        user.save()
        return user
    
class Form_Dist(forms.Form):
    select = forms.ChoiceField(choices=((1,"1/4 Miles"),(2,"1/2 Miles")))
    
class CreateRoom(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Room Name'}),max_length=50, label='Room Name')
