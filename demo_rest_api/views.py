from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response(
                {"error": "Los campos 'name' y 'email' son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )
        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)
        return Response(
            {
                "message": "Datos guardados correctamente.",
                "data": data
            },
            status=status.HTTP_201_CREATED
        )

class DemoRestApiItem(APIView):
    """
    Vista para operaciones sobre un solo elemento identificado por 'id'
    """

    def get(self, request, id=None):
        if not id:
            return Response({"error": "El parámetro 'id' es obligatorio en la URL."}, status=status.HTTP_400_BAD_REQUEST)
        for item in data_list:
            if item['id'] == id:
                return Response(item, status=status.HTTP_200_OK)
        return Response({"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id=None):
        data = request.data
        if not id:
            return Response({"error": "El parámetro 'id' es obligatorio en la URL."}, status=status.HTTP_400_BAD_REQUEST)
        # Buscar el elemento
        for idx, item in enumerate(data_list):
            if item['id'] == id:
                # Reemplazar todos los campos excepto el id
                new_item = {
                    'id': id,
                    'name': data.get('name'),
                    'email': data.get('email'),
                    'is_active': data.get('is_active', True)
                }
                data_list[idx] = new_item
                return Response({"message": "Elemento reemplazado correctamente.", "data": new_item}, status=status.HTTP_200_OK)
        return Response({"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id=None):
        data = request.data
        if not id:
            return Response({"error": "El parámetro 'id' es obligatorio en la URL."}, status=status.HTTP_400_BAD_REQUEST)
        for item in data_list:
            if item['id'] == id:
                # Actualizar solo los campos enviados
                for key in ['name', 'email', 'is_active']:
                    if key in data:
                        item[key] = data[key]
                return Response({"message": "Elemento actualizado parcialmente.", "data": item}, status=status.HTTP_200_OK)
        return Response({"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None):
        if not id:
            return Response({"error": "El parámetro 'id' es obligatorio en la URL."}, status=status.HTTP_400_BAD_REQUEST)
        for item in data_list:
            if item['id'] == id:
                item['is_active'] = False
                return Response({"message": "Elemento eliminado lógicamente."}, status=status.HTTP_200_OK)
        return Response({"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)