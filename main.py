

from fastapi import FastAPI, HTTPException
import pandas as pd


app = FastAPI()


# Leer el DataFrame desde el archivo pickle
try:
    data_movies = pd.read_pickle('peliculas.pkl')
except FileNotFoundError:
    raise HTTPException(status_code=404, detail="Archivo de datos no encontrado")


@app.get("/cantidad_filmaciones_mes/{Mes}")
def cantidad_filmaciones_mes(Mes:str):
  """
  Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas
  en el mes consultado en la totalidad del dataset.

  """
  Mes = Mes.lower()
  mes_dict = {
        'enero':1,
        'febrero':2,
        'marzo':3,
        'abril':4,
        'mayo':5,
        'junio':6,
        'julio':7,
        'agosto':8,
        'septiembre':9,
        'octubre':10,
        'noviembre':11,
        'diciembre':12
    }

    
  if Mes not in mes_dict:
        raise HTTPException(status_code=400, detail="Error al ingresar el nombre del mes")



    # obtenemos el valor numeroo del mes
  mes = mes_dict[Mes]
    #Obtenemos la catidad de peliculas que se lanzaron en el mes
  cantidad_filmaciones = data_movies[data_movies['release_date'].dt.month == mes].shape[0]
  return cantidad_filmaciones , "cantidad de peliculas que fueron estrenadas el mes de ",Mes

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia):

    """
    Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas
    en el dia consultado en la totalidad del dataset.

    """
    dia = dia.lower()
    dia_dict = {
      'uno':1,'dos':2,'tres':3,'cuatro':4,'cinco':5,'seis':6,'siete':7,'ocho':8,'nueve':9,'diez':10,
      'once':11,'doce':12,'trece':13,'catorce':14,'quince':15,'dieciseis':16,'diecisiete':17,'dieciocho':18,
      'diecinueve':19,'veinte':20,'veitiuno':21,'veitidos':22,'veititres':23,'veiticuatro':24,'veiticinco':25,
      'veintiseis':26,'veintisiete':27,'veintiocho':28,'veintinueve':29,'treinta':30,'treinta y uno':31,

  }
    if dia not in dia_dict:
        raise HTTPException(status_code=400, detail="Error al ingresar el dia ")
    
     # obtenemos el valor numeroo del mes
    dia = dia_dict[dia]
    #Obtenemos la catidad de peliculas que se lanzaron en el mes
    cantidad_filmaciones = data_movies[data_movies['release_date'].dt.month == dia].shape[0]
    return cantidad_filmaciones , "cantidad de peliculas que fueron estrenadas el dia ",dia

@app.get("/score_film/{titulo}")
def score_titulo( titulo ): 
    """Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno 
    y el score."""

    titulos_pelis = data_movies["title"].unique()

    if titulo  in titulos_pelis:
        
        score = data_movies.loc[data_movies["title"] == titulo ,"popularity"]
        estreno = data_movies.loc[data_movies["title"] == titulo ,"release_year"]
        estreno = int(estreno.iloc[0])
        score = float ( score.iloc[0])
    else:
        raise HTTPException(status_code=400, detail="Error al ingresar el titulo de la pelicula ")

    return "La pelicula " + str(titulo)+ " fue estrenada da en el año "+ str(estreno) +" con un score/popularidad de "+str(score)

@app.get("/votes_film/{titulo}")
def votos_titulo( titulo ): 

    """Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio 
    de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, se regresa un mensaje avisando que no cumple
      esta condición y que por ende, no se devuelve ningun valor."""
    
    titulos_pelis = data_movies["title"].unique()

    if titulo  in titulos_pelis:

        vote_count = data_movies.loc[data_movies["title"] == titulo ,"vote_count"]
        vote_average = data_movies.loc[data_movies["title"] == titulo ,"vote_average"]
        estreno = data_movies.loc[data_movies["title"] == titulo ,"release_year"]
        
        estreno = int(estreno.iloc[0])
        vote_count = float(vote_count.iloc[0])
        vote_average = float(vote_average.iloc[0])

        if vote_count >= 2000:
        
            return "La pelicula " + titulo + " fue estrenada en el año "+ str(estreno) + " , la misma cuenta con un total de  "+ str(vote_count)+" valoraciones y con un promedio de "+str(vote_average)
        else :
            print("Esta pelicula no cuenta con la valoracion necesaria no a sido de agrado para el publico")

        
    else:
        

        raise HTTPException(status_code=400, detail="Error al ingresar el nombre de la pelicula o no se encuntra dentro de lista de peliculas de eta plataforma")

    