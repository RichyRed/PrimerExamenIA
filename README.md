# AutoBikeDetect: Tu Compañero de Identificación Vehicular 🚗🏍️🚴‍♂️

## Descripción 
AutoBikeDetect es la aplicación líder en tecnología de visión por computadora que permite identificar y clasificar vehículos de manera precisa. Con AutoBikeDetect, podrás reconocer y seguir automóviles, motocicletas y bicicletas con rapidez y precisión, abriendo nuevas posibilidades para la seguridad vial y la gestión del tráfico.

## Propósito
AutoBikeDetect tiene como objetivo revolucionar la gestión del tráfico y la seguridad vial mediante la entrega de una solución integral para la identificación precisa de automóviles, motocicletas y bicicletas.

## Cómo Ejecutar el Proyecto
- Clona el repositorio en tu máquina local.
- Ejecuta el script "predictor.py" para inicializar el modelo de detección de vehículos.
- Luego, ejecuta el script "app.py" para iniciar la API.
- Accede a la documentación en "/docs" para explorar y probar los endpoints.

## Endpoints Utilizados
La API de CarID tiene tres endpoints principales:

### GET /status
Este endpoint proporciona información crucial sobre el estado del servicio de detección de vehículos.

### POST /predict
Este endpoint acepta una imagen y devuelve la misma imagen con la predicción de la marca del vehículo, la confianza de la predicción y el tiempo de ejecución.

### GET /reports
Este endpoint guarda todas las predicciones realizadas a través del endpoint POST /predict y permite descargarlas como un archivo CSV con información relevante.

### ¡Gracias por elegir AutoBikeDetect! Si tienes alguna pregunta o comentario, no dudes en ponerte en contacto con nosotros.

## Autor
- **Richard Alejandro Rojas Aguilar**
- **55077**


