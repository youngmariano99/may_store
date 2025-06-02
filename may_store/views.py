# Importamos las funciones de Django para manejar vistas y redirecciones
from django.shortcuts import render
from django.shortcuts import redirect

# Importamos las funciones de Django para manejar mensajes y autenticación
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

# Importamos el modelo User de Django para manejar usuarios
from django.contrib.auth.models import User

# Importamos el formulario de registro que hemos creado
from .forms import RegisterForm

from products.models import Product

# Vista para mostrar la página de inicio
def index(request):
    products = Product.objects.all().order_by('-id')

    return render(request, 'index.html', {
        # context (Sirve para dar dinamismo a la pagina)
        'message': 'Listado de Productos',
        'title': 'Productos',
        'products': products
    })

# Vista para manejar el inicio de sesión
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index') 
        
    if request.method == 'POST':
    # Aquí puedes manejar la lógica de inicio de sesión
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Auntenticación del usuario
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            
        
    return render(request, 'users/login.html', {
             
        })

# Vista para cerrar sesión
def logout_view(request):
    
    # Aquí puedes manejar la lógica de cierre de sesión
    # Por ejemplo, redirigir a la página de inicio de sesión
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    
    
    # Redirigir a la página de inicio de sesión
    return redirect('login')


# # Vista para registrar un nuevo usuario
def register(request):

    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)
    
    #Obtenemos la información de un formulario a partir de una clase
    if request.method == 'POST' and form.is_valid():
        
        # Obtenemos los datos del formulario
        # y los guardamos en la base de datos.
        user = form.save()

        # Si el usuario se creó correctamente, iniciamos sesión y redirigimos al usuario a la página de inicio.
        # El método create_user() se encarga de hashear la contraseña automáticamente.
        if user:
            login(request, user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('index')


    return render(request, 'users/register.html', {
        'form': form
    })        