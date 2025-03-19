from flask import Flask, render_template_string
import random
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz

# Lista de membros do chatCore
chat_core_members = ["Sousa", "Marcus", "Duda", "Nana", "Barcala"]

app = Flask(__name__)
sorteado = ""
drawn_this_week = set()  # Armazena os membros já sorteados na semana
current_week = datetime.now().isocalendar()[1]  # Obtém a semana atual

# Função para sortear um membro sem repetir durante a semana
def draw_member():
    global sorteado, drawn_this_week, current_week

    # Obtém a semana atual
    new_week = datetime.now().isocalendar()[1]

    # Se a semana mudou, resetamos a lista
    if new_week != current_week:
        drawn_this_week.clear()
        current_week = new_week

    # Filtra membros que ainda não foram sorteados nesta semana
    available_members = [m for m in chat_core_members if m not in drawn_this_week]

    if not available_members:
        # Todos já foram sorteados, resetamos a lista
        drawn_this_week.clear()
        available_members = chat_core_members

    # Sorteia um membro e adiciona à lista dos sorteados
    sorteado = random.choice(available_members)
    drawn_this_week.add(sorteado)

def schedule_task():
    timezone = pytz.timezone('America/Sao_Paulo')
    scheduler = BackgroundScheduler()
    scheduler.add_job(draw_member, 'cron', hour=15, minute=9, timezone=timezone)
    scheduler.start()

# Rota principal que exibe o membro sorteado
@app.route('/')
def show_sorteado():
    html_template = '''
    <html>
        <head>
            <title>Sorteio de Membro do ChatCore</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f8ff;
                    color: #333;
                    text-align: center;
                    margin-top: 50px;
                }
                h1 {
                    color: #4CAF50;
                }
                p {
                    font-size: 24px;
                    color: #555;
                }
            </style>
        </head>
        <body>
            <h1>Membro do ChatCore Sorteado</h1>
            <p>{{ sorteado }}</p>
        </body>
    </html>
    '''
    return render_template_string(html_template, sorteado=sorteado)

if __name__ == '__main__':
    draw_member()  # Inicializa com um membro sorteado
    schedule_task()  # Agenda a tarefa para rodar todos os dias
    app.run(host='0.0.0.0', port=5000)