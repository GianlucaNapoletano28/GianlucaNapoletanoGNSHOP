
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rimuovi help_texts di default di Django
        for field in self.fields:
            self.fields[field].help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Controlla se l'email esiste già nel database
            if get_user_model().objects.filter(email__iexact=email).exists():
                raise forms.ValidationError("Un utente con questa email esiste già.")
        return email

    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        if password2:
            if len(password2) < 8:
                raise forms.ValidationError("La password deve essere lunga almeno 8 caratteri.")
            if not any(char.isdigit() for char in password2):
                raise forms.ValidationError("La password deve contenere almeno un numero.")
        return password2

    error_messages = {
        'password_mismatch': "Le due password non coincidono.",
        'unique': "Un utente con questo valore esiste già.",
        'required': "Questo campo è obbligatorio.",
        'invalid': "Inserisci un valore valido.",
    }

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'username': 'Nome utente',
            'email': 'Email',
            'first_name': 'Nome',
            'last_name': 'Cognome',
            'password1': 'Password',
            'password2': 'Conferma password',
        }
        help_texts = {
            'username': '',
            'email': '',
            'first_name': '',
            'last_name': '',
            'password1': '',
            'password2': '',
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
