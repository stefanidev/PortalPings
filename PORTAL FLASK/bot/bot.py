import requests
import time 

def last_chat_id(token):
    try:
        url = "https://api.telegram.org/bot{}/getUpdates".format(token)
        response = requests.get(url)
        if response.status_code == 200:
            json_msg = response.json()
            for json_result in reversed(json_msg['result']):
                message_keys = json_result['message'].keys()
                print(message_keys)
                if ('new_chat_member' in message_keys) or ('group_chat_created' in message_keys):
                    return json_result['message']['chat']['id']
            print('Nenhum grupo encontrado')
        else:
            print('A resposta falhou, cógido de status: {}'.format(response.status_code))
    except Exception as e:
        print("Erro no getUpdates: ", e)

token = '5314422542:AAGbXECqxtq3CCLIVErgK46G2X6X1tEbdlk'
chat_id = '-713730908'

def send_message(token, chat_id, message):
    try:
        data = {"chat_id": chat_id, "text": message}
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        requests.post(url, data)
    except Exception as e:
        print('Erro no sendMessage: ', e)
    
msg = "Ping: xxx.xxx.xx-x está com problemas"

chat = '-691950197'
chat2 = '-1001721209785'

def enviar_imagem(file_path):
    body = {
        'chat_id': chat2,
    }
    files = {
        'photo': open(file_path, 'rb')
    }
    r = requests.post('https://api.telegram.org/bot{}/sendPhoto'.format(
    token), data=body, files=files)
    if r.status_code >= 400:
        print('Houve um erro ao enviar mensagem. Detalhe: {}'.format(r.text))
    else:
        print('Mensagem enviada com sucesso.')



