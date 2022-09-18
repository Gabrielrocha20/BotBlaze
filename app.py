import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from bot_app import *
from bot_blaze import BotDouble
from os import getenv
import os.path


class AppBot(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

        self.bot = BotDouble()
        self.username = getenv("USERNAME")
        self.arquivo = fr'C:\Users\{self.username}\Desktop\configuracao_bot.txt'
        if os.path.isfile(self.arquivo):
            pass
        else:
            self.arquivo = fr'C:\Users\{self.username}\OneDrive\Área de Trabalho\configuracao_bot.txt'
        if os.path.isfile(self.arquivo):
            with open(self.arquivo, 'r') as config:
                chave_api, chat_id = config
            self.bot.api = chave_api.strip()
            self.inputChaveapi.setText(self.bot.api)

            self.bot.chat_id = chat_id.strip()
            self.inputChaveid.setText(self.bot.chat_id)


        ###BOTÕES###
        self.btnMenu.clicked.connect(self.menu_lateral)
        self.btnConfiguracao.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.btnVoltar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page))
        self.btnIniciar.clicked.connect(self.iniciar_bot)
        self.btnRodar.clicked.connect(self.rodar)

        self.btnBranco.clicked.connect(self.winBranco)
        self.btnWin.clicked.connect(self.winGreen)
        self.btnGale.clicked.connect(self.winGale)
        self.btnLoss.clicked.connect(self.loss)

        self.btnAlerta.clicked.connect(self.alerta_comecando)
        self.btnContraTendencia.clicked.connect(self.contra_tendencia)
        self.btnJogaGale.clicked.connect(self.jogar_gale)

        ### Contador
        self.Branco_count = 0
        self.Win_count = 0
        self.Gale_count = 0
        self.Loss_count = 0

    def iniciar_bot(self):
        if os.path.isfile(self.arquivo):
            return
        self.bot.api = self.inputChaveapi.text()
        self.bot.chat_id = self.inputChaveid.text()
        if self.checkManterSalvo.isChecked():
            with open(self.arquivo, 'w') as config:
                config.write(f'{self.inputChaveapi.text()} \n'
                             f'{self.inputChaveid.text()}')

    def menu_lateral(self):
        width = self.menu.width()
        if width == 0:
            newWidth = 50
        else:
            newWidth = 0

        self.animation = QtCore.QPropertyAnimation(self.menu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def rodar(self):
        self.bot.coletar_dados()
        self.bot.checar_padroes()
        self.labelSinais.setText(self.bot.msg_app if len(self.bot.msg_app) > 2 else 'Aguarde')

    def winBranco(self):
        self.bot.resultado_do_giro('2')
        self.Branco_count += 1
        self.labelBranco.setText(f'{self.Branco_count}')

    def winGreen(self):
        self.bot.resultado_do_giro('1')
        self.Win_count += 1
        self.labelWin.setText(f'{self.Win_count}')

    def winGale(self):
        self.bot.resultado_do_giro('3')
        self.Gale_count += 1
        self.labelGale.setText(f'{self.Gale_count}')

    def loss(self):
        self.bot.resultado_do_giro('4')
        self.Loss_count += 1
        self.labelLoss.setText(f'{self.Loss_count}')

    def jogar_gale(self):
        self.bot.enviar_msg_telegram(msg='Jogar Gale 1')

    def contra_tendencia(self):
        self.bot.enviar_msg_telegram(msg='Alerta Contra Tendencia')

    def alerta_comecando(self):
        self.bot.enviar_msg_telegram(msg='Vamos Começar Todos prontos')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Bot = AppBot()
    Bot.show()
    app.exec_()