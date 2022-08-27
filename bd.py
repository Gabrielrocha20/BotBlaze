import sqlite3

con = sqlite3.connect('banco_de_padroes.db')
cursor = con.cursor()

"""results = cursor.fetchall()
with open('padroes',  'r') as padroes:
    for linha in padroes:
        parametros = linha.split(',')
        padrao = parametros[0]
        resultado = parametros[1]
        vitoria = int(parametros[2])
        derrota = int(parametros[3])

        cursor.execute(f'INSERT INTO padroes (Padrao, Resultado, Vitoria, Derrota) VALUES ("{padrao}", "{resultado}",'
                       f'{vitoria}, {derrota})')

        con.commit()"""

soma = 8 + 5
vitorias = 8 * 100
resultado = f'{vitorias / soma:.0f}'
print(resultado)