from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "votes"  # Cambiado para coincidir con la colección en Firebase

    def get(self, request):

      # Referencia a la colección
      ref = db.reference(f'{self.collection_name}')

      # get: Obtiene todos los elementos de la colección
      data = ref.get()

      # Si no hay datos, retorna un arreglo vacío
      if data is None:
          return Response([], status=status.HTTP_200_OK)

      # Convierte el objeto de Firebase a un array para una respuesta más legible
      # Incluye el ID de Firebase en cada elemento
      result = []
      for key, value in data.items():
          item = value.copy()
          item['id'] = key  # Agrega el ID de Firebase al objeto
          result.append(item)

      # Devuelve un arreglo JSON
      return Response(result, status=status.HTTP_200_OK)
    
    def post(self, request):

      data = request.data

      # Referencia a la colección
      ref = db.reference(f'{self.collection_name}')

      current_time  = datetime.now()
      custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
      data.update({"timestamp": custom_format })

      # push: Guarda el objeto en la colección
      new_resource = ref.push(data)

      # Devuelve el id del objeto guardado
      return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
