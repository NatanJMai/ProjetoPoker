import random
import requests
from sys import argv
from cartas import *
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
@view('index')
def index():
	return "Cliente, suas cartas sao: " + str(cartas)

envia_cliente()

run(host='localhost', port=int(argv[1]))
