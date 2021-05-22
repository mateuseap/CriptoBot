from emoji.core import emojize
import requests
import time
import json
import os
import emoji
import urllib.request

class CriptoBot:

    def __init__(self):
        token = '1877965997:AAE7rBzp0BNeU2Zj1-z4N_CB7D5LoWbHuv0'
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_novas_mensagens(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    mensagem = str(dado["message"]["text"])
                    chat_id = dado["message"]["from"]["id"]
                    self.criar_resposta(mensagem, chat_id)
                    
    # Obter mensagens
    def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=1000'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    # Criar uma resposta
    def criar_resposta(self, mensagem, chat_id):
        if mensagem in ('menu', 'Menu'):
            resposta = f'Selecione a Criptomoeda que você deseja receber atualizações de preço:{os.linesep}{os.linesep}• Digite ▶️0◀️ para selecionar o BitCoin'
            self.responder(resposta, chat_id)
        
        elif mensagem == '/start':
            resposta = emoji.emojize(f'Seja bem vindo ao CriptoBot 🤖{os.linesep}{os.linesep}Digite "menu" para acessar as funcionalidades do CriptoBot :grinning_face_with_big_eyes:')
            self.responder(resposta, chat_id)

        elif mensagem == '0':
            valorAnterior = 0
            while(True):
                try:
                    url = "http://api.coindesk.com/v1/bpi/currentprice.json"
                    with urllib.request.urlopen(url) as url:
                        response = url.read()
                        data = json.loads(response.decode('utf-8'))
                        valor = float(data['bpi']['USD']['rate'].replace(",", ""))
                except urllib.error.HTTPError:
                    valor = 'ERROR'

                if valorAnterior == 0:
                    resposta = emoji.emojize(f'↪️ 1 Bitcoin vale ${valor} dólares!')
                elif valorAnterior < valor:
                    resposta = emoji.emojize(f'🤑 O preço do Bitcoin subiu!{os.linesep}{os.linesep}↪️ 1 Bitcoin vale ${valor} dólares!')
                elif valorAnterior > valor:
                    resposta = emoji.emojize(f'🥶 O preço do Bitcoin desceu!{os.linesep}{os.linesep}↪️ 1 Bitcoin vale ${valor} dólares!')
                else:
                    pass

                valorAnterior = valor

                self.responder(resposta, chat_id)
                time.sleep(10)
                

    # Responder
    def responder(self, resposta, chat_id):
        link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_requisicao)


bot = CriptoBot()
bot.Iniciar()