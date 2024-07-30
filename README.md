# Sistema de recomendacion de peliculas

## Descripcion

Este proyecto implementaun sitema de recomendacion urilizando tecnicas de Machine Learning . El objetivo es recomendar peliculas en base a un pelicula ya vista o visitada , en la funcion /recomendacion/ dentro del archivo main.py se define comoparametro 'titulo_pelicula' y como retorno las recomendaciones de las 5 peliculas mas parecidas a esa.

## Contenido archivos

- credits.pkl : Este archivo es la data ya limpia y transformada del archivo originas credits.pkl .Este archivo contiene como informacion util el nombre de los actores y directores  en cada peliculas 
- peliculas.pkl : Este archivo es la data ya limpia y transformada del archivo original movies.csv . Este archivo contiene informacion de las peliculas como son:
 * Nombre depelicula
 * Costo
 * Retorno
 * Compañia
 * etc 
 En el archivo Diccionario de Datos.xlsx viene especificado cada una de las columnas
 - ETL: Contiene el codigo de la extraccion , transformacion y caarga de los datos. 
 - Modelo_Recomendacion_EDA : Es el archivo que contiene el codigo en dodne se visualiza la informacionmediante graficas y ademas contiene le codigo del modelo de recomendacion.
 - main.py : Es el archivo que contiene las funciones y que es ejecutado desde render
  - requirements.txt :Contiene las bibliotecas utilizadas

# Render API
- https://ml-sistema-recomendacion-peliculas.onrender.com


### Requisitos

- Python 3.9.11
- Bibliotecas especificadas en `requirements.txt`


