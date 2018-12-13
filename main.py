import OpenGL 

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time, sys, math

def init():
	glClearColor(0.0,0.0,0.0,0.0)

def desenharChao():
	glPushMatrix()

	glBegin(GL_POLYGON)
	glColor3f (150.0, 0.0, 0.0)
	glVertex3f (-25, -25, 0.0)
	glColor3f (0.0, 150.0, 0.0)
	glVertex3f (-25, 25, 0.0)
	glColor3f (0.0, .0, 150.0)
	glVertex3f (25, 25, 0.0)
	glColor3f (150.0, 0.0, 150.0)
	glVertex3f (25, -25, 0.0)
	glEnd()
	
	glPopMatrix()

def desenharParede(v1x, v1y, v2x, v2y, cor, altura=10):
	glPushMatrix()

	glBegin(GL_POLYGON)
	glColor3f (cor[0], cor[1], cor[2])
	glVertex3f (v1x, v1y, 0.0)
	glVertex3f (v1x, v1y, altura)
	glVertex3f (v2x, v2y, altura)
	glVertex3f (v2x, v2y, 0.0)
	glEnd()
	
	glPopMatrix()

def desenhar_cenario():
	desenharChao()
	desenharParede(-25,-25,-25,25,[150,0,0])
	desenharParede(-25,25,25,25,[0,150,0])
	desenharParede(25,25,25,-25,[0,0,150])
	desenharParede(25,-25,-25,-25,[150,150,0])

def configurar_camera():
	# glRotatef(spin, 0.0, 0.0, 1.0)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	x,y,width,height = glGetDoublev(GL_VIEWPORT)
	gluPerspective(
		75, # field of view in degrees
		width/float(height or 1), # aspect ratio
		0.5, # near clipping plane
		100, # far clipping plane
	)

	ponto_visao = convert_esferica_r3()

	# and then the model view matrix
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(
		posicao[0],posicao[1],posicao[2], # eyepoint
		ponto_visao[0],ponto_visao[1],ponto_visao[2], # center-of-view
		0,0,1, # up-vector
	)

def convert_esferica_r3():
	x = 5 * math.sin(math.radians(angulo_visao[1])) * math.cos(math.radians(angulo_visao[0]))
	y = 5 * math.sin(math.radians(angulo_visao[1])) * math.sin(math.radians(angulo_visao[0]))
	z = 5 * math.cos(math.radians(angulo_visao[1]))

	x += posicao[0]
	y += posicao[1]
	z += posicao[2]

	return [x,y,z]

def depth():
	glDepthFunc(GL_LESS)
	glEnable(GL_DEPTH_TEST)

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	desenhar_cenario()

	depth()

	configurar_camera()
	
	glutSwapBuffers()

def movimentacao_mouse(x, y):
	global angulo_visao, pos_antiga, correcao_dy, correcao_dx, primeira_interacao

	if(is_mouse_hidden):

		if(primeira_interacao):
			pos_antiga = [x,y]
			primeira_interacao = False

		# calcular movimentacao do mouse
		dx = x - pos_antiga[0] + correcao_dx
		dy = y - pos_antiga[1] + correcao_dy

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
		pos_antiga = [x,y]
		correcao_dy = 0
		correcao_dx = 0

		# alteracao do angulo da camera conforme a movimentacao do mouse
		if(dx!=0 and dy!=0):
			angulo_visao[0] = (angulo_visao[0]-dx/sensibilidade_mouse)%360
			angulo_visao[1] = angulo_visao[1]+dy/sensibilidade_mouse

			if(angulo_visao[1] > 170):
				angulo_visao[1] = 170
			if(angulo_visao[1] < 10):
				angulo_visao[1] = 10

		# verificao da necessidade do correcao
		if(x > 600):
			glutWarpPointer( x-500 , y )
			correcao_dx = 500
		elif(x<100):
			glutWarpPointer( x+500 , y )
			correcao_dx = -500
		if(y > 600):
			glutWarpPointer( x , y-500 )
			correcao_dy = 500
		elif(y<100):
			glutWarpPointer( x , y+500 )
			correcao_dy = -500

	glutPostRedisplay()

# NAO E O IDEAL
def girarCenario():
	global spin

	spin = spin + 2.0
	if (spin > 360.0):
		spin = spin - 360.0
	glutPostRedisplay()

# Funcao de tratamento de teclado (teclas comuns)
def keyboard_CommomKeys(key, x, y):
	# print(ord(key))
	if(key == chr(27)): # ESCAPE
		sys.exit()
	if(key == chr(115)): # s
		girarCenario()
	if(key == chr(113)): # q
		show_mouse()
	glutPostRedisplay()

# Funcao de tratamento de teclado (teclas especiais)
def keyboard_SpecialKeys(key, x, y):
	global posicao

	vetor_frente = [0,0,0]
	vetor_frente[0] = tam_passo*math.cos(math.radians(angulo_visao[0]))
	vetor_frente[1] = tam_passo*math.sin(math.radians(angulo_visao[0]))
	vetor_direita = [0,0,0]
	vetor_direita[0] = tam_passo*math.cos(math.radians(angulo_visao[0]-90))
	vetor_direita[1] = tam_passo*math.sin(math.radians(angulo_visao[0]-90))

	if(key == GLUT_KEY_UP):
		posicao = soma_vetor_3d(posicao, vetor_frente)
	if(key == GLUT_KEY_DOWN):
		posicao = diff_vetor_3d(posicao, vetor_frente)
	if(key == GLUT_KEY_LEFT):
		posicao = diff_vetor_3d(posicao, vetor_direita)
	if(key == GLUT_KEY_RIGHT):
		posicao = soma_vetor_3d(posicao, vetor_direita)
	glutPostRedisplay()

def soma_vetor_3d(v1, v2):
	return [v1[0]+v2[0],v1[1]+v2[1],v1[2]+v2[2]]

def diff_vetor_3d(v1, v2):
	return [v1[0]-v2[0],v1[1]-v2[1],v1[2]-v2[2]]

def clique_mouse(button, state, x, y):
	global primeira_interacao

	if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
		hide_mouse()
		primeira_interacao = True
	glutPostRedisplay()

def hide_mouse():
	global is_mouse_hidden

	glutSetCursor(GLUT_CURSOR_NONE)
	is_mouse_hidden = True

def show_mouse():
	global is_mouse_hidden

	glutSetCursor(GLUT_CURSOR_INHERIT)
	is_mouse_hidden = False

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize (width, height)
	glutInitWindowPosition (100, 100)
	glutCreateWindow('Treino camera')
	init()
	glutDisplayFunc(display)
	glutKeyboardFunc(keyboard_CommomKeys)
	glutSpecialFunc(keyboard_SpecialKeys)
	glutMouseFunc(clique_mouse)
	glutPassiveMotionFunc(movimentacao_mouse)
	glutIdleFunc(display)
	glutMainLoop()

width = 700
height = 700

# variaveis utilizadas para movimentacao da camera
spin = 0.0
tam_passo = 0.5
posicao = [0,0,5]
pos_antiga = posicao
correcao_dx = 0
correcao_dy = 0
angulo_visao = [90.0,90.0]
sensibilidade_mouse = 20.0
is_mouse_hidden = False
primeira_interacao = False

main()