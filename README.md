# AutoBikeDetect: Tu Compañero de Identificación Vehicular 🚗🏍️🚴‍♂️

## Descripción 
La aplicación del momento que utiliza tecnología de visión por computadora para identificar y clasificar vehículos. Con AutoBikeDetect, podrás reconocer y seguir autos, motos y bicicletas con precisión y rapidez, abriendo un nuevo mundo de posibilidades para la seguridad vial y la gestión del tráfico.

## Propósito
AutoBikeDetect se propone revolucionar la gestión del tráfico y la seguridad vial al ofrecer una solución integral para la identificación precisa de autos, motos y bicicletas.

## Para correrlo
  * Primero debemos clonar el proyecto.
  * Despues debemos correr el "predictor.py"
  * Despues el "app.py"
  * Cuando la aplicacion se lance debemos ir a la ruta "/docs" y listo

## Endpoints utilizados
La API de CarID tiene tres endpoints principales:

## GET /status
Este endpoint devuelve información importante sobre el estado del servicio de detección de autos.

## POST /predict
Este endpoint recibe una imagen y devuelve la imagen con la predicción de a qué marca pertenece, la confianza de la predicción y el tiempo de ejecución.

## GET /reports
Este endpoint guarda todas las predicciones realizadas a través del endpoint POST /predict y permite descargarlas como un archivo CSV con información relevante.

## Autor
* Richard Alejandro Rojas Aguilar
* 55077


