import pyautogui as pg
import time 
import requests

token = '5314422542:AAGbXECqxtq3CCLIVErgK46G2X6X1tEbdlk'
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

def encontrar(nome):
    while True:
        image = pg.locateCenterOnScreen('imgs2/{}.png'.format(nome))
        if(image != None):
            pg.click(image)
            return


ini_x = 1
ini_y = 106

fin_x = 867
fin_y = 720

time.sleep(5)

pg.moveTo(ini_x, ini_y)
time.sleep(1)
pg.hotkey('win', 'shift', 's')
time.sleep(6)
pg.mouseDown()
time.sleep(1)
pg.moveTo(fin_x, fin_y)
time.sleep(2)
pg.mouseUp()

encontrar('notifi')
encontrar('disquete')
time.sleep(3)
pg.write('relatorio')
time.sleep(1)
pg.press('enter')
encontrar('sim')
time.sleep(10)

enviar_imagem(r'C:\Users\Vivo2\Desktop\MONITORAMENTO - ALE\backup master\PORTAL FLASK\bot\imgs\relatorio.png')

pg.hotkey('alt', 'f4')