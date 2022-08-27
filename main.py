import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class BotBlaze:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("-headless")
        self.nav = webdriver.Chrome()

        self.nav.get('https://blaze.com/pt/games/double')

        self.cores = []
        self.texto = None

        self.emoji = {
            'Vermelho': '🔴',
            'Preto': '⚫'
        }

    def recebe_dados(self):
        pegardados = self.nav.find_element(By.XPATH, '//*[@id="roulette-recent"]').text

        tfg = pegardados.split()[:5]
        cores = []
        for n in tfg:
            if int(n) < 8:
                cores.append('V')
            else:
                cores.append('P')

        self.cores = cores[::-1]
        return self.cores

    def checar_padroes(self):
        with open('padroes', 'r') as sequencias:
            for linha in sequencias:
                sequencia = linha.split(',')
                padrao = sequencia[0].split(' ')

                if self.cores == padrao:

                    self.texto = f'Chance de ser {self.emoji[sequencia[1][:-1]]}\n ' \
                                 f'Com proteção no ⚪\n' \
                                 f'Lembrando Caso Nao esteja a favor\n' \
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
        with open('padroes', 'a') as padroes:
            cores = ''
            for cor in self.cores:
                cores += f'{cor} '
            padroes.write(f'{cores[:-1]},{resultado}\n')

    def enviar_resultados(self):
        token = '5642593484:AAFTATUVCN1rUePW45BGbKF7DY_mWktPQdU'
        chat_id = '-623026227'
        mensagem = self.texto
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensagem}'
        requests.get(url)

    def exit(self):
        self.nav.close()
        self.nav.quit()


if __name__ == '__main__':
    s = ''
    bot = BotBlaze()
    while s == '':
        bot.recebe_dados()
        bot.checar_padroes()
        bot.enviar_resultados()
        s = input('Digite: ')
