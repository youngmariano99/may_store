from django import forms

# Importamos el modelo User de Django para manejar usuarios
from django.contrib.auth.models import User

# Esta es una clase que hereda de forms.Form para crear un formulario de registro
# de usuarios. Contiene campos para el nombre de usuario, email y contraseña.
class RegisterForm(forms.Form):
    username = forms.CharField(required=True,
                               min_length=3,max_length=50,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'id': 'username',
                                    
                               }))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={
                                'class': 'form-control',
                                'id': 'email',
                                'placeholder': 'example@email.com'
                            }))
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'id': 'password',
                                      'placeholder': '********'
                               }))
    password2 = forms.CharField(label='Confirmar password',
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'id': 'password2',}))
    

    # Método para limpiar el campo de nombre de usuario.
    # Verifica si el nombre de usuario ya existe en la base de datos.
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')
        return username
    
    # Método para limpiar el campo de email.
    # Verifica si el email ya existe en la base de datos.
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')
        return email
    
    # Método para limpiar el campo de contraseña.
    # Verifica si las contraseñas coinciden.
    def clean(self):
        # Llama al método clean del padre para obtener los datos limpios
        # y realizar validaciones adicionales.
        cleaned_data = super().clean()
        # Verifica si las contraseñas coinciden
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'Las contraseñas no coinciden')
    
    def save(self):
        # Crea un nuevo usuario utilizando los datos del formulario
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        return user