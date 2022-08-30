import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sqlite3
import telebot

class BotBlaze:
    token = '5642593484:AAFTATUVCN1rUePW45BGbKF7DY_mWktPQdU'
    bot_telegram = telebot.TeleBot(token)
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("-headless")
        self.nav = webdriver.Chrome(options=self.chrome_options)

        self.nav.get('https://blaze.com/pt/games/double')

        self.token = '5642593484:AAFTATUVCN1rUePW45BGbKF7DY_mWktPQdU'
        self.bot_telegram = telebot.TeleBot(self.token)

        self.cores = []
        self.texto = None
        self.guarda_cores = None
        self.resultado = None

        self.emoji = {
            'Vermelho': '🔴',
            'Preto': '⚫'
        }
        self.con = sqlite3.connect('banco_de_padroes.db')
        self.cursor = self.con.cursor()

    def recebe_dados(self):
        tfg = []
        i = 1
        while i <= 5:
            pegardados = self.nav.find_element(By.XPATH, f'//*[@id="roulette-recent"]/div/div[1]/div[{i}]').text
            if pegardados != '':
                tfg.append(pegardados)
            else:
                tfg.append('0')
            i += 1

        cores = []
        for n in tfg:
            if int(n) == 0:
                cores.append('B')
            elif int(n) <= 7:
                cores.append('V')
            else:
                cores.append('P')

        self.cores = cores[::-1]
        print(self.cores)
        return self.cores

    def checar_padroes(self):
        self.guarda_cores = ''
        for cor in self.cores:
            self.guarda_cores += f' {cor}'
        self.cursor.execute('SELECT * FROM padroes')
        padroes = self.cursor.fetchall()
        for linha in padroes:
            linha = list(linha)
            padrao = linha[0].split(' ')
            if self.cores == padrao:
                self.calcular_chance()
                resultado = self.resultado
                self.texto = f'Chance de ser {self.emoji[linha[1]]}\n' \
                             f'Com proteção no ⚪\n' \
                             f'Lembrando Caso Nao esteja a favor\n' \
                             f'\n'\
                             f'{resultado[0]}% Win | {resultado[1]}% Loss' \
                             f'\n' \
                             f'Nao jogue\n' \
                             f'Tendencias:\n' \
                             f'Tendendia de Red:🔴🔴⚫⚫\n' \
                             f'Tendendia de Black:⚫⚫🔴🔴\n' \
                             f'Tendendia de Red:🔴⚫🔴⚫\n' \
                             f'Tendendia de Black:⚫🔴⚫🔴'
                return
            pass
        print(self.cores)
        pergunta = input('Deseja Digitar o resultado? S ou N ')
        if pergunta == 'N':
            return
        resultado = input('Digite o resultado: ')

        self.cursor.execute(f'INSERT INTO padroes (Padrao, Resultado, Vitoria, Derrota) VALUES ("{self.guarda_cores[1:]}"'
                            f', "{resultado}",'
                            f'{0}, {0})')
        self.con.commit()

    def enviar_resultados(self):
        chat_id = '-623026227'
        mensagem = self.texto
        url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={mensagem}'
        requests.get(url)

    def calcular_chance(self):
        cores = ''
        for cor in self.cores:
            cores += f' {cor}'
        self.cursor.execute(f'SELECT Vitoria, Derrota FROM padroes WHERE padrao="{cores[1:]}"')
        resultados = self.cursor.fetchall()
        for v, d in resultados:
            soma = v + d
            vitorias = v * 100
            derrotas = d * 100
            if v == 0:
                if derrotas == 0:
                    self.resultado = [vitorias, derrotas]
                else:
                    self.resultado = [vitorias, derrotas / soma]
            else:
                if derrotas == 0:
                    self.resultado = [vitorias / soma, derrotas]
                else:
                    self.resultado = [vitorias / soma, derrotas / soma]

    def adiciona_resultado(self, resultado):
        self.cursor.execute(f'SELECT Vitoria, Derrota FROM padroes WHERE padrao="{self.guarda_cores[1:]}"')
        resultados = self.cursor.fetchall()
        for v, d in resultados:
            if resultado == 'Loss':
                self.cursor.execute(f'UPDATE padroes SET Derrota ={d + 1} WHERE Padrao="{self.guarda_cores[1:]}"')
                self.con.commit()
            else:
                self.cursor.execute(f'UPDATE padroes SET Vitoria ={v + 1} WHERE Padrao="{self.guarda_cores[1:]}"')
                self.con.commit()

    def exit(self):
        self.nav.close()
        self.nav.quit()


if __name__ == '__main__':
    s = ''
    bot = BotBlaze()
    while s == '':
        bot.recebe_dados()
        # bot.checar_padroes()
        # bot.enviar_resultados()

        s = input('Digite: ')
