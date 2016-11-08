import random
import requests
import ast
from sys import argv
from bottle import run, get, post, view, request, redirect, route, static_file

cartas  = []
server = argv[2]
h_cartas = {}
clientes = []


def comparar(a , b):
    return max(h_cartas[a], h_cartas[b])


def hierarquia_cartas():
    for i in range(2,10):
        h_cartas[str(i)] = i

    h_cartas['T'] = 10
    h_cartas['J'] = 11
    h_cartas['Q'] = 12
    h_cartas['K'] = 13
    h_cartas['A'] = 14


def envia_cliente():
	r = requests.get('http://localhost:' + server + '/get_players/'+argv[1])


@get('/eh_maior/<cartas_adv>')
def eh_maior(cartas_adv):
    cartas_adv = ast.literal_eval(cartas_adv)
    hierarquia_cartas()
    adv = comparar(cartas_adv[0][0], cartas_adv[1][0])
    eu = comparar(cartas[0][0], cartas[1][0])
    if adv > eu:
        print("Sim")
    else:
        print("Nao")

    print("Cartas adv:", cartas_adv, adv)
    print("Minhas cartas: ", cartas, eu)


@get('/recebe_clientes/<cli>')
def recebe_clientes(cli):
    print(cli)
    global clientes
    clientes = ast.literal_eval(cli)


@get('/acordo')
def acordo():
    print("Clientes:", clientes)
    for c in clientes:
        print(c)
        if c != argv[1]:
            print('http://localhost:' + c + '/eh_maior/' + str(cartas))
            requests.get('http://localhost:' + c + '/eh_maior/' + str(cartas))


@get('/recebe_cartas/<mao>')
def recebe_cartas(mao):
    global cartas
    mao = ast.literal_eval(mao)
    cartas += mao


@get('/')
@view('client')
def index():
	#convert_cartas = ast.literal_eval(cartas[0]) if cartas else []
	return {'cartas': cartas}


envia_cliente()

@route('/img/:filename', name='static')
def send_image(filename):
    return static_file(filename, root='./img/', mimetype='image/png')

run(host='localhost', port=int(argv[1]))
