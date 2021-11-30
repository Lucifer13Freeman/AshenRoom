from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from .models import Room, User


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['admin', 'members']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['bio'].required = False