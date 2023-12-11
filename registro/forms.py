from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import UserMessage

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Nombre de usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.',
        'inactive': 'Esta cuenta está inactiva.',
    }

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['content']