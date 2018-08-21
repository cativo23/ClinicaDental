from django import forms
from myauth.models import MyUser


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    username = forms.CharField(label='Usuario', required=True, )
    avatar = forms.ImageField(
                             label='Imagen',
                             required=False, )
    email = forms.EmailField(label='Email',
                             help_text='Un correo valido porfavor',
                             required=True, )

    class Meta:
        model = MyUser
        fields = ('username', 'avatar', 'email', )
