class Interface:
	"""
	Classe responsável pela interação com o utilizador,
	o seu único objetivo é recolher os dados de entrada
	do utilizador e envià-los para a classe Maquina que
	depois executa os cálculos.
	"""
	def __init__(self,maquina):
		self.maquina = maquina

	def execute(self):
		print("Escolha o cálculo a efetuar ( + - * / sqrt)")
		operacao: str = input("Operação: ")

		print("Introduza os valores: ")
		x: float = float(input("x="))

		y: float = 0 # A raíz quadrada só utiliza um valor que é x
		if operacao != "sqrt":
			y = float(input("y="))

		#Cálculo é feito pela classe Maquina
		resultado = self.maquina.execute(operacao, x, y)
		print(f"O resultado da operação é: {resultado}")



