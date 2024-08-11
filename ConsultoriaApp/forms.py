from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class UserCreationFormWithEmail(UserCreationForm):
    """
    Formulario que incluye campos adicionales como el correo electrónico, 
    el nombre y el apellido de los usuarios (ya que en el formulario por 
    defecto la clase "UserCreationForm" la cual solo registra usuario y contraseña).

    Atributos:
    - email (EmailField): Campo de correo electrónico requerido.
    - first_name (CharField): Campo de nombre del usuario.
    - last_name (CharField): Campo de apellido del usuario.
    """
    email = forms.EmailField(max_length=254, help_text='Se requiere información valida del correo.')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30) 

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

