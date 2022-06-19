import tekore as tk

def pedir_token():
    """
    La funcion hará el request del token a la api a traves de Tekore.
    Postcondicion: Retornará el token obtenido a partir de los datos del usuario.
    """
    client_id: str = '6d3faa7cfb01460bacc1605a2f508e0d'
    client_secret: str = '1e159178e8ca443498e3ec58f25fd792'
    redirect_uri: str = 'https://example.com/callback'
    conf: tuple = (client_id, client_secret, redirect_uri)

    token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
    return token

def mostrar_playlist(token) -> None:
    """
    Muestra las primeras 20 playlists que tenga el usuario.
    Precondición: Recibe el token obtenido de la Api.
    """
    contador: int = 0
    spotify = tk.Spotify(token)
    playlist = spotify.followed_playlists(limit=20).items

    print('Listas de reproducción: ')
    for track in playlist:
        print(f'{contador + 1} - {track.name}')
        contador += 1



