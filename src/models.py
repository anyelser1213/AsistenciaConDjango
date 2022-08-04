import os
import shutil #libreria para borrar carpetas esten o no llenas
from django.conf import settings
from django.db import models

#Estos dos modelos son para crear permisos personalizados
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete


# Create your models here.


############################FUNCIONES####################################################
#Funcion para agregar carpetas al usuario
def direccion_usuarios(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    print(instance)
    print(instance.id)
    print(instance.username)
    return 'usuarios/fondos/{0}/{1}'.format(instance.username, filename)



#########################################################################################

##################################################################################################
####################### Modelos para Usuarios ####################################################

class UsuarioManager(BaseUserManager):

    def create_user(self,email,username,password=None,admin = False,is_superuser =False,plan_elegido="gratis"):
        print("Creamos Usuario Normal")
        #if not email:
        #    raise ValueError('El usuario debe tener un correo electronico')

        usuario = self.model(
            
            username = username,
            password = password,
            #rol = rol,
            admin =admin,
            is_superuser = is_superuser,
            #plan_elegido = plan_elegido,
        )

        #aqui encriptamos la clave para no guardar en texto plano
        print("ENCRIPTAMOS", password)
        usuario.set_password(password)
        usuario.save()
        return usuario
    
    

    #Funcion para usuario administrador
    def create_superuser(self,email,username,password,admin = True,is_superuser = True):
        print("Creamos superusuario")

        usuario = self.create_user(
            username = username,
            #rol = rol,
            #plan_elegido = plan_elegido,
            password = password,
            admin =admin,
            is_superuser = is_superuser
        )
        
            
            
        print("Entramos en superuser")
        input()
        usuario.save()
        return usuario





class Empresa(models.Model):

    nombre = models.CharField("nombre",max_length=200,unique=True)


    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        db_table = 'Empresas'
        
        permissions = [
            #(Lo que se guarda en bases de datos, lo que se ve al usuario)
            #Permisos para master y gerente
            #("permisoscompletos", "Permisoscompletos"),
            ]





# Heredamos de AbstractBaseUser para adaptarlo a nuestro gusto
class Usuarios(AbstractBaseUser,PermissionsMixin):

    #(Lo que se guarda en bases de datos, lo que se ve al usuario)
    usuario_tipos = [
        ('master','Master'),
    #    ('empresa','Empresa'),
    #    ('entrevistador','Entrevistador'),
    #    ('candidato','Candidato'),
        ('usuario','Usuario'),
    ]

    tipo_horario = [
        ('mañana','Mañana'),
        ('tarde','Tarde'),
        ('noche','Noche'),
    ]

    tipo_genero = [
        ('mujer','Mujer'),
        ('hombre','Hombre'),
        ('otro','Otro'),
    ]
    
    id = models.AutoField(primary_key=True)
    username = models.CharField("username",max_length=200,unique=True)
    apellido = models.CharField("apellido",max_length=200,blank=True, null=True) 
    cargo = models.CharField("cargo",max_length=200,blank=True, null=True) 
    horario = models.CharField("Horario",max_length=150,choices=tipo_horario,default='mañana')
    genero = models.CharField("Genero",max_length=150,choices=tipo_genero,default='hombre')
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE,blank=True, null=True)
    activo = models.BooleanField(default=True)#Para poder ingresar al sistema  
    is_superuser = models.BooleanField(default=False)#Este es superusuario
    admin = models.BooleanField(default=False)#Para poder ingresar al admin de django
    fecha_creacion = models.DateTimeField(auto_now_add=True) 
    ultimo_ingreso = models.DateTimeField('actualizado', auto_now=False)
    
    
    #rol = models.CharField("Rol",max_length=150,choices=usuario_tipos,default='usuario',blank=True, null=True)

    #Para enlazar al manager que has creado
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'  #Para estableccer este campo como unico
    REQUIRED_FIELDS = ['is_superuser'] # Campos obligatorios(los pide cuando los creas por consola)

    def __str__(self):
        return f'Usuario {self.username}'
    
    
    
    #para verificar si un usuario es administrador o no(Para entrar en el admin)
    @property
    def is_staff(self):
         # "Is the user a member of staff?"
         if self.activo:
            return self.admin
         return False
     

    def has_module_perms(self, app_label):
        return True

    

################# AQUI HACEMOS TODAS LAS PRUEBAS #########################




    def save(self, *args, **kwargs):
        
        super(Usuarios, self).save(*args, **kwargs)
        
        
        
        print(self.id)
        print("metodo jajajaj:",self._state.adding)



    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'usuarios'
        
        permissions = [
            #(Lo que se guarda en bases de datos, lo que se ve al usuario)
            #Permisos para master y gerente
            #("permisoscompletos", "Permisoscompletos"),
            
            
            
            
            
            
        ]#Fin de los permisos



class Asistencia(models.Model):

    tipo_registro = [
        ('entrada','Entrada'),
        ('salida','Salida'),
    ]

    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuarios,on_delete=models.CASCADE,blank=True, null=True)
    calendario = models.DateTimeField()
    registro = models.CharField("Registro",max_length=150,choices=tipo_registro,default='entrada')


    def __str__(self):
        return f'{self.usuario.username} registro: {self.registro}'