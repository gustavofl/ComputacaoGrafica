import OpenGL 

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys, math
import pygame
import numpy

from PIL import Image
from camera import *
from util import *
from cenario_1 import *

def init():
	glClearColor(0.0,0.0,0.0,0.0)

'''
def carregar_textura(filename):
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.int8)

    #width = textureSurface.get_width()
    #height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)#habilita textura 2D
    textID = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D,textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)    
    

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    
    return textID
'''

def carregar_textura(textura):

        textureSurface = pygame.image.load(textura) #carrega imagem da textura
        textureData = pygame.image.tostring(textureSurface,"RGBA",1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()

        glEnable(GL_TEXTURE_2D)#habilita textura 2D
        texid = glGenTextures(1)#ID da textura

        glBindTexture(GL_TEXTURE_2D,texid)
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,textureData)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)


        return texid

def depth():
	glDepthFunc(GL_LESS)
	glEnable(GL_DEPTH_TEST)

def display():
        
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	textura = carregar_textura('parede_256px.png')
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D,textura)
	cenario.desenhar_cenario()
	glDisable(GL_TEXTURE_2D)

	depth()

	# analisar as teclas pressionadas no teclado e realizar alguma acao
	operacoes_teclado()

	camera.display()
	
	glutSwapBuffers()

# Funcao de tratamento de teclado (teclas comuns)
def operacoes_teclado():
	if(keybuffer[27]): # ESCAPE
		sys.exit()
		
	if(keybuffer[ord('q')]):
		show_mouse()

	if(keybuffer[ord('a')]):
		camera.move(CAMERA_ESQUERDA, tam_passo)
	if(keybuffer[ord('s')]):
		camera.move(CAMERA_TRAS, tam_passo)
	if(keybuffer[ord('d')]):
		camera.move(CAMERA_DIREITA, tam_passo)
	if(keybuffer[ord('w')]):
		camera.move(CAMERA_FRENTE, tam_passo)

	glutPostRedisplay()

def movimentacao_mouse(x, y):
	if(is_mouse_hidden):
		camera.rotacionar_pelo_mouse(x,y)

	glutPostRedisplay()

def clique_mouse(button, state, x, y):
	if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
		hide_mouse()
		camera.primeira_interacao = True
	glutPostRedisplay()

def hide_mouse():
	global is_mouse_hidden

	glutSetCursor(GLUT_CURSOR_NONE)
	is_mouse_hidden = True

def show_mouse():
	global is_mouse_hidden

	glutSetCursor(GLUT_CURSOR_INHERIT)
	is_mouse_hidden = False

def key_pressed(key, x, y):
	# print(ord(key))
	keybuffer[ord(key)] = True
	glutPostRedisplay()

def key_up(key, x, y):
	keybuffer[ord(key)] = False
	glutPostRedisplay()

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize (width, height)
	glutInitWindowPosition (100, 100)
	glutCreateWindow('Treino camera')
	init()
	glutDisplayFunc(display)
	glutKeyboardFunc(key_pressed)
	glutKeyboardUpFunc(key_up)
	glutMouseFunc(clique_mouse)
	glutPassiveMotionFunc(movimentacao_mouse)
	glutIdleFunc(display)
	glutMainLoop()

width = 700
height = 700

tam_passo = 0.3
is_mouse_hidden = False

# buffer com as teclas pressionadas do teclado
keybuffer = [False for i in range(256)]

camera = Camera()
cenario = Cenario_1()

main()
