import telebot
from telebot import types
import math  

patrikao_bot = telebot.TeleBot('************************') #token removido por questões de segurança

user_data = {} # para guardar os números do usuário

@patrikao_bot.message_handler(commands=['start']) # menu principal com o comando start
def start(msg: telebot.types.Message):
    markup = types.InlineKeyboardMarkup()
    botao_dois_numeros = types.InlineKeyboardButton('Operações com 2 números', callback_data='menu_2nums') # botão para funções com 2 números
    botao_um_numero = types.InlineKeyboardButton('Operações com 1 número', callback_data='menu_1num') # botão para funções com 1 número
    markup.add(botao_dois_numeros, botao_um_numero) # adiciona os botões na tela
    patrikao_bot.send_message(msg.chat.id, 'Escolha o tipo de operação:', reply_markup=markup)

@patrikao_bot.callback_query_handler(func=lambda call: True)
def escolher_operacao(call: types.CallbackQuery):
    chat_id = call.message.chat.id

    if call.data == 'menu_2nums': # operações com 2 números
        markup = types.InlineKeyboardMarkup()
        botao_soma = types.InlineKeyboardButton('Soma', callback_data='Soma')
        botao_subtracao = types.InlineKeyboardButton('Subtração', callback_data='Subtracao')
        botao_multiplicacao = types.InlineKeyboardButton('Multiplicação', callback_data='Multiplicacao')
        botao_divisao = types.InlineKeyboardButton('Divisão', callback_data='Divisao')
        botao_potencia = types.InlineKeyboardButton('Potenciação', callback_data='Potencia')
        markup.add(botao_soma, botao_subtracao, botao_multiplicacao, botao_divisao, botao_potencia)
        patrikao_bot.send_message(chat_id, 'Escolha a operação com 2 números:', reply_markup=markup)

    elif call.data == 'menu_1num': # operações com 1 número
        markup = types.InlineKeyboardMarkup()
        botao_raiz = types.InlineKeyboardButton('Raiz Quadrada', callback_data='Raiz')
        botao_seno = types.InlineKeyboardButton('Seno', callback_data='Seno')
        botao_cosseno = types.InlineKeyboardButton('Cosseno', callback_data='Cosseno')
        botao_log = types.InlineKeyboardButton('Logaritmo', callback_data='Log')
        markup.add(botao_raiz, botao_seno, botao_cosseno, botao_log)
        patrikao_bot.send_message(chat_id, 'Escolha a operação com 1 número:', reply_markup=markup)

    elif call.data in ['Soma', 'Subtracao', 'Multiplicacao', 'Divisao', 'Potencia']:
        user_data[chat_id] = {'operacao': call.data} # salva a operação do usuário
        patrikao_bot.send_message(chat_id, 'Digite o primeiro número:')
        patrikao_bot.register_next_step_handler_by_chat_id(chat_id, receber_primeiro_numero) # chama a função de receber o primeiro número

    elif call.data in ['Raiz', 'Seno', 'Cosseno', 'Log']: 
        user_data[chat_id] = {'operacao': call.data} # salva a operação escolhida
        patrikao_bot.send_message(chat_id, 'Digite o número:')
        patrikao_bot.register_next_step_handler_by_chat_id(chat_id, receber_numero_unico) # chama a função de receber apenas um número

def receber_primeiro_numero(msg: telebot.types.Message): # pega o primeiro número
    chat_id = msg.chat.id
    try:
        numero1 = float(msg.text)
        user_data[chat_id]['numero1'] = numero1
        patrikao_bot.send_message(chat_id, 'Digite o segundo número:')
        patrikao_bot.register_next_step_handler_by_chat_id(chat_id, receber_segundo_numero) # espera o segundo número
    except ValueError: # tratamento de erros 
        patrikao_bot.send_message(chat_id, 'Número inválido. Digite um número válido:')
        patrikao_bot.register_next_step_handler_by_chat_id(chat_id, receber_primeiro_numero)

def receber_segundo_numero(msg: telebot.types.Message): # recebe o segundo número e faz a operação
    chat_id = msg.chat.id
    try:
        numero2 = float(msg.text)
        operacao = user_data[chat_id]['operacao']
        numero1 = user_data[chat_id]['numero1']

        # faz a operação escolhida
        if operacao == 'Soma':
            resultado = numero1 + numero2
        elif operacao == 'Subtracao':
            resultado = numero1 - numero2
        elif operacao == 'Multiplicacao':
            resultado = numero1 * numero2
        elif operacao == 'Divisao':
            if numero2 == 0:
                patrikao_bot.send_message(chat_id, 'Erro: divisão por zero!')
                return
            resultado = numero1 / numero2
        elif operacao == 'Potencia':
            resultado = numero1 ** numero2
        else:
            patrikao_bot.send_message(chat_id, 'Operação inválida.') # tratamento de erros
            return

        # Mostra o resultado e oferece a opção de voltar ao menu inicial
        markup = types.InlineKeyboardMarkup()
        botao_voltar = types.InlineKeyboardButton('Voltar ao Menu Inicial', callback_data='voltar_menu')
        markup.add(botao_voltar)
        patrikao_bot.send_message(chat_id, f'Resultado da {operacao}: {resultado:.2f}\nEscolha a opção abaixo:', reply_markup=markup)

    except ValueError:
        patrikao_bot.send_message(chat_id, 'Número inválido. Digite um número válido:')
        patrikao_bot.register_next_step_handler_by_chat_id(chat_id, receber_segundo_numero)

def receber_numero_unico(msg: telebot.types.Message): # funções com apenas um número
    chat_id = msg.chat.id
    try:
        numero = float(msg.text)
        operacao = user_data[chat_id]['operacao']

        # Faz a conta conforme a escolha do usuário
        if operacao == 'Raiz':
            if numero < 0:
                patrikao_bot.send_message(chat_id, 'Erro: raiz de número negativo não é real!')
                return
            resultado = math.sqrt(numero)
        elif operacao == 'Seno':
            resultado = math.sin(math.radians(numero))  # graus para radianos
        elif operacao == 'Cosseno':
            resultado = math.cos(math.radians(numero)) 
        elif operacao == 'Log':
            if numero <= 0:
                patrikao_bot.send_message(chat_id, 'Erro: log de número <= 0 não existe!')
                return
            resultado = math.log10(numero) # log do número inserido
        else:
            patrikao_bot.send_message(chat_id, 'Operação inválida.') # tratamento de erros
            return

        # mostra o resultado
        markup = types.InlineKeyboardMarkup()
        botao_voltar = types.InlineKeyboardButton('Voltar ao Menu Inicial', callback_data='voltar_menu')
        markup.add(botao_voltar)
        patrikao_bot.send_message(chat_id, f'Resultado da {operacao}: {resultado:.4f}\nEscolha a opção abaixo:', reply_markup=markup)

    except ValueError: # tratamento de erros 
        patrikao_bot.send_message(chat_id, 'Número inválido. Digite um número válido:')
        patrikao_bot.register_next_step_handler_by_chat_id(chat_id, receber_numero_unico)

# exibe o menu novamente se clicar em voltar
@patrikao_bot.callback_query_handler(func=lambda call: call.data == 'voltar_menu')
def voltar_menu(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    start(call.message)  # chama a função start para exibir o menu inicial novamente

# mantem o bot rodando
patrikao_bot.polling()
