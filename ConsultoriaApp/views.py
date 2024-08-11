from django.conf import settings
from .models import Pricing, Subscription, Cursos 
from .forms import UserCreationFormWithEmail
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

import stripe

#llave secreta de Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

#Interfaces de Menu
def inicio(request):
    """ Renderiza el archivo de inicio.html """
    return render(request, 'ConsultoriaApp/inicio.html')

def conocenos(request):
    """ Renderiza el archivo de Conocenos.html """
    return render(request, 'ConsultoriaApp/Conocenos.html')

def contacto(request):
    """Renderiza el archivo de contacto.html"""
    return render(request, 'ConsultoriaApp/Contacto.html')

#Interfaces del Login
def registro(request, *args, **kwargs):
    """ Maneja el registro de usuarios. Crea una cuenta de usuario y una suscripción de 
    prueba gratuita en Stripe."""
    if request.method == 'POST':
        form = UserCreationFormWithEmail(request.POST)
        if form.is_valid():
            # Registra al usuario
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # Autentica al usuario
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # Crea un cliente de Stripe asociado al nuevo usuario
            free_trial_pricing = Pricing.objects.get(name='Free Trial')

            subscription = Subscription.objects.create(
                user=user,
                pricing=free_trial_pricing
            )
            # Crear cliente de Stripe
            stripe_customer = stripe.Customer.create(
                email=user.email,
                name=user.username
            )
            # Crear suscripción en Stripe con un periodo de prueba de 7 días
            stripe_subscription = stripe.Subscription.create(
                customer=stripe_customer.id,
                items=[{'price': 'price_1PH8wPJmTTplu4eg3XFPNqWJ'}],
                trial_period_days=7
            )
            # Actualizar la suscripción y el usuario con detalles de Stripe
            subscription.status=stripe_subscription.status
            subscription.stripe_subscription_id = stripe_subscription.id
            subscription.save()
            user.stripe_customer_id = stripe_customer.id
            user.save()
            # Redirigir a la página principal después de un registro exitoso
            return redirect('/')
    else:
         # Si no es una solicitud POST, mostrar el formulario de registro
        form = UserCreationFormWithEmail()
        # Renderizar la página de registro.html con el formulario
    return render(request, 'ConsultoriaApp/Login/registro.html', {'form': form})

def inicios(request):
    """ Maneja el inicio de sesión de los usuarios. Si el usuario ya está autenticado, 
    lo redirige a la página de inicio. En dado caso de que no sea asi, procesa el formulario 
    de inicio de sesión. 
    """
    # Verifica si el usuario ya está autenticado
    if request.user.is_authenticated:
        # Si el usuario está autenticado, renderiza la página de inicio
        return render(request, 'ConsultoriaApp/inicio.html')
    # Verifica si el método de la solicitud es POST
    if request.method == 'POST':
         # Obtiene el nombre de usuario y la contraseña del formulario de inicio de sesión
        username = request.POST['username']
        password = request.POST['password']
        # Autentica al usuario con las credenciales proporcionadas
        user = authenticate(request, username=username, password=password)
        # Si las credenciales son correctas y el usuario existe
        if user is not None:
            # Inicia sesión del usuario
            login(request, user)
            # Redirige a la página de inicio
            return redirect('/')
        else:
            # Si las credenciales son incorrectas, muestra un mensaje de error
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'ConsultoriaApp/Login/index.html', {'form': form, 'msg': msg})
    else:
        # Si el método de la solicitud no es POST, muestra el formulario de inicio de sesión
        form = AuthenticationForm()
        return render(request, 'ConsultoriaApp/Login/index.html', {'form': form})   
    
def cierres(request):
    """ Maneja el cierre de Sesion del usuario. Una vez que el usuario realiza la acción de logout
    se redirige a la página de inicio """
    # Cierra la sesión del usuario
    logout(request)
    # Redirige a la página de inicio
    return redirect('/')   

#Interfaces de los Servicios
def tramites(request):
    """ renderiza el archivo 1tramies.html """
    return render(request, 'ConsultoriaApp/Servicios/1tramites.html')

