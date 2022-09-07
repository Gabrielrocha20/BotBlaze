import sqlite3
from time import sleep
from selenium import webdriver
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class BotDouble:
    def __init__(self):
        self.api = ''
        self.chat_id = ''

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
        self.msg_app = ''

        self.win_cores = 0
        self.win_branco = 0
        self.win_gale = 0
        self.loss = 0

        # Validação para interface
        self.sem_resultado = False

    ######## Funçoes para retornar resultados ########
    def ler_banco(self):
        self.cursor.execute(f'SELECT * FROM padroes')
        resultados = self.cursor.fetchall()
        return resultados

    def ler_vitoria_derrota(self, sequencia):
        self.cursor.execute(f'SELECT Vitoria, Derrota FROM padroes WHERE padrao="{sequencia}"')
        resultado = self.cursor.fetchall()
        for vitoria, derrota in resultado:
            return [vitoria, derrota]

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
        return self.transforma_cores(self.dados[::-1])

    def transforma_cores(self, dados):
        self.cores = ' '.join(['B' if int(n) == 0 else 'V' if int(n) <= 7 else 'P' for n in dados])
        return self.cores

    def checar_padroes(self):
        resultados = self.ler_banco()
        for sequencia, resultado, vitoria, derrota in resultados:
            if self.cores == sequencia:
                self.calculadora(vitoria, derrota)
                self.msg_app = self.enviar_para_app(sequencia, self.dados[0], resultado)
                return self.enviar_msg_telegram(prev=resultado, percentual=self.percentual)
        self.sem_resultado = True
        return self.enviar_msg_telegram(msg='Aguarde')

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
                        Entrar depois do {self.dados[0]}
                        Com Gale 1

                        Tendencias:
                        Tendendia de Red:🔴🔴⚫⚫
                        Tendendia de Red:🔴⚫🔴⚫
                        Tendendia de Black:⚫⚫🔴🔴
                        Tendendia de Black:⚫🔴⚫🔴
                        """
            url = f'https://api.telegram.org/bot{self.api}/sendMessage?chat_id={self.chat_id}&text={msg}'
            requests.get(url)
            return
        url = f'https://api.telegram.org/bot{self.api}/sendMessage?chat_id={self.chat_id}&text={msg}'
        requests.get(url)

    def enviar_para_app(self, sequencia: str, numero, resultado):
        sequencia = sequencia.replace('V', self.emoji['Vermelho'])\
                                .replace('P', self.emoji['Preto'])\
                                .replace('B', self.emoji['Branco'])
        return f'{sequencia} entrar apos o {numero} na cor {self.emoji[resultado]}'



    def resultado_do_giro(self, resultado):
        alternativa = {
            '1': '🟢🟢🟢WIN🟢🟢🟢',
            '2': '⚪⚪⚪Branco⚪⚪⚪ \n Tente no duplo tambem',
            '3': '🐔🐔🐔G1🐔🐔🐔',
            '4': '🔴🔴🔴Loss🔴🔴🔴'
        }

        self.enviar_msg_telegram(msg=alternativa[resultado])
        self.contagem_resultados(resultado)

    def contagem_resultados(self, resultado):
        resultados = self.ler_vitoria_derrota(self.cores)
        if resultado == '1':
            self.win_cores += 1
            self.cursor.execute(f'UPDATE padroes SET Vitoria={resultados[0] + 1} WHERE Padrao="{self.cores}"')
            self.conectar.commit()
        elif resultado == '2':
            self.win_branco += 1
            self.cursor.execute(f'UPDATE padroes SET Vitoria={resultados[0] + 1} WHERE Padrao="{self.cores}"')
            self.conectar.commit()
        elif resultado == '3':
            self.win_gale += 1
            self.cursor.execute(f'UPDATE padroes SET Vitoria={resultados[0] + 1} WHERE Padrao="{self.cores}"')
            self.conectar.commit()
        else:
            self.loss += 1
            self.cursor.execute(f'UPDATE padroes SET Derrota={resultados[1] + 1} WHERE Padrao="{self.cores}"')
            self.conectar.commit()
        self.enviar_msg_telegram(msg=f'{self.win_cores}Wins🟢   '
                                     f'{self.win_branco}Brancos⚪   '
                                     f'{self.win_gale}Gale🐔   '
                                     f'{self.loss}Loss🔴')

    def exit(self):
        self.driver.quit()


# if __name__ == '__main__':
#    s = ''
#    bot = BotDouble('5642593484:AAFTATUVCN1rUePW45BGbKF7DY_mWktPQdU', '-623026227')
#    while s == '':
#        bot.coletar_dados()
#        bot.checar_padroes()
#        s = input('Digite: ')
#   bot.exit()
