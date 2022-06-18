import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle


def apertura():
    """Precondiciones: Apertura hara el request de las tokens a la api, generando una autentificacion, pero antes verificara si ya existe una que no este expirada. En el caso que este expirada usara la refresh token. Con la token
    obtendremos los permisos para acceder a los datos que necesitamos del usuario a traves de la api.
    Postcondiciones: La funcion apertura retornara las credenciales que nos entrego la api para poder empezara utilizar sus funciones"""

    credentials = None

    # token.pickle guarda las credenciales de logins anterioires

    if os.path.exists('token.pickle'):
        print('Cargando credenciales desde el archivo...')
        with open('token.pickle', 'rb') as token: #Read bites ya que token.pickle es un archivo tipo bite
            credentials = pickle.load(token)


    # Si no hay credenciales validas disponibles, entonces o refresco el token o vuelvo a loginear.
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


###################################


def nombre_playlists()->None:
    """Precondiciones: Nombre playlist hara un request a la api sobre los datos de las playlist de los usuarios. Luego mediante bucles o recorrido del diccionario que llega de la response
    obtendremos los datos del nombre del canal y las playlists"""


    credentials = apertura()

    youtube = build('youtube', 'v3', credentials=credentials)

    request = youtube.playlists().list(part="snippet",mine=True) #Genero el request q con el part=snippet me dara toda la informacion que necesito. mine=true hara que busque en el canal de la persona que se autentico
    response = request.execute()

    cant_de_playlists:int = len(response["items"]) # Obtengo la cantidad de playlists tomando cuantos diccionarios hay dentro de items, que son las playlists

    nombre_de_playlists:list=[]

    nombre_de_canal:str = response["items"][0]["snippet"]["channelTitle"] # Dentro del diccionario response, obtengo le nombre del canal recorriendo por sus keys

    for i in range (0,cant_de_playlists): #Recorro todas las playlists obtenidas como diccionarios para sacar solamente los titulos de las mismas
        nombre_de_playlists.append((response["items"][i]["snippet"]["title"]))

    print("Plataforma: Youtube")
    print(f"Usuario: {nombre_de_canal}")
    print(f"El nombre de las playlist es: {nombre_de_playlists}")


def crear_playlists():

    credentials = apertura()

    youtube = build('youtube', 'v3', credentials=credentials)

    nombre_playlist:str = input('Inserte el nombre de la nueva playlist que desea crear: ')

    descripcion_playlist:str = input('Inserte la descripcion de la playlist: ')

    public_o_private:str = input('Ingrese "private" si desea que su playlist sea privada. Si desea que sea publica ingrese "public": ')

    while public_o_private != 'private' and public_o_private != 'public':
        print('Valor ingresado no valido!. Pruebe otra vez.')
        public_o_private: str = input('Ingrese "private" si desea que su playlist sea privada. Si desea que sea publica ingrese "public": ')

    playlists_insert_response = youtube.playlists().insert(
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

    print('Playlist creada con exito!')
    print(f'Nombre de la playlist: {nombre_playlist}\n'
          f'Descripcion de la playlist: {descripcion_playlist}\n'
          f'Playlist {public_o_private}\n'
          f'Link nueva playlist: https://www.youtube.com/playlist?list={playlists_insert_response["id"]}')



crear_playlists()