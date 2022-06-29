import modulo_youtube
import os
import api_spotify
import tekore as tk
import punto_7

def cls() -> None:
    """Funcion para limpiar la consola, el condicional hace que sirva tanto para linux como para windows"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():

    continuar:bool = True

    while continuar:
        print("""
Menu Principal TP2

1- Autenticarse en Youtube y Spotify
2- Ver tus playlist en una de las plataformas
3- Elegir una playlist y exportarla a CSV
4- Crear una playlist en una de las plataformas
5- Buscar nuevos elementos para visualizar o agregarlos a una playlist
6- Sincronizar una playlist entre ambas plataformas
7- Construir una nube de palabras y el ranking top 10 de palabras mas utilizadas en la letra de una playlist
8- Salir
        """)

        #Realizo validacion de que se haya realizado una eleccion válida

        is_Int: bool = False
        in_Range: bool = False

        while not is_Int or not in_Range:
            try:
                eleccion: int = int(input('Ingrese el numero de la accion que desea realizar: '))
                is_Int = True

            except ValueError:
                print('Valor no numerico!')
                is_Int = False

            if is_Int:

                if eleccion > 8 or eleccion < 1:
                    print('El valor ingresado no esta dentro del rango posible.')
                else:
                    in_Range = True

        print('')

        if eleccion == 2 or eleccion == 3 or eleccion == 4 or eleccion == 5 or eleccion == 7:
            plataforma:str = (input('Ingrese en que plataforma desea realizar la accion (youtube/spotify): ')).lower()

            while plataforma != 'youtube' and plataforma != 'spotify':
                print('Plataforma invalida.')
                plataforma: str = (input('Ingrese en que plataforma desea realizar la accion (youtube/spotify): ')).lower()


        cls()

        def autenticacion_spotify():
            print("Autenticacion Spotify: \n")
            Spotify = tk.Spotify(api_spotify.pedir_token())
            return Spotify

        if eleccion == 1:
            print("Autenticacion Youtube: \n")
            modulo_youtube.autenticar()
            print("")
            Spotify = autenticacion_spotify()

        if eleccion == 2:
            if plataforma == 'youtube':
                modulo_youtube.nombre_playlists()

            if plataforma == 'spotify':
                try:
                    api_spotify.mostrar_playlist(Spotify)
                except UnboundLocalError:
                    Spotify = autenticacion_spotify()
                    api_spotify.mostrar_playlist(Spotify)

        if eleccion == 3:
            if plataforma == 'youtube':
                modulo_youtube.playlist_csv()

            if plataforma == 'spotify':
                try:
                    api_spotify.exportar_csv(Spotify)
                except UnboundLocalError:
                    Spotify = autenticacion_spotify()
                    api_spotify.exportar_csv(Spotify)

        if eleccion == 4:
            if plataforma == 'youtube':
                modulo_youtube.crear_playlists()

            if plataforma == 'spotify':
                try:
                    api_spotify.crear_playlist(Spotify)
                except UnboundLocalError:
                    Spotify = autenticacion_spotify()
                    api_spotify.crear_playlist(Spotify)

        if eleccion == 5:
            if plataforma == 'youtube':
                modulo_youtube.agregar_cancion()

            if plataforma == 'spotify':
                try:
                    api_spotify.buscar_nuevos_elementos(Spotify)
                except UnboundLocalError:
                    Spotify = autenticacion_spotify()
                    api_spotify.buscar_nuevos_elementos(Spotify)

        if eleccion == 6:
            pass

        if eleccion == 7:
            if plataforma == 'youtube':
                letras = modulo_youtube.funcion_letras()
                punto_7.punto7(letras)

            if plataforma == 'spotify':
                try:
                    letras = api_spotify.funcion_letras(Spotify)

                except UnboundLocalError:
                    Spotify = autenticacion_spotify()
                    letras = api_spotify.funcion_letras(Spotify)
                cls()
                punto_7.punto7(letras)


        if eleccion == 8:
            continuar = False

        print("")
        confirmacion:str = (input('Desea continuar? (s/n): ')).lower()

        while confirmacion != 's' and confirmacion != 'n':
            print('Ingreso invalido.')
            confirmacion: str = (input('Desea continuar? (s/n): ')).lower()

        if confirmacion == 'n':
            continuar = False

        cls()
main()