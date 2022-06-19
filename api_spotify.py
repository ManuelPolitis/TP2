import tekore as tk

def pedir_token():
    """
    La funcion hará el request del token a la api a traves de Tekore.
    Postcondiciones: Retornará el token obtenido a partir de los datos del usuario.
    """
    client_id: str = '6d3faa7cfb01460bacc1605a2f508e0d'
    client_secret: str = '1e159178e8ca443498e3ec58f25fd792'
    redirect_uri: str = 'https://example.com/callback'
    conf: tuple = (client_id, client_secret, redirect_uri)
    #file: str = 'tekore.cfg'

    token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
    #tk.config_to_file(file, conf + (token.refresh_token,))
    return token

def mostrar_playlist(token):
    spotify = tk.Spotify(token)
    playlist = spotify.followed_playlists(limit=10).items
    #track = spotify.playlist_items(playlist.id, limit=1).items[0].track
    for track in playlist:
        print(track.name)



