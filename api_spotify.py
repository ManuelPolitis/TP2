import tekore as tk

CLIENT_ID: str = '6d3faa7cfb01460bacc1605a2f508e0d'
CLIENT_SECRET: str = '1e159178e8ca443498e3ec58f25fd792'
REDIRECT_URI: str = 'https://example.com/callback'

def pedir_token():
    """
    La funcion hará un request a la api a traves de Tekore para obtener las credenciales.
    Postcondicion: Retornará el token obtenido a partir de los datos del usuario.
    """
    conf: tuple = (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    token = tk.prompt_for_user_token(*conf, tk.scope.every)
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

def crear_playlist(spotify) -> None:
    """
    Crea una playlist vacía a partir de los datos que ingresa el usuario.
    Precondicion: Recibe una instancia de la clase Spotify creada a partir del token.
    """
    user_id: str = spotify.current_user().id
    nombre: str = input('Ingrese el nombre de la playlist: ')
    descripcion: str = input('Escriba una descripción: ')

    spotify.playlist_create(user_id, nombre, True, descripcion)