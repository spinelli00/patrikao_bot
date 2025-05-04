import telebot
from telebot import types

patrikao_bot = telebot.TeleBot('******************') #Token removido por questões de segurança

user_data = {} #Dicionario usado como memória para salvar a função desejada do usuario

@patrikao_bot.message_handler(commands=['start']) #Exibe os botões quando o usuário envia /start 
def start(msg: telebot.types.Message):
    markup = types.InlineKeyboardMarkup()
    botao_soma = types.InlineKeyboardButton('Soma', callback_data='Soma')
    botao_subtracao = types.InlineKeyboardButton('Subtracao', callback_data='Subtracao')
    botao_multiplicacao = types.InlineKeyboardButton('Multiplicacao', callback_data='Multiplicacao')
    botao_divisao = types.InlineKeyboardButton('Divisao', callback_data='Divisao')
    markup.add(botao_soma, botao_subtracao, botao_multiplicacao, botao_divisao) #Adiciona os botões 
    patrikao_bot.send_message(msg.chat.id, 'Bem vindo à calculadora desenvolvida em Python! \n Escolha a sua opção : ', reply_markup=markup)

@patrikao_bot.callback_query_handler(func=lambda call: True) #Exibe e salva a opção desejada do usuario
def escolher_operacao(call: types.CallbackQuery):
    chat_id = call.message.chat.id #Pega o id do chat 
    user_data[chat_id] = {'operacao': call.data} #salva no dicionario a opção escolhida pelo usuário
    patrikao_bot.send_message(chat_id, 'Digite o primeiro número:') #exibe o texto para inserir o primeiro numero
    patrikao_bot.register_next_step_handler_by_chat_id(chat_id, receber_primeiro_numero) #espera a próxima função do usuário

def receber_primeiro_numero(msg: telebot.types.Message):
    chat_id = msg.chat.id #coleta o id do chat 
    try: #para o tratamento de erros
        numero1 = float(msg.text)
        user_data[chat_id]['numero1'] = numero1 #adiciona no dicionario o primeiro número
        patrikao_bot.send_message(chat_id, 'Digite o segundo número:') #exibe a mensagem de segundo número
        patrikao_bot.register_next_step_handler_by_chat_id(chat_id, receber_segundo_numero)
    except ValueError:
        patrikao_bot.send_message(chat_id, 'Número inválido. Digite um número válido:')
        patrikao_bot.register_next_step_handler_by_chat_id(chat_id, receber_primeiro_numero) #da a opção para o usuario inserir outro número

def receber_segundo_numero(msg: telebot.types.Message): #função que recebe o segundo número
    chat_id = msg.chat.id 
    try: #tratamento de erros
        numero2 = float(msg.text)
        operacao = user_data[chat_id]['operacao'] #salva a operação do usuario 
        numero1 = user_data[chat_id]['numero1'] #puxa da memória o numero 1

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
        else:
            patrikao_bot.send_message(chat_id, 'Operação inválida.')
            return

        patrikao_bot.send_message(chat_id, f'Resultado da {operacao}: {resultado:.2f}')

    except ValueError:
        patrikao_bot.send_message(chat_id, 'Número inválido. Digite um número válido:')
        patrikao_bot.register_next_step_handler_by_chat_id(chat_id, receber_segundo_numero)

patrikao_bot.polling() #mantém o bot rodando
