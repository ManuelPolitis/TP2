import csv
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import modulo_lyrics

def cls() -> None:
    """Funcion para limpiar la consola, el condicional hace que sirva tanto para linux como para windows"""
    os.system('cls' if os.name == 'nt' else 'clear')


def autenticar():
    """Precondiciones: Apertura hara el request de las tokens a la api, generando una autentificacion, pero antes verificara si ya existe una que no este expirada. En el caso que este expirada usara la refresh token. Con la token
    obtendremos los permisos para acceder a los datos que necesitamos del usuario a traves de la api.
    Postcondiciones: La funcion apertura retornara las credenciales que nos entrego la api para poder empezara utilizar sus funciones"""

    credentials = None

    # token.pickle guarda las credenciales de logins anteriores

    if os.path.exists('token.pickle'):
        print('Cargando credenciales desde el archivo...')
        with open('token.pickle', 'rb') as token: #Read bites ya que token.pickle es un archivo tipo bite
            credentials = pickle.load(token)


    # Si no hay credenciales válidas disponibles, entonces o refresco el token o vuelvo a loginear.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refrescando token de acceso...')
            credentials.refresh(Request())
        else:
            print('Obteniendo nuevos tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json',
                scopes=["https://www.googleapis.com/auth/youtube",
              "https://www.googleapis.com/auth/youtube.force-ssl",
              "https://www.googleapis.com/auth/youtube.readonly",
              "https://www.googleapis.com/auth/youtubepartner",
              "https://www.googleapis.com/auth/youtubepartner-channel-audit"]
            )

            flow.run_local_server(port=8080, prompt='consent',
                                  authorization_prompt_message='')
            credentials = flow.credentials

            # Guardo las credenciales para la proxima
            with open('token.pickle', 'wb') as f:
                print('Guardando las credenciales para proximo uso...')
                pickle.dump(credentials, f)

    return credentials


def nombre_playlists()->list:
    """Precondiciones: Nombre playlist hara un request a la api sobre los datos de las playlist de los usuarios. Luego mediante bucles o recorrido del diccionario que llega de la response
    obtendremos los datos del nombre del canal y las playlists"""


    credentials = autenticar() #Me fijo si tengo credenciales sin vencer y sino creo nuevas.

    youtube = build('youtube', 'v3', credentials=credentials)

    request = youtube.playlists().list(part="snippet",mine=True, maxResults=50) #Genero el request q con el part=snippet me dara toda la informacion que necesito. mine=true hara que busque en el canal de la persona que se autentico
    response = request.execute()

    cant_de_playlists:int = len(response["items"]) # Obtengo la cantidad de playlists tomando cuantos diccionarios hay dentro de items, que son las playlists

    nombre_de_playlists:list=[]

    nombre_de_canal:str = response["items"][0]["snippet"]["channelTitle"] # Dentro del diccionario response, obtengo le nombre del canal recorriendo por sus keys

    for i in range (0,cant_de_playlists): #Recorro todas las playlists obtenidas como diccionarios para sacar solamente los titulos de las mismas
        nombre_de_playlists.append((response["items"][i]["snippet"]["title"]))

    print("Plataforma: Youtube")
    print(f"Usuario: {nombre_de_canal}")
    print(f"Nombres de las playlist es: {nombre_de_playlists}")

    return nombre_de_playlists


def crear_playlists():
    """Precondiciones: Crea una nueva playlist en la cuenta del usuario preguntandole por el titulo, descripcion de la playlist
    y si quiere que la misma sea privada o publica."""

    credentials = autenticar() #Me fijo si tengo credenciales sin vencer y sino creo nuevas.

    youtube = build('youtube', 'v3', credentials=credentials)

    cls()

    nombre_playlist:str = input('Inserte el nombre de la nueva playlist que desea crear: ')

    descripcion_playlist:str = input('Inserte la descripcion de la playlist: ')

    public_o_private:str = input('Ingrese "private" si desea que su playlist sea privada. Si desea que sea publica ingrese "public": ')

    while public_o_private != 'private' and public_o_private != 'public':
        print('Valor ingresado no valido!. Pruebe otra vez.')
        public_o_private: str = input('Ingrese "private" si desea que su playlist sea privada. Si desea que sea publica ingrese "public": ')

    playlists_insert_response = youtube.playlists().insert( #Inserto la playlist con los datos dados por el usuario
        part="snippet,status",
        body=dict(
            snippet=dict(
                title=nombre_playlist,
                description=descripcion_playlist
            ),
            status=dict(
                privacyStatus=public_o_private
            )
        )
    ).execute()

    cls()

    print('Playlist creada con exito!')
    print(f'Nombre de la playlist: {nombre_playlist}\n'
          f'Descripcion de la playlist: {descripcion_playlist}\n'
          f'{public_o_private} playlist\n'
          f'Link nueva playlist: https://www.youtube.com/playlist?list={playlists_insert_response["id"]}')