def auditoria(request):
    """ renderiza el archivo 2Auditoría Preventiva.html """
    return render(request, 'ConsultoriaApp/Servicios/2Auditoría Preventiva.html')

def atencion(request):
    """ renderiza el archivo 3Atención.html """
    return render(request, 'ConsultoriaApp/Servicios/3Atención.html')

def asistencia(request):
    """ renderiza el archivo 4Asistencia.html """
    return render(request, 'ConsultoriaApp/Servicios/4Asistencia.html')

def asistenciaOA(request):
    """ renderiza el archivo 5Asistencia en la Operación Aduanera.html """
    return render(request, 'ConsultoriaApp/Servicios/5Asistencia en la Operación Aduanera.html')

def capacitacion(request):
    """ renderiza el archivo 6Capacitación.html """
    return render(request, 'ConsultoriaApp/Servicios/6Capacitación.html')

def estrategias(request):
    """ renderiza el archivo 7Estrategias Comerciales.html """
    return render(request, 'ConsultoriaApp/Servicios/7Estrategias Comerciales.html')

def serviciosC(request):
    """ renderiza el archivo 8Servicios Corporativos.html """
    return render(request, 'ConsultoriaApp/Servicios/8Servicios Corporativos.html')

def serviciosD(request):
    """ renderiza el archivo 9Servicios Digitales.html """
    return render(request, 'ConsultoriaApp/Servicios/9Servicios Digitales.html')

def alianzas1(request):
    """ renderiza el archivo 10.1Alianzas Estratégicas Submenú1 (Servicios Especializados).html """
    return render(request, 'ConsultoriaApp/Servicios/10.1Alianzas Estratégicas Submenú1 (Servicios Especializados).html')

def alianzas2(request):
    """ renderiza el archivo 10.2Alianzas Estratégicas Submenú2 (Servicios Tercerizados).html """
    return render(request, 'ConsultoriaApp/Servicios/10.2Alianzas Estratégicas Submenú2 (Servicios Tercerizados).html')

def alianzas3(request):
    """ renderiza el archivo 10.3Alianzas Estratégicas Submenú3 (Servicios Tercerizados).html """
    return render(request, 'ConsultoriaApp/Servicios/10.3Alianzas Estratégicas Submenú3 (Servicios Tercerizados).html')

#Funcion para dar permiso de ver el curso si tiene la suscripcion activa

def permission_subscription(user, course_name):
    """
    Verifica si un usuario tiene permiso para acceder a cursos basados en su suscripción.
    """
    # Filtra los cursos por el nombre del curso especificado
    courses = Cursos.objects.filter(course_name=course_name)
    # Filtra las suscripciones activas del usuario
    subscriptions = user.subscriptions.filter(status='active')
    # Si no hay suscripciones activas, devuelve una lista vacía
    if not subscriptions:
        return []
    # Obtiene los precios de las suscripciones activas
    pricing_tiers = [sub.pricing for sub in subscriptions]
    # Filtra los cursos a través del pricing de la suscripción
    return [
        course for course in courses 
        if any(pricing_tier in course.pricing_tiers.all() for pricing_tier in pricing_tiers)
    ]

# Interfaces donde se mostraran los Videos
@login_required
def tramitesvideo(request, *args, **kwargs):
    """
    Se renderiza la página de Tramites.html, mostrando solo 
    los cursos que el usuario tiene permiso de poder acceder. 
    """
    # Obtiene los cursos a los que el usuario tiene permiso de acceder
    courses = permission_subscription(request.user, 'Tramites, Registros y Autorizaciones')
    # Renderiza la página con los cursos filtrados
    return render(request, 'ConsultoriaApp/ServiciosVideos/Tramites.html', {'courses': courses})

@login_required
def auditoriavideo(request, *args, **kwargs):
    """
    Se renderiza la página de 2Auditoria.html, mostrando solo 
    los cursos que el usuario tiene permiso de poder acceder. 
    """
    courses = permission_subscription(request.user, 'Auditoría Preventiva')
    return render(request, 'ConsultoriaApp/ServiciosVideos/2Auditoria.html', {'courses': courses})

