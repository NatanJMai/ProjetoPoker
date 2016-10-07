import random
import requests
import ast
from sys import argv
from bottle import run, get, post, view, request, redirect, route, static_file

global cartas

cartas  = []
server = argv[2]

def envia_cliente():
	r = requests.get('http://localhost:' + server + '/get_players/'+argv[1])


#@get('/get_cartas')
#def get_cartas():
#	r = requests.get('http://localhost:' + server + '/get_cartas')
	#print(r.text)

@get('/recebe_cartas/<mao>')
def recebe_cartas(mao):
	cartas.append(mao)
	print(cartas)

@get('/')
@view('client')
def index():
	convert_cartas = ast.literal_eval(cartas[0]) if cartas else []
	return {'cartas': convert_cartas}

envia_cliente()

@route('/img/:filename', name='static')
def send_image(filename):
    return static_file(filename, root='./img/', mimetype='image/png')

run(host='localhost', port=int(argv[1]))