def playlist_csv():
    """Imprime todas las playlists del usuario y le pide que elija una para luego crear un archivo .csv con los datos de la playlist elegida."""
    credentials = autenticar()  # Me fijo si tengo credenciales sin vencer y sino creo nuevas.

    youtube = build('youtube', 'v3', credentials=credentials)

    request = youtube.playlists().list(part="snippet",mine=True,maxResults=50)  # Genero el request que con el part=snippet me dara toda la informacion que necesito. mine=true hara que busque en el canal de la persona que se autentico
    response = request.execute()

    cls()

    cant_de_playlists:int = int(len(response["items"])) # Obtengo la cantidad de playlists tomando cuantos diccionarios hay dentro de items, que son las playlists

    playlistsIds:list = []

    nombre_de_playlists:list=[]

    for i in range (0,cant_de_playlists): #Recorro todas las playlists obtenidas como diccionarios para sacar solamente los titulos de las mismas
        nombre_de_playlists.append((response["items"][i]["snippet"]["title"]))

    for i in range (0,cant_de_playlists): #Recorro todas las playlists obtenidas como diccionarios para sacar solamente los id de las mismas
        playlistsIds.append((response["items"][i]["id"]))

    diccionario_playlists:dict = {}

    for i in range(0,cant_de_playlists):
        diccionario_playlists[i]=nombre_de_playlists[i]

    print("Tus Playlists:")
    for indice,nombre in diccionario_playlists.items():
        print(f"{indice+1}) {nombre}")

    is_Int:bool = False
    in_Range:bool = False

    while not is_Int or not in_Range:
        try:
            numero_de_playlist: int = input('Ingrese el indice de playlist de la que desea obtener un archivo csv: ')
            numero_de_playlist:int = int(numero_de_playlist)
            is_Int = True

        except ValueError:
            print('Valor no numerico!')
            is_Int = False

        if is_Int:
            if numero_de_playlist > cant_de_playlists or numero_de_playlist < 0:
                print('El valor ingresado no esta dentro del rango posible.')
            else:
                in_Range = True

    cls()

    numero_de_playlist-=1

    print(f'Eligio la playlist: {diccionario_playlists[numero_de_playlist]}')
    idPlaylistElegida:str = playlistsIds[numero_de_playlist]
    print(f'Link de la Playlist: https://www.youtube.com/playlist?list={idPlaylistElegida}')

    request = youtube.playlistItems().list(part="snippet", maxResults=50,playlistId=idPlaylistElegida)
    response = request.execute()


    with open(f'playlist {diccionario_playlists[numero_de_playlist]}.csv','w',newline='',encoding='UTF-8') as archivo_csv:
        csv_writer = csv.writer(archivo_csv,delimiter =',',quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow((
            'Fecha de publicacion',
            'ID del canal autenticado',
            'Titulo',
            'Descripcion del video',
            'ID de la playlist',
            'ID del video',
            'Nombre del canal',
            'ID del canal',
            "Tipo de elemento",
            "E-tag"))

        print('')
        print('Creando archivo CSV...')
        for i in range(0, len(response['items'])):
            try:
                csv_writer.writerow(
                    (response["items"][i]["snippet"]["publishedAt"],
                     response["items"][i]["snippet"]["channelId"],
                     response["items"][i]["snippet"]["title"],
                     response["items"][i]["snippet"]["description"],
                     response["items"][i]["snippet"]["playlistId"],
                     response["items"][i]["snippet"]["resourceId"]["videoId"],
                     response["items"][i]["snippet"]["videoOwnerChannelTitle"],
                     response["items"][i]["snippet"]["videoOwnerChannelId"],
                     response["items"][i]["kind"],
                     response["items"][i]["etag"]))

            except KeyError:
                print('')

        print(f'Archivo creado exitosamente! Nombre del archivo: playlist {diccionario_playlists[numero_de_playlist]}.csv')



def agregar_cancion():
    """Pide al usuario el nombre y artista de la cancion que quiere agregar a su playlist.
    Luego hace una busqueda con esas palabras clave y presenta los primeros 3 resultados que se presentan.
    Después de elegir la cancion deseada consulta al usuario si quere agregar esa cancion a una playlist suya o no.
    En el caso que sí, pregunta en cuál desea agregarla.
    Indefinidamente si agrega a su playlist o no, se imprime la letra de la cancion al final de la ejecucion."""

    credentials = autenticar()  # Me fijo si tengo credenciales sin vencer y sino creo nuevas.

    youtube = build('youtube', 'v3', credentials=credentials)

    indice_a_agregar: int = 0

    while indice_a_agregar == 0:

        cls()
        nombre_cancion_a_buscar: str = input('Ingrese el nombre de la cancion: ')
        artista_cancion_a_buscar: str = input("Ingrese el artista de la cancion: ")

        cancion_a_buscar:str = nombre_cancion_a_buscar + " " + artista_cancion_a_buscar
        cls()

        request = youtube.search().list(part='snippet',maxResults=3,type='video',q=cancion_a_buscar) #Valor predeterminado de order es SEARCH_SORT_RELEVANCE.
        response = request.execute()

        diccionario_resultados:dict = {}

        print("Resultados:")

        for i in range(0, len(response['items'])):
            print('----------------------------------------------------------------------------------------------------------')
            print(f'{i+1}) {response["items"][i]["snippet"]["title"]}')
            print(response['items'][i]['snippet']['description'])
            diccionario_resultados[i+1] = response["items"][i]["id"]["videoId"]

        print('----------------------------------------------------------------------------------------------------------\n')

        is_Int: bool = False
        in_Range: bool = False

        while not is_Int or not in_Range:
            try:
                indice_a_agregar: int = int(input('Ingrese de las opciones (1/2/3) cual desea agregar a su playlist. Si su opcion no esta dentro de sus opciones ingrese (0): '))
                is_Int = True

            except ValueError:
                print('Valor no numerico!')
                is_Int = False

            if is_Int:

                if indice_a_agregar > len(response['items']) or indice_a_agregar < 0:
                    print('El valor ingresado no esta dentro del rango posible.')
                else:
                    in_Range = True

    print("")
    confirmacion_agregar:str = input("¿Desea agregar esta cancion a una de sus playlists? (S/N): ")

    while confirmacion_agregar.lower() != "s" and confirmacion_agregar.lower() != "n":
        confirmacion_agregar:str = input("Valor ingresado invalido. ¿Desea agregar esta cancion a una de sus playlists? (S/N): ")

    if confirmacion_agregar.lower() == "s":
        request = youtube.playlists().list(part="snippet", mine=True,maxResults=50)  # Genero el request q con el part=snippet me dara toda la informacion que necesito. mine=true hara que busque en el canal de la persona que se autentico
        response = request.execute()

        cant_de_playlists: int = len(response["items"])  # Obtengo la cantidad de playlists tomando cuantos diccionarios hay dentro de items, que son las playlists

        nombre_de_playlists: dict = {}
        id_de_playlists:dict = {}

        for i in range(0,cant_de_playlists):  # Recorro todas las playlists obtenidas como diccionarios para sacar solamente los titulos de las mismas
            nombre_de_playlists[i+1]=response["items"][i]["snippet"]["title"]
            id_de_playlists[i+1] = response["items"][i]["id"]

        cls()

        print("Tus Playlists:\n")
        for indice,nombre in nombre_de_playlists.items():
            print(f"{indice}) {nombre}")

        print("")
        is_Int: bool = False
        in_Range: bool = False

        while not is_Int or not in_Range:
            try:
                playlist_a_modificar: int = input("Elija de la lista de playlists, en cual quiere agregar su cancion (1/2/3/4/...): ") # Puedo crear funcion validar
                playlist_a_modificar: int = int(playlist_a_modificar)
                is_Int = True

            except ValueError:
                print('Valor no numerico!')
                is_Int = False

            if is_Int:
                if playlist_a_modificar > cant_de_playlists or playlist_a_modificar < 0:
                    print('El valor ingresado no esta dentro del rango posible.')
                else:
                    in_Range = True

        video_ID:str = diccionario_resultados[indice_a_agregar]
        playlist_ID:str = id_de_playlists[playlist_a_modificar]

        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_ID,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_ID
                    }
                }
            }
        )
        cls()
        print("Video agregado con exito!")
        response = request.execute()

    cls()

    print(modulo_lyrics.letra_cancion(nombre_cancion_a_buscar,artista_cancion_a_buscar))

