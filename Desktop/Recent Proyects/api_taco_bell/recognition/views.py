from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import librosa
import numpy as np
import os

def detect_bell_sound(audio_file):
    # Leer el archivo de audio
    y, sr = librosa.load(audio_file)

    # Calcular el espectrograma
    S = np.abs(librosa.stft(y))

    # Extraer características relevantes del espectrograma (por ejemplo, picos espectrales)
    # En este ejemplo, simplemente sumaremos las intensidades de frecuencia para todas las frecuencias
    intensidades_frecuencia = np.sum(S, axis=1)

    # Calcular una medida de "campana-ness" (simplemente a modo de ejemplo)
    umbral_campana = 1000  # Define un umbral de intensidad arbitrario
    if np.max(intensidades_frecuencia) > umbral_campana:
        return "¡Se detectó el sonido de una campana!"
    else:
        return "No se detectó el sonido de una campana."


@api_view(['POST'])
def index(request):
    try:
        # Verificar si el archivo de audio fue enviado en la solicitud
        if 'audio_file' in request.FILES:
            # Obtener el archivo de audio enviado en la solicitud
            audio_file = request.FILES['audio_file']
            # Guardar el archivo de audio temporalmente
            with open('temp_audio.wav', 'wb+') as temp_audio:
                for chunk in audio_file.chunks():
                    temp_audio.write(chunk)
            # Realizar la detección de sonido de campana
            resultado = detect_bell_sound('temp_audio.wav')
            # Eliminar el archivo de audio temporal
            os.remove('temp_audio.wav')
            # Crear la respuesta de la API
            content = {
                'data': {
                    'code': 200,
                    'msg': resultado,
                }
            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            # Si no se proporcionó un archivo de audio en la solicitud
            content = {
                'data': {
                    'code': 400,
                    'msg': 'No se proporcionó un archivo de audio en la solicitud.'
                }
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Manejar cualquier error que pueda ocurrir
        print(e)
        content = {
            'data': {
                'code': 500,
                'msg': 'Se produjo un error al procesar la solicitud.'
            }
        }
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)