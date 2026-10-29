# LIBRERIAS
import json
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Proyecto


class ProyectoView(View):

    def _parse_json_body(self, request):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None, JsonResponse({"error": "JSON inválido"}, status=400)

        if not isinstance(data, dict):
            return None, JsonResponse(
                {"error": "El cuerpo JSON debe ser un objeto"}, status=400
            )

        return data, None

    def _validate_data(self, data, partial=False):
        if not partial and "nombre" not in data:
            return JsonResponse(
                {"error": "El campo 'nombre' es obligatorio"}, status=400
            )

        if "nombre" in data and (
            not isinstance(data["nombre"], str) or not data["nombre"].strip()
        ):
            return JsonResponse(
                {"error": "El campo 'nombre' debe ser un texto no vacío"}, status=400
            )

        if "nombre" in data and len(data["nombre"].strip()) > 100:
            return JsonResponse(
                {"error": "El campo 'nombre' no puede superar los 100 caracteres"},
                status=400,
            )

        if "descripcion" in data and not isinstance(data["descripcion"], str):
            return JsonResponse(
                {"error": "El campo 'descripcion' debe ser un texto"}, status=400
            )

        if partial and not any(
            field in data for field in ("nombre", "descripcion")
        ):
            return JsonResponse(
                {"error": "Debe enviar 'nombre' o 'descripcion' para actualizar"},
                status=400,
            )

        return None

    def get(self, request, pk=None):
        if pk is not None:
            p = get_object_or_404(Proyecto, pk=pk)
            return JsonResponse({
                "id": p.id,
                "nombre": p.nombre,
                "descripcion": p.descripcion
            })
        proyectos = list(
            Proyecto.objects.values("id", "nombre", "descripcion")
        )
        return JsonResponse(proyectos, safe=False)

    def post(self, request):
        data, error = self._parse_json_body(request)
        if error:
            return error

        error = self._validate_data(data)
        if error:
            return error

        p = Proyecto.objects.create(
            nombre=data["nombre"].strip(),
            descripcion=data.get("descripcion", "")
        )
        return JsonResponse({"mensaje": "Creado", "id": p.id}, status=201)

    def put(self, request, pk):
        data, error = self._parse_json_body(request)
        if error:
            return error

        error = self._validate_data(data, partial=True)
        if error:
            return error

        p = get_object_or_404(Proyecto, pk=pk)
        if "nombre" in data:
            p.nombre = data["nombre"].strip()
        if "descripcion" in data:
            p.descripcion = data["descripcion"]
        p.save()
        return JsonResponse({"mensaje": "Actualizado"})

    def delete(self, request, pk):
        p = get_object_or_404(Proyecto, pk=pk)
        p.delete()
        return JsonResponse({"mensaje": "Eliminado"})
