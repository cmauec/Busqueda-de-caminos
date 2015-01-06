from const.constants import * 
import pygame
from pygame.locals import *

coloresRuta = [(207,23,23),(168,19,19),(133,15,15),(94,10,10),(59,6,6),(230,39,39),(237,111,111),(235,75,75),(242,148,148)]


class Robot(object):

    def __init__(self,source,nombre, color):
        #Punto donde sale el robot
        self.source = source
        self.state = 'libre'
        self.nombre = nombre
        self.path = []
        self.color = color 


    def dibujarRobot(self,screen):
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(screen, self.color, Rect(nx, ny, NODE_SIZE, NODE_SIZE))

    def agregarRuta(self,ruta):
        self.path = ruta
        

    def iniciarRuta(self):
        print 'Iniciar'

    def notificacion_libre(self,control):
        control.asignarPedidoRobot(self.nombre)


    def dibujarRuta(self, screen, nodes):
        if self.path:
            seg = [nodes[y][x].rect.center 
                    for (x, y) in self.path]
            pygame.draw.lines(screen, self.color, False,
                    seg, PATH_WIDTH)

    