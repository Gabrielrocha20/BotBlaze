import json
from time import sleep
import requests
import sqlite3


def add_banco_dados(cor, numero, data, horario):
    conect = sqlite3.connect('banco_de_padroes.db')
    cursor = conect.cursor()
    cursor.execute(f'INSERT INTO horarios_padroes(Cor, Numero, Data, Horario) VALUES ("{cor}"'
                            f', {numero},'
                            f'"{data}", "{horario}")')
    conect.commit()
def start_last_colors():
    try:

        while True:

            URL_LINK_BLAZE = 'https://blaze.com/api/roulette_games/recent'

            information = requests.get(URL_LINK_BLAZE)

            if information.status_code == 200:

                results_colors = json.loads(information.text)

                color, roll, server_seed, date = results_colors[0]['color'], results_colors[0]['roll'], results_colors[0][
                    'server_seed'], results_colors[0]['created_at']

                created_at = date.split('T')[1][:5]
                created_at = f'{int(created_at[:2]) - 3}:{created_at[3:5]}'

                ano, mes, dia = date.split('T')[0][2:4], date.split('T')[0][5:7], date.split('T')[0][8:10]
                data = f'{dia}/{mes}/{ano}'

                ''' 0 = WHITE
                    1 = RED
                    2 = BLACK '''

                if color == 0:
                    color = 'WHITE'

                elif color == 1:
                    color = 'RED'

                else:
                    color = 'BLACK'

                if server_seed not in list_server_seed:

                    print(f"COLOR: {color} | ROLL: {roll} | TIME: {created_at} | DATA: {data}")
                    add_banco_dados(color, roll, data, created_at)
                    list_server_seed.append(server_seed)
                    sleep(20)

                else:
                    continue

            else:
                continue

    except Exception as error:

        with open('ERROR_LOG.txt', 'a') as error_log:
            error_log.writelines(f"ERRO: {error} | STATUS CODE: {information.status_code} ")


list_server_seed = []
start_last_colors()