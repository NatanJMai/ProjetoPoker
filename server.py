import random
from cartas import *
from bottle import run, get, post, view, request, redirect, route, static_file

global cartas, valores, tipos

cartas  = []
tipos   = ['Paus', 'Espadas', 'Copas', 'Ouros']
valores = [str(i) for i in range(1,11)] + ['J', 'Q', 'K']

@get('/gerar_cartas')
def gera_cartas():
	for i in tipos:
		for j in valores:
			cartas.append(Carta(i, j))
	redirect('/')

@get('/embaralhar_cartas')
def embaralhar_cartas():
	random.shuffle(cartas)
	redirect('/')


@get('/')
@view('index')
def index():
	return {'cartas': cartas}
    

@route('/img/:filename', name='static')
def send_image(filename):
    return static_file(filename, root='./img/', mimetype='image/png')


run(host='localhost', port=8080)