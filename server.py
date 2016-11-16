import requests
import random
import json
import ast
from bottle   import run, get, post, view, request, redirect, route, static_file
from operator import itemgetter

global cartas, valores, naipes, h_cartas

naipes   = ['s', 'h', 'c', 'd']
cartas   = []
erros 	 = {}
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


# funcao para registrar os clientes no servidor
@get('/get_players/<porta>')
def get_players(porta):
	if porta not in players:
		players.append(porta)



@get('/distribuir_cartas')
def distribuir_cartas():
	if len(players) < 4 or len(players) > 26:
		erros.update({1: "Para distribuir cartas precisa ter entre 4 e 26 jogadores"})
		redirect('/')


	l = []
	for p in players:
		if not d_cartas.get(p):
			mao = get_cartas()
			d_cartas[p] = ast.literal_eval(mao)
			#print(mao)
			requests.get('http://localhost:' + p + '/recebe_cartas/' + mao)

			valor = comparar(d_cartas[p][0][0], d_cartas[p][1][0])
			l.append((p, valor))

	# a = comparar(d_cartas['8081'][0][0], d_cartas['8081'][1][0])
	# b = comparar(d_cartas['8082'][0][0], d_cartas['8082'][1][0])
	
	if len(l) > 1:
		# maior = max(l)
		l.sort(key = itemgetter(1), reverse = True)
		maior = l[0]

		print("Maior Carta: ", maior)
		distribuir_clientes()
		address = 'http://localhost:'+maior[0]+'/acordo'
		#print(address)
		requests.get(address)
	#else:
	#	print("Maior Carta: %d" % l[0][1])

	# print(l)
	
	redirect('/')


@get('/distribuir_clientes')
def distribuir_clientes():
	for p in players:
		requests.get('http://localhost:'+ p + '/recebe_clientes/'+ json.dumps(players))



def get_cartas():
	c1 = cartas.pop(0)
	c2 = cartas.pop(0)
	return json.dumps([c1, c2])


@get('/')
@view('index')
def index():
	erros_aux = erros.copy()
	erros.clear()
	return {'cartas': cartas, 'erros': erros_aux.values()}


@route('/img/:filename', name='static')
def send_image(filename):
    return static_file(filename, root='./img/', mimetype='image/png')


run(host='localhost', port=8080)
