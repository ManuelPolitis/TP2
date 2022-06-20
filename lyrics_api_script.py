from lyricsgenius import Genius

client_id:str = "4GUOEO9swOqdnknWbco9EICRbuEp19-gCQ7AQXbf7OlLU6whZgyPiEZa7vCCLcYM"
client_secret:str = "6eutEXXOtlXg8gaqtPq7iYY6kyyzT3YfJ28GvKyC_paCKKZDv7Iq61G_RM9E2NFk4LuwH_B9fjt7LKrQ86HSdQ"
client_access_token:str = "aKwvnEEPesxBgGV6N4OohEFqTx0mwgKVRcsvgv8Mv0IZS9EhFwUTEae0G5jbtz3J"


def letra_cancion_youtube(titulo,artista):
    genius = Genius(client_access_token)

    busqueda = titulo + " " + artista

    song = genius.search_song(busqueda)

    try:
        print("Letra: \n",song.lyrics)

    except AttributeError:
        print("")


letra_cancion_youtube("cuatro veintiuno","emilia mernes")