from lyricsgenius import Genius
import os

client_id:str = "4GUOEO9swOqdnknWbco9EICRbuEp19-gCQ7AQXbf7OlLU6whZgyPiEZa7vCCLcYM"
client_secret:str = "6eutEXXOtlXg8gaqtPq7iYY6kyyzT3YfJ28GvKyC_paCKKZDv7Iq61G_RM9E2NFk4LuwH_B9fjt7LKrQ86HSdQ"
client_access_token:str = "aKwvnEEPesxBgGV6N4OohEFqTx0mwgKVRcsvgv8Mv0IZS9EhFwUTEae0G5jbtz3J"

def cls() -> str:
    """Funcion para limpiar la consola, el condicional hace que sirva tanto para linux como para windows"""
    os.system('cls' if os.name == 'nt' else 'clear')

def letra_cancion(titulo,artista):
    """Busca la cancion del artista que fueron pasados por parametro
    Precondciones: Se le debe pasar a la funcion por parametro el nombre de la cancion
    a buscar y el artista de la misma."""

    genius = Genius(client_access_token)

    cancion = genius.search_song(titulo, artista)

    try:
        print("Letra: \n",cancion.lyrics,"\n")

    except AttributeError:
        confirmacion = 0

    confirmacion: str = input("¿Es esta la letra de la cancion que buscabas? (S/N): ")

    while confirmacion.lower() != "s" and confirmacion.lower() != "n":
        print("Valor invalido introducido. Prueba otra vez")
        confirmacion: str = input("¿Es esta la letra de la cancion que buscabas? (S/N): ")

    if confirmacion.lower() == 's':
        return cancion.lyrics

    if confirmacion.lower() == "n":
        cls()
        print("Para ser mas preciso en la busqueda de la letra, especifique el titulo y nombre del artista correctamente")
        titulo:str = input("Titulo de la cancion: ")
        artista:str = input("Artista de la cancion: ")

        cancion = genius.search_song(titulo, artista)

        try:
            return cancion.lyrics

        except AttributeError:
            return ""

