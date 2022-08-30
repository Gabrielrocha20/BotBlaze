import sqlite3
from time import sleep
from selenium import webdriver
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class BotDouble:
    def __init__(self, api, chat_id):
        self.api = api
        self.chat_id = chat_id

        self.option = Options()
        self.option.add_argument("-headless")

        self.driver = webdriver.Chrome(options=self.option)
        self.driver.get('https://blaze.com/pt/games/double')

        self.emoji = {
            'Vermelho': '🔴',
            'Preto': '⚫',
            'Branco': '⚪'
        }

        self.conectar = sqlite3.connect('banco_de_padroes.db')
        self.cursor = self.conectar.cursor()

        self.cores = ''
        self.percentual = []
        self.dados = []

        # Validação para interface
        self.sem_resultado = False

    ######## Funçoes para retornar resultados ########
    def ler_banco(self):
        self.cursor.execute(f'SELECT * FROM padroes')
        resultados = self.cursor.fetchall()
        return resultados

    def calculadora(self, vitoria, derrota):
        soma = vitoria + derrota + 2
        self.percentual = [(vitoria + 1) * 100 / soma, (derrota + 1) * 100 / soma]
        return self.percentual

    #####################################################

    def coletar_dados(self):
        self.dados = []
        index = 1

        while index <= 5:
            pegar_dados = self.driver.find_element(By.XPATH, f'//*[@id="roulette-recent"]/div/div[1]/div[{index}]').text

            self.dados.append('0' if pegar_dados == '' else pegar_dados)
            index += 1
            self.dados = self.dados[::-1]
        return self.transforma_cores(self.dados)

    def transforma_cores(self, dados):
        self.cores = ' '.join(['B' if int(n) == 0 else 'V' if int(n) <= 7 else 'P' for n in dados])
        return self.cores

    def checar_padroes(self):
        resultados = self.ler_banco()
        for sequencia, resultado, vitoria, derrota in resultados:
            if self.cores == sequencia:
                self.calculadora(vitoria, derrota)
                return

        self.sem_resultado = True
        return 'Aguarde'

    def novo_padrao(self, resultado):
        self.cursor.execute(f'INSERT INTO padroes (Padrao, Resultado, Vitoria, Derrota) VALUES ("{self.cores}"'
                            f', "{resultado}",'
                            f'{0}, {0})')
        self.conectar.commit()
        self.sem_resultado = False
    
    def enviar_msg_telegram(self, prev=None, percentual=None, msg=None):
        if msg is None:
            sequencia = self.cores\
                .replace('V', self.emoji['Vermelho'])\
                .replace('P', self.emoji['Preto'])\
                .replace('B', self.emoji['Branco'])
            msg = f"""
                        Chance de ser {self.emoji[prev]} 
                        Com proteção no ⚪
                        Lembrando Caso nao esteja a favor

                        {percentual[0]:.0f}% Win | {percentual[1]:.0f}% Loss

                        Sequencia: {sequencia}
                        Entrar depois do {self.dados[-1]}
                        Com Gale 1

                        Tendencias:
                        Tendendia de Red:🔴🔴⚫⚫
                        Tendendia de Red:🔴⚫🔴⚫
                        Tendendia de Black:⚫⚫🔴🔴
                        Tendendia de Black:⚫🔴⚫🔴
                        """
        url = f'https://api.telegram.org/bot{self.api}/sendMessage?chat_id={self.chat_id}&text={msg}'
        requests.get(url)
        


if __name__ == '__main__':
    s = ''
    bot = BotDouble('Oi', 'A')
    while s == '':
        bot.coletar_dados()
        print(bot.cores)
        s = input('Digite: ')
