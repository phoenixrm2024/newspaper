# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            'username',
            'email',
            'age',
            )

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = (
            'username',
            'email',
            'age',
            )

# class Meta: a subclass that contains metadata uses to 'change' the behavior 
# of our model 'fields', like changes in fields ordering ,verbose_name, ...