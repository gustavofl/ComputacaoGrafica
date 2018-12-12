import OpenGL 

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time, sys

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

	# and then the model view matrix
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(
		posicao[0],posicao[1],posicao[2], # eyepoint
		ponto_visao[0],ponto_visao[1],ponto_visao[2], # center-of-view
		0,0,1, # up-vector
	)

def depth():
	glDepthFunc(GL_LESS)
	glEnable(GL_DEPTH_TEST)

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	desenhar_cenario()

	depth()

	configurar_camera()
	
	glutSwapBuffers()

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
	glutPostRedisplay();

# Funcao de tratamento de teclado (teclas especiais)
def keyboard_SpecialKeys(key, x, y):
	if(key == GLUT_KEY_UP):
		posicao[1] += tam_passo
		ponto_visao[1] += tam_passo
	if(key == GLUT_KEY_DOWN):
		posicao[1] -= tam_passo
		ponto_visao[1] -= tam_passo
	if(key == GLUT_KEY_LEFT):
		posicao[0] -= tam_passo
		ponto_visao[0] -= tam_passo
	if(key == GLUT_KEY_RIGHT):
		posicao[0] += tam_passo
		ponto_visao[0] += tam_passo
	glutPostRedisplay();

def movimentacao_mouse(x, y):
	if(is_mouse_hidden):
		if(x > 600):
			glutWarpPointer( x-500 , y )
		elif(x<100):
			glutWarpPointer( x+500 , y )
		if(y > 600):
			glutWarpPointer( x , y-500 )
		elif(y<100):
			glutWarpPointer( x , y+500 )
	glutPostRedisplay();

def clique_mouse(button, state, x, y):
	if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
		hide_mouse()
	glutPostRedisplay();

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
	glutInitWindowSize (700, 700); 
	glutInitWindowPosition (100, 100);
	glutCreateWindow('Treino camera')
	init()
	glutDisplayFunc(display)
	glutKeyboardFunc(keyboard_CommomKeys)
	glutSpecialFunc(keyboard_SpecialKeys)
	glutMouseFunc(clique_mouse)
	glutPassiveMotionFunc(movimentacao_mouse)
	glutIdleFunc(display)
	glutMainLoop()

spin = 0.0
tam_passo = 0.5
posicao = [0,0,5]
ponto_visao = [0,5,5]
is_mouse_hidden = False

main()