from django import forms
from myauth.models import MyUser



class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    MALE= 'M'
    FEMALE = "F"
    NO = "N"
    SEX_CHOICES = (
        (MALE, 'Masculino'),
        (FEMALE, 'Femenino'),
        (NO, "No decir"),
    )
    username = forms.CharField(label='Usuario', required=True, )
    avatar = forms.ImageField(
                             label='Imagen',
                             required=False, )
    email = forms.EmailField(label='Email',
                             help_text='Un correo valido porfavor',
                             required=True, )
    sex = forms.ChoiceField(choices=SEX_CHOICES , label='Sexo',
                            required=True, )

    class Meta:
        model = MyUser
        fields = ('username', 'avatar', 'email',  'sex',)
