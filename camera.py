import OpenGL 

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

from util import *

CAMERA_FRENTE = 1
CAMERA_TRAS = 2
CAMERA_DIREITA = 3
CAMERA_ESQUERDA = 4

class Camera():

	posicao = [0,0,5]
	pos_antiga = posicao
	correcao_dx = 0
	correcao_dy = 0
	angulo_visao = [5,90.0,90.0]
	sensibilidade_mouse = 20.0
	primeira_interacao = False
	vetor_frente = [0,0,0]
	vetor_direita = [0,0,0]

	def display(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		x,y,width,height = glGetDoublev(GL_VIEWPORT)
		gluPerspective(
			75, # field of view in degrees
			width/float(height or 1), # aspect ratio
			0.5, # near clipping plane
			100, # far clipping plane
		)

		ponto_visao = converter_esferica_r3(self.angulo_visao, self.posicao)

		# and then the model view matrix
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		gluLookAt(
			self.posicao[0],self.posicao[1],self.posicao[2], # eyepoint
			ponto_visao[0],ponto_visao[1],ponto_visao[2], # center-of-view
			0,0,1, # up-vector
		)

	def rotacionar_pelo_mouse(self, x, y):
		if(self.primeira_interacao):
			self.pos_antiga = [x,y]
			self.primeira_interacao = False

		# calcular movimentacao do mouse
		dx = x - self.pos_antiga[0] + self.correcao_dx
		dy = y - self.pos_antiga[1] + self.correcao_dy

		# revisao da correcao
		if(dx >= 400):
			dx-=500
		if(dx <= -400):
			dx+=500
		if(dy >= 400):
			dy-=500
		if(dy <= -400):
			dy+=500

		# configurando variaveis globais
		self.pos_antiga = [x,y]
		self.correcao_dy = 0
		self.correcao_dx = 0

		# alteracao do angulo da camera conforme a movimentacao do mouse
		if(dx!=0 and dy!=0):
			self.angulo_visao[1] = (self.angulo_visao[1]-dx/self.sensibilidade_mouse)%360
			self.angulo_visao[2] = self.angulo_visao[2]+dy/self.sensibilidade_mouse

			if(self.angulo_visao[2] > 170):
				self.angulo_visao[2] = 170
			if(self.angulo_visao[2] < 10):
				self.angulo_visao[2] = 10

		# verificao da necessidade do correcao
		if(x > 600):
			glutWarpPointer( x-500 , y )
			self.correcao_dx = 500
		elif(x<100):
			glutWarpPointer( x+500 , y )
			self.correcao_dx = -500
		if(y > 600):
			glutWarpPointer( x , y-500 )
			self.correcao_dy = 500
		elif(y<100):
			glutWarpPointer( x , y+500 )
			self.correcao_dy = -500

		# atualizar vetores de movimentacao
		self.vetor_frente[0] = math.cos(math.radians(self.angulo_visao[1]))
		self.vetor_frente[1] = math.sin(math.radians(self.angulo_visao[1]))
		self.vetor_direita[0] = math.cos(math.radians(self.angulo_visao[1]-90))
		self.vetor_direita[1] = math.sin(math.radians(self.angulo_visao[1]-90))

	def move(self, direcao, distancia):
		if(direcao == CAMERA_FRENTE):
			self.posicao = soma_vetor_3d(self.posicao, escala_vetor_3d(self.vetor_frente, distancia))
		elif(direcao == CAMERA_TRAS):
			self.posicao = soma_vetor_3d(self.posicao, escala_vetor_3d(self.vetor_frente, -distancia))
		elif(direcao == CAMERA_DIREITA):
			self.posicao = soma_vetor_3d(self.posicao, escala_vetor_3d(self.vetor_direita, distancia))
		elif(direcao == CAMERA_ESQUERDA):
			self.posicao = soma_vetor_3d(self.posicao, escala_vetor_3d(self.vetor_direita, -distancia))
