import requests

def punto7(letras):
    letras = letras

    if len(letras) == 0:
        print('\nPlaylist Vacia. Pruebe introducir otra.')

    else:
        letras_corregidas = []

        rankings_letras = []

        for letra in letras:

            # Elimino todos los corchetes y dejar renglones de las letras para poder identificar las palabras de las letras asi es posible hacer el ranking

            letra = letra.replace('\n', " ")

            lista_letra: list = []

            palabra: list = []

            parar_agregado = False

            for i in letra:

                if i == "[" or i == "(":
                    parar_agregado = True

                if i != " " and parar_agregado == False and i != ',' and i != '.':
                    palabra.append(i)

                elif i == " " and parar_agregado == False:
                    lista_letra.append(("".join(palabra)).lower())
                    palabra = []

                if i == "]" or i == ")":
                    parar_agregado = False

                for i in lista_letra:
                    if i == "" or i == "'" or i == "'":
                        lista_letra.remove(i)

            letras_corregidas.append(' '.join(lista_letra))

            ranking: dict = {}

            for i in lista_letra:
                if i not in ranking.keys():
                    ranking[i] = 1

                elif i in ranking.keys():
                    ranking[i] += 1

            list_ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)

            while len(list_ranking) > 10:
                list_ranking.pop()

            ranking = dict(list_ranking)

            rankings_letras.append(ranking)

        # Uno todos los rankings de las letras en uno solo
        ranking_total = {}
        for diccionario in rankings_letras:

            for key, value in diccionario.items():
                if key in ranking_total.keys():
                    ranking_total[key] += value

                else:
                    ranking_total[key] = value

        # Ordeno los valores del ranking total de mayor a menor

        list_ranking = sorted(ranking_total.items(), key=lambda x: x[1], reverse=True)

        # Limito el ranking a 10 valores nomas
        while len(list_ranking) > 10:
            list_ranking.pop()

        ranking_total = dict(list_ranking)

        print('Ranking de palabras:')

        contador = 1
        for key, value in ranking_total.items():
            print(f'Top {contador}: {key} con {value} repeticiones')
            contador += 1

        # Creacion nube de palabras con todas las letras juntas

        print("Creando nube de palabras...")

        resp = requests.post('https://quickchart.io/wordcloud', json={
            'format': 'png',
            'width': 1000,
            'height': 1000,
            'fontScale': 15,
            'scale': 'linear',
            'text': (" ".join(letras_corregidas)),
        })

        with open('newscloud.png', 'wb') as f:
            f.write(resp.content)

        print("Nube de palabras creada con exito!")