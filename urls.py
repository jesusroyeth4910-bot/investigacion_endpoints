from django.urls import path
from .views import ProyectoView

urlpatterns = [
    path("proyectos/", ProyectoView.as_view()),           # GET (lista) y POST (crear)
    path("proyectos/<int:pk>/", ProyectoView.as_view()),  # GET (uno), PUT y DELETE
]

# En el urls.py PRINCIPAL del proyecto agrega:
# from django.urls import path, include
# urlpatterns = [
#     ...
#     path("api/", include("nombre_de_tu_app.urls")),
# ]
