class Carta:
	def __init__(self, tipo, valor):
		self.tipo  = tipo
		self.valor = valor

	def __repr__(self):
		return str((self.valor, self.tipo))