@login_required
def atenciónvideo(request, *args, **kwargs):
    """
    Se renderiza la página de 3Atencion.html, mostrando solo 
    los cursos que el usuario tiene permiso de poder acceder. 
    """
    courses = permission_subscription(request.user, 'Atención de Auditorías')
    return render(request, 'ConsultoriaApp/ServiciosVideos/3Atencion.html', {'courses': courses})

@login_required
def asistenciavideo(request, *args, **kwargs):
    """
    Se renderiza la página de 4Asistencia.html, mostrando solo 
    los cursos que el usuario tiene permiso de poder acceder. 
    """
    courses = permission_subscription(request.user, 'Asistencia legal')
    return render(request, 'ConsultoriaApp/ServiciosVideos/4Asistencia.html', {'courses': courses})

@login_required
def aoavideo(request, *args, **kwargs):
    """
    Se renderiza la página de 5AOA.html, mostrando solo 
    los cursos que el usuario tiene permiso de poder acceder. 
    """
    courses = permission_subscription(request.user, 'Asistencia en la operación aduanera')
    return render(request, 'ConsultoriaApp/ServiciosVideos/5AOA.html', {'courses': courses})

@login_required
def capacitacionvideo(request, *args, **kwargs):
    """
    Se renderiza la página de 6CapacitacionV.html, mostrando solo 
    los cursos que el usuario tiene permiso de poder acceder. 
    """
    courses = permission_subscription(request.user, 'Capacitación')
    return render(request, 'ConsultoriaApp/ServiciosVideos/6CapacitacionV.html', {'courses': courses})

@login_required
def estrategiasvideo(request, *args, **kwargs):
    """
    Se renderiza la página de 7Estrategias.html, mostrando solo 
    los cursos que el usuario tiene permiso de poder acceder. 
    """
    courses = permission_subscription(request.user, 'Estrategias comerciales')
    return render(request, 'ConsultoriaApp/ServiciosVideos/7Estrategias.html', {'courses': courses})

@login_required
def servicioscvideo(request, *args, **kwargs):
    """
    Se renderiza la página de 8ServiciosC.html, mostrando solo 
    los cursos que el usuario tiene permiso de poder acceder. 
    """
    courses = permission_subscription(request.user, 'Servicios Corporativas')
    return render(request, 'ConsultoriaApp/ServiciosVideos/8ServiciosC.html', {'courses': courses})

@login_required
def serviciosdvideo(request, *args, **kwargs):
    """
    Se renderiza la página de 9SevicioD.html, mostrando solo 
    los cursos que el usuario tiene permiso de poder acceder. 
    """
    courses = permission_subscription(request.user, 'Servicios digitales')
    return render(request, 'ConsultoriaApp/ServiciosVideos/9ServicioD.html', {'courses': courses})

@login_required
def ae1video(request, *args, **kwargs):
    """
    Se renderiza la página de 10.1AE1.html, mostrando solo 
    los cursos que el usuario tiene permiso de poder acceder. 
    """
    courses = permission_subscription(request.user, 'Alianzas Estrategicas')
    return render(request, 'ConsultoriaApp/ServiciosVideos/10.1AE1.html', {'courses': courses})

@login_required
def ae2video(request, *args, **kwargs):
    """
    Se renderiza la página de 10.2AE2.html, mostrando solo 
    los cursos que el usuario tiene permiso de poder acceder. 
    """
    courses = permission_subscription(request.user, 'Alianzas Estrategicas2')
    return render(request, 'ConsultoriaApp/ServiciosVideos/10.2AE2.html', {'courses': courses})

@login_required
def ae3video(request, *args, **kwargs):
    """
    Se renderiza la página de 10.3AE3.html, mostrando solo 
    los cursos que el usuario tiene permiso de poder acceder. 
    """
    courses = permission_subscription(request.user, 'Alianzas Estrategicas3')
    return render(request, 'ConsultoriaApp/ServiciosVideos/10.3AE3.html', {'courses': courses})