from django import forms
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.forms import ClearableFileInput, ModelForm, widgets
from src.models import *



class loginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        #usuario_id = kwargs.pop('usuario')
        super(loginForm, self).__init__(*args, **kwargs)
        print("Formulario Login Form")
        #self.fields['creado_por'].empty_label = None
        #self.fields['creado_por'].queryset= Usuarios.objects.filter(id=usuario_id)


        
        #self.fields['tipo_reporte'].widget.attrs.update({'class': 'selects form-control' })

        #self.fields['descripcion'].widget.attrs.update({'placeholder': 'Descripción','autofocus': 'true','class': 'descripcion form-control' })
        self.fields['username'].error_messages = {'required': 'Esto es grave aqui!'}
        self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder':'Ingresar Usuario' })
        self.fields['password'].widget.attrs.update({'class': 'form-control','placeholder':'Ingresar Contraseña' })

    class Meta:
        labels = {
            'username': ('Writer'),
        }
        help_texts = {
            'username': ('Probando cosas'),
        }
        error_messages = {
            'username': {
                'max_length': ("This writer's name is too long."),
            },
        }
        widgets = {
            #"creado_por": forms.Select(attrs={'class': 'form-control' }),
            #"username": forms.TextInput(attrs={'class': 'form-control ', 'placeholder':'Enter username' }),
            #"nombres": forms.TextInput(attrs={'class': 'form-control ', 'placeholder':'Enter name' }),
            #"email": forms.EmailInput(attrs={'class': 'browser-default' , 'placeholder':'Enter email'}),
            #"apellidos": forms.TextInput(attrs={'class': 'browser-default ', 'placeholder':'Enter full name' }),
            #"cedula": forms.NumberInput(attrs={'class': 'form-control ', 'placeholder':'Enter DNI' }),
            #"compañia": forms.Select(attrs={'class': 'form-control' }),
            #"rol": forms.Select(attrs={'class': 'form-control' }),
            #"direccion": forms.TextInput(attrs={'class': 'form-control ', 'placeholder':'Enter Address' }),
            #"telefono": forms.TextInput(attrs={'class': 'form-control ', 'placeholder':'Enter telephone' }),
            #"imagen": forms.FileInput(attrs={'class': 'form-control' }),
            #"password1": forms.PasswordInput(attrs={'class': 'form-control' }),
            #'password1': forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})),
            #"password2": forms.PasswordInput(attrs={'class': 'form-control' }),
            #"nombres": forms.TextInput(attrs={'class': 'form-control ', 'placeholder':'Enter name' }),

            
        }

        #self.fields['fotografia'].widget.attrs.update({'class': 'dropify form-control' })


    


class UsuariosForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        #usuario_id = kwargs.pop('usuario')
        super(UsuariosForm, self).__init__(*args, **kwargs)
        print("Formulario UsuariosForm")

        self.fields['password1'].widget = widgets.PasswordInput(
            attrs={
                'placeholder': 'New password',
                'class': 'browser-default'
            })
        self.fields['password2'].widget = widgets.PasswordInput(
            attrs={
                'placeholder': 'Repeat password',
                'class': 'browser-default'
            })

     

    class Meta:
        model = Usuarios
        #fields = "__all__"
        #fields = ["username","nombres","apellidos","email","compañia","cedula","direccion","rol","telefono","imagen","is_superuser","admin"]
        #fields = ["username","apellidos","email","direccion","rol","telefono","imagen"]
        fields = ["username","apellido"]
        widgets = {
            #"creado_por": forms.Select(attrs={'class': 'form-control' }),
            "username": forms.TextInput(attrs={'class': 'browser-default ', 'placeholder':'Enter username' }),
            #"nombres": forms.TextInput(attrs={'class': 'form-control ', 'placeholder':'Enter name' }),
            #"email": forms.EmailInput(attrs={'class': 'browser-default' , 'placeholder':'Enter email'}),
            "apellido": forms.TextInput(attrs={'class': 'browser-default ', 'placeholder':'Enter full name' }),
            #"cedula": forms.NumberInput(attrs={'class': 'form-control ', 'placeholder':'Enter DNI' }),
            #"compañia": forms.Select(attrs={'class': 'form-control' }),
            #"rol": forms.Select(attrs={'class': 'form-control' }),
            #"direccion": forms.TextInput(attrs={'class': 'form-control ', 'placeholder':'Enter Address' }),
            #"telefono": forms.TextInput(attrs={'class': 'form-control ', 'placeholder':'Enter telephone' }),
            #"imagen": forms.FileInput(attrs={'class': 'form-control' }),
            #"password1": forms.PasswordInput(attrs={'class': 'form-control' }),
            #'password1': forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})),
            #"password2": forms.PasswordInput(attrs={'class': 'form-control' }),
            #"nombres": forms.TextInput(attrs={'class': 'form-control ', 'placeholder':'Enter name' }),

            
        }
        
    def clean_username(self):
        username = self.cleaned_data['username']
        username_taken = Usuarios.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('El nombre de usuario ya esta en usooooo.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        email_taken = Usuarios.objects.filter(email=email).exists()
        if email_taken:
            raise forms.ValidationError('El email ya esta en uso.')
        return email

    
    def clean_password2(self):
        
        """
        validacion de contrasenas 

        metodo que valida que ambas contrasenas ingresadas sean iguales, esto antes de ser encriptadas
        y guardadas en la base de datos, retornar la contrasena valida.

        excepcions:
            ValidatorError -- cuando las contrasenas no son iguales muestra un mensaje de error
        
        """

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        print(self.cleaned_data)
        if password1 != password2:
            raise forms.ValidationError('las claves no son iguales')
        return password2


    def save(self, commit=True):
        user = super().save(commit=False) 
        user.set_password(self.cleaned_data['password1'])
        if commit: 
            user.save()
        return user


    


###################### AQUI COMIENZAN LOS FORMULARIOS PARA EDITAR EN EL ADMIN ##########################################

