import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import json

def apertura():

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


def nombre_playlists():

    credentials = apertura()

    youtube = build('youtube', 'v3', credentials=credentials)

    request = youtube.playlists().list(part="snippet",mine=True)
    response = request.execute()

    cant_de_playlists:int = len(response["items"])

    nombre_de_playlists:list=[]

    nombre_de_canal:str = response["items"][0]["snippet"]["channelTitle"]

    for i in range (0,cant_de_playlists):
        nombre_de_playlists.append((response["items"][i]["snippet"]["title"]))

    print("Plataforma: Youtube")
    print(f"Usuario: {nombre_de_canal}")
    print(f"El nombre de las playlist es: {nombre_de_playlists}")

