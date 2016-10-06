import random
import requests
import json
from bottle import run, get, post, view, request, redirect, route, static_file

global cartas, valores, naipes

naipes   = ['s', 'h', 'c', 'd']
cartas   = []
valores  = [str(i) for i in range(2, 10)] + ['T', 'J', 'Q', 'K', 'A']
players  = []
d_cartas = {}


@get('/gerar_cartas')
def gera_cartas():
	if not cartas: # gerar cartas somente uma vez
		for i in naipes:
			for j in valores:
				cartas.append(j+i)
	redirect('/')


@get('/embaralhar_cartas')
def embaralhar_cartas():
	random.shuffle(cartas)
	redirect('/')


@get('/get_players/<porta>')
def get_players(porta):
	if porta not in players:
		players.append(porta)


@get('/distribuir_cartas')
def distribuir_cartas():
	for c in players:
		mao 		= get_cartas()
		d_cartas[c] = mao
		requests.get('http://localhost:' + c + '/recebe_cartas/' + mao)
	redirect('/')


def get_cartas():
	c1 = cartas.pop(0)
	c2 = cartas.pop(0)
	return json.dumps([c1, c2])


@get('/')
@view('index')
def index():
	return {'cartas': cartas}


@route('/img/:filename', name='static')
def send_image(filename):
    return static_file(filename, root='./img/', mimetype='image/png')


run(host='localhost', port=8080)
