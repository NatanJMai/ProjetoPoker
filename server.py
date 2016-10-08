import random
import requests
import json
import ast
from bottle import run, get, post, view, request, redirect, route, static_file

global cartas, valores, naipes, h_cartas

naipes   = ['s', 'h', 'c', 'd']
cartas   = []
valores  = [str(i) for i in range(2, 10)] + ['T', 'J', 'Q', 'K', 'A']
players  = []
d_cartas = {}
h_cartas = {}


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

@get('/gerar_cartas')
def gera_cartas():
	hierarquia_cartas()
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
	l = []
	for c in players:
		if not d_cartas.get(c):
			mao = get_cartas()
			d_cartas[c] = ast.literal_eval(mao)
			requests.get('http://localhost:' + c + '/recebe_cartas/' + mao)

			valor = comparar(d_cartas[c][0][0], d_cartas[c][1][0])
			l.append((c, valor))

	# a = comparar(d_cartas['8081'][0][0], d_cartas['8081'][1][0])
	# b = comparar(d_cartas['8082'][0][0], d_cartas['8082'][1][0])
	
	if len(l) > 1:
		maior = max(l[0][1], l[1][1])
		print("Maior Carta: %d" % maior)
	else:
		print("Maior Carta: %d" % l[0][1])

	# print(l)

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