def funcion_letras()->list:

    credentials = autenticar()  # Me fijo si tengo credenciales sin vencer y sino creo nuevas.

    youtube = build('youtube', 'v3', credentials=credentials)

    request = youtube.playlists().list(part="snippet", mine=True,
                                       maxResults=50)  # Genero el request q con el part=snippet me dara toda la informacion que necesito. mine=true hara que busque en el canal de la persona que se autentico
    response = request.execute()

    cant_de_playlists: int = len(response[
                                     "items"])  # Obtengo la cantidad de playlists tomando cuantos diccionarios hay dentro de items, que son las playlists

    nombre_de_playlists: dict = {}
    id_de_playlists: dict = {}

    for i in range(0,
                   cant_de_playlists):  # Recorro todas las playlists obtenidas como diccionarios para sacar solamente los titulos de las mismas
        nombre_de_playlists[i + 1] = response["items"][i]["snippet"]["title"]
        id_de_playlists[i + 1] = response["items"][i]["id"]

    cls()

    print("Tus Playlists:\n")
    for indice, nombre in nombre_de_playlists.items():
        print(f"{indice}) {nombre}")

    print("")
    is_Int: bool = False
    in_Range: bool = False

    while not is_Int or not in_Range:
        try:
            playlist_a_modificar: int = input(
                "Elija de la lista de playlists, cual quiere analizar sus letras (1/2/3/4/...): ")  # Puedo crear funcion validar
            playlist_a_modificar: int = int(playlist_a_modificar)
            is_Int = True

        except ValueError:
            print('Valor no numerico!')
            is_Int = False

        if is_Int:
            if playlist_a_modificar > cant_de_playlists or playlist_a_modificar < 0:
                print('El valor ingresado no esta dentro del rango posible.')
            else:
                in_Range = True

    playlist_ID: str = id_de_playlists[playlist_a_modificar]

    credentials = autenticar()  # Me fijo si tengo credenciales sin vencer y sino creo nuevas.

    youtube = build('youtube', 'v3', credentials=credentials)

    request = youtube.playlistItems().list(part="snippet", playlistId = playlist_ID,
                                       maxResults=50)  # Genero el request q con el part=snippet me dara toda la informacion que necesito. mine=true hara que busque en el canal de la persona que se autentico
    response = request.execute()

    titulo_y_artista:list = []

    for i in range(0,len(response['items'])):
        titulo = response['items'][i]['snippet']['title']

        contador_letra = 0
        ultima_letra = 0
        for x in titulo: #saco todo lo que este entre parentesis

                if x == '(':
                    ultima_letra = contador_letra

                if ultima_letra != 0:
                    titulo=titulo[0:ultima_letra]

                contador_letra+=1


        artista = response['items'][i]['snippet']['videoOwnerChannelTitle']
        titulo_y_artista.append([titulo,artista])


    letras:list = []

    for nombre_cancion_a_buscar, artista_cancion_a_buscar in titulo_y_artista:
        letras.append(modulo_lyrics.letra_cancion(nombre_cancion_a_buscar,''))

    return letras



