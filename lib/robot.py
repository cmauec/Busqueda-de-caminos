from const.constants import * 
import pygame
from pygame.locals import *

class Robot(object):

    def __init__(self,source,nombre):
        #Punto donde sale el robot
        self.source = source
        self.state = 'libre'
        self.nombre = nombre

    def dibujarRobot(self,screen,color):
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(screen,color, Rect(nx, ny, NODE_SIZE, NODE_SIZE))

    def agregarRuta(self,ruta):
        print 'Ruta'

    def iniciarRuta(self):
        print 'Iniciar'

    def notificacion_libre(self,control):
        control.asignarPedidoRobot(self.nombre)