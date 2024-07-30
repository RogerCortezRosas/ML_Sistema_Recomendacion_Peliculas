

from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = FastAPI()


# Leer el DataFrame desde el archivo pickle
try:
    data_movies = pd.read_pickle('peliculas.pkl')
except FileNotFoundError:
    raise HTTPException(status_code=404, detail="Archivo de datos no encontrado")

# Leer el DataFrame desde el archivo pickle
try:
    data_credits = pd.read_pickle('credits.pkl')
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
  return str(cantidad_filmaciones) + " es la cantidad de peliculas que fueron estrenadas el mes de "+str(Mes)

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
    cantidad_filmaciones = data_movies[data_movies['release_date'].dt.day == dia].shape[0]
    return str(cantidad_filmaciones) + " es la cantidad de peliculas que fueron estrenadas el dia "+ str(dia)

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

@app.get("/actors/{name_actor}")
def get_actor( name_actor ):
    """ Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, la cantidad de películas que en las que ha participado y el promedio de retorno."""

    val_return = []
    count = 0
    bandera=False

    for index,row in data_credits.iterrows():
        
            lista_actors = row["Actors/Actress"]
            

            if name_actor in lista_actors:
                retun = row["return"]
                val_return.append(retun)
                count +=1
                bandera=True
    
    if bandera == False:
         raise HTTPException(status_code=400, detail="Error al ingresar el nombre del director o actriz o no se encuntra dentro de lista de actores o actrices")

    suma_return = round(sum(val_return) ,3) 
    promedio = round(suma_return / len(val_return) ,3)     

    return "El actor " + name_actor + " ha participado en " + str(count) + " peliculas , el mismo ha consegido un retorno de "+str(suma_return)+" con un promedio de "+str(promedio)
                
  
@app.get("/director/{nombre_director}") 
def get_director( nombre_director ): 
    """Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno.
      Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma"""
    
    val_return = []
    count = 0
    name = []
    fecha = []
    costo = []
    ganancia = []
    bandera = False

  

    for index,row in data_credits.iterrows():
        
            lista_director = row["Director"]
            

            if nombre_director in lista_director:
                retun = row["return"]
                name.append(row["title"])
                fecha.append(row["release_year"])
                costo.append(row["budget"])
                ganancia.append(row["revenue"])
                val_return.append(retun)
                count +=1
                bandera = True
    


    suma_return = round(sum(val_return) ,3) 
    
    if bandera == False:
         raise HTTPException(status_code=400, detail="Error al ingresar el nombre del director  o no se encuntra dentro de lista de directores")
    
    lista_dict = []
    
    
    # Iterar sobre las claves y los valores combinados
    for name,fecha,costo,ganancia in zip(name,fecha,costo,ganancia):
      dicc = {
           "Director":nombre_director,
           "Retorno":suma_return,
           "Numero pelis":count,
           "Titulo Pelicula":name,
           "Fecha lanzamiento":fecha,
           "Costo":costo,
           "Ganancia":ganancia
         
            }
      lista_dict.append(dicc)

    return    lista_dict


@app.get("/recomendacion/{titulo_pelicula}") 
def recomendar_peliculas_por_puntuacion(titulo_pelicula):
    """Función para recomendar películas basadas en vecinos mas cercanos"""
    
    peliculas = data_movies['title'].tolist()

    if titulo_pelicula not in peliculas:
        raise HTTPException(status_code=400, detail="Error al ingresar el nombre de la pelicula  o no se encuentra dentro de lista de peliculas de esta plataforma")

    # Vectorizar las descripciones usando TF-IDF
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data_movies['overview'])

    # Obtener el índice de la película dada
    idx = data_movies[data_movies['title'] == titulo_pelicula].index[0]


    # Calcular la similitud del coseno entre la película dada y todas las demás
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

   # Ordenar las películas por la similitud en orden descendente
    sim_scores = list(enumerate(cosine_sim))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Seleccionar las más cercanas (excluyendo la propia película)
    sim_scores = sim_scores[1:5+1]
    
    # Obtener los índices de las películas recomendadas
    movie_indices = [i[0] for i in sim_scores]

    lista_pelis = data_movies['title'].iloc[movie_indices].tolist()


    return "Te recomendamos ver  las siguientes peliculas",lista_pelis
