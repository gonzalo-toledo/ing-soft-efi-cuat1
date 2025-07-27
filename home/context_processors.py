from home.forms import LoginForm, RegisterForm
from pasajeros.forms import PasajeroForm

def login_form(request):
    """
    Context processor para agregar el formulario de inicio de sesión al contexto de las plantillas.
    Este formulario se puede utilizar en cualquier plantilla que lo necesite, como por ejemplo en la barra de navegación.
    Se utiliza para mostrar un modal de inicio.
    """
    return {
        'login_form': LoginForm()
    }

def register_form(request):
    """
    Context processor para agregar el formulario de registro al contexto de las plantillas.
    Este formulario se puede utilizar en cualquier plantilla que lo necesite, como por ejemplo en la barra de navegación.
    Se utiliza para mostrar un modal de registro de usuario.
    """
    return {
        'register_form': RegisterForm()
    }
    

def pasajero_form(request):
    """
    Context processor para agregar el formulario de pasajero al contexto de las plantillas.
    Este formulario se puede utilizar en cualquier plantilla que lo necesite, como por ejemplo en la barra de navegación.
    Se utiliza para mostrar un modal de registro de pasajero.
    """
    return {
        'pasajero_form': PasajeroForm()
    }
