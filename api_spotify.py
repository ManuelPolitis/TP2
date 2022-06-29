import tekore as tk
import csv

CLIENT_ID: str = '6d3faa7cfb01460bacc1605a2f508e0d'
CLIENT_SECRET: str = '1e159178e8ca443498e3ec58f25fd792'
REDIRECT_URI: str = 'https://example.com/callback'

def pedir_token():
    """
    La funcion hará un request a la api a traves de Tekore para obtener las credenciales.
    Postcondicion: Retornará el token obtenido a partir de los datos del usuario.
    """
    conf: tuple = (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    valido:bool = False
    
    while not valido:
        try:
            token = tk.prompt_for_user_token(*conf, tk.scope.every)
            valido = True
        except KeyError:
            print("\nCopio mal el URL, pruebe hacerlo de nuevo")
            valido = False
    return token

def mostrar_playlist(spotify) -> None:
    """
    Muestra las primeras 20 playlists que tenga el usuario.
    Precondición: Recibe una instancia de la clase Spotify creada a partir del token.
    """
    contador: int = int()
    playlists = spotify.followed_playlists(limit=20).items

    print('\nListas de reproducción: ')

    for track in playlists:
        print(f'{contador + 1} - {track.name}')
        contador += 1

def exportar_csv(spotify) -> None:
    contador: int = int()
    user_id: str = spotify.current_user().id
    lista_playlist = spotify.playlists(user_id, limit=20, offset=0).items
    print("\nLa lista es: ")
    
    for track in lista_playlist:
        print(f"{contador + 1} - {track.name} - {track.id}")
        contador +=1
    
    in_range:bool = False
    is_int:bool = False
    while not is_int or not in_range:
    
        try:
            numero_de_playlist: int = input('\nIngrese el indice de playlist de la que desea obtener un archivo csv: ')
            numero_de_playlist:int = int(numero_de_playlist)
            is_int = True
        
        except ValueError:
            print('Valor no numerico!')
            is_int = False
        
        if is_int:
            if numero_de_playlist > contador or numero_de_playlist < 0:
                print('El valor ingresado no esta dentro del rango posible.')
            else:
                in_range = True
    
    id_playlist:str = lista_playlist[numero_de_playlist-1].id
    nombre_playlist:str = lista_playlist[numero_de_playlist-1].name
    print(f"Eligio la playlist : {nombre_playlist}, id: {id_playlist}")
    link_playlist:str = (f"https://open.spotify.com/playlist/{id_playlist}")

    cantidad_canciones = (spotify.playlist_items(id_playlist, fields=None, market=None, as_tracks=False, limit=100, offset=0)).total
    
    artistas = (spotify.playlist_items(id_playlist, fields=None, market=None, as_tracks=False, limit=100, offset=0)).items
    
    lista_canciones = []
    tiempo: int = 0
    lista_artistas = []
    for i in range(cantidad_canciones):
        
        try:
            musico = artistas[i].track
            nombre_musico = musico.artists[0]
            if nombre_musico.name not in lista_artistas:
                lista_artistas.append(nombre_musico.name)
        except Exception:
            None
        
        lista_canciones.append(musico.name)
        tiempo += musico.duration_ms

    
    tiempo = tiempo/1000
    nombres_artistas:set = set(lista_artistas)
    
    cantidad_artistas:int = len(nombres_artistas)
    
    nombres_canciones:set = set(lista_canciones)
    cantidad_canciones:int = len(nombres_canciones)

    with open(f'playlist_{nombre_playlist}.csv','w',newline='',encoding='UTF-8') as archivo_csv:
        csv_writer = csv.writer(archivo_csv,delimiter =',',quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow((
            "ID de playlist",
            "Nombre de playlist",
            "Cantidad de canciones",
            "Nombres de canciones",
            "Descripción de playlist",
            "Cantidad de seguidores de la playlist",
            "Playlist publica",
            "Cantidad de artistas",
            "nombres de artistas",
            "Playlist colaborativa",
            "ID del propietario",
            "link de playlist",
            "Duración de playlist en segundos"))
        
        print('')
        print('Creando archivo CSV...')

        
        try:
            csv_writer.writerow((
                spotify.playlist(id_playlist, fields=None, market=None, as_tracks=False).id,
                spotify.playlist(id_playlist, fields=None, market=None, as_tracks=False).name,
                cantidad_canciones,
                nombres_canciones,
                spotify.playlist(id_playlist, fields=None, market=None, as_tracks=False).description,
                (spotify.playlist(id_playlist, fields=None, market=None, as_tracks=False).followers).total,
                spotify.playlist(id_playlist, fields=None, market=None, as_tracks=False).public,
                cantidad_artistas,
                nombres_artistas,
                spotify.playlist(id_playlist, fields=None, market=None, as_tracks=False).collaborative,
                (spotify.playlist(id_playlist, fields=None, market=None, as_tracks=False).owner).id,
                link_playlist,
                tiempo
            ))



        except KeyError:
                print('')

        print(f'Archivo creado exitosamente! Nombre del archivo: playlist_{nombre_playlist}.csv')

def crear_playlist(spotify) -> None:
    """
    Crea una playlist vacía a partir de los datos que ingresa el usuario.
    Precondicion: Recibe una instancia de la clase Spotify creada a partir del token.
    """
    user_id: str = spotify.current_user().id
    nombre: str = input('Ingrese el nombre de la playlist: ')
    descripcion: str = input('Escriba una descripción: ')

    spotify.playlist_create(user_id, nombre, True, descripcion)

def buscar_nuevos_elementos(spotify) -> None:
    nombre_cancion_a_buscar: str = input('Ingrese el nombre de la cancion: ')

    buscar:tuple = spotify.search(query=nombre_cancion_a_buscar, limit=3)
    lista_cancion:list = buscar[0].items
    for i in range(3):
        atributos_artista:list = lista_cancion[i].artists
        print(f"{i+1}) {lista_cancion[i].name} , {atributos_artista[0].name} ")
    
    cancion_elegida_str:str = input("Ingrese el número de la canción que desea visualizar (1/2/3): ")
    #Validación de que sea un número
    cancion_elegida_es_int:bool = cancion_elegida_str.isdigit()
    while cancion_elegida_es_int == False:
        print("Ingrese valores enteros")
        cancion_elegida_str = input("Ingrese las figuritas del alumno o 0 sino ingresa más: ")
        cancion_elegida_es_int = cancion_elegida_str.isdigit()
    if cancion_elegida_es_int == True:
        cancion_elegida:int = int(cancion_elegida_str)
    
    while cancion_elegida > 3 or cancion_elegida <= 0:
        print("Ingrese valores entre 1 y 3")
        cancion_elegida_str:str = input("Ingrese el número de la canción que desea visualizar (1/2/3): ")
        #Validación de que sea un número
        cancion_elegida_es_int:bool = cancion_elegida_str.isdigit()
        while cancion_elegida_es_int == False:
            print("Ingrese valores enteros")
            cancion_elegida_str = input("Ingrese las figuritas del alumno o 0 sino ingresa más: ")
            cancion_elegida_es_int = cancion_elegida_str.isdigit()
        if cancion_elegida_es_int == True:
            cancion_elegida:int = int(cancion_elegida_str)
    
    atributos_artista:list = lista_cancion[cancion_elegida-1].artists
    album:list = lista_cancion[cancion_elegida-1].album
    
    print("\nNombre de la canción:",lista_cancion[cancion_elegida-1].name)
    print("Artista:",atributos_artista[0].name)
    print("Album:",album.name)
