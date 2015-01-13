from const.constants import * 
import pygame
from pygame.locals import *
import random

colorRobot = [(235,56,211),(255,109,5),(59,57,55),(36,90,240),(0,255,4),(49,18,204),(119,5,176)]
colorRobotTemp = []


class Robot(object):

    def __init__(self,source,nombre):
        #Punto donde sale el robot
        self.colorRandom = random.choice(colorRobot)
        self.index_colorRandom = colorRobot.index(self.colorRandom)
        colorRobot.pop(self.index_colorRandom)
        self.source = source
        self.state = 'libre'
        self.nombre = nombre
        self.path = []
        self.color = self.colorRandom 
        self.init = 0
        self.pos = 30
        self.mov_pos =0
        self.pedido_actual = None


    def dibujarRobot(self,screen):
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(screen, self.color, Rect(nx, ny, NODE_SIZE, NODE_SIZE))

    def agregarRuta(self,ruta,pedido):
        self.path = ruta
        self.pedido_actual = pedido
        

    def iniciarRuta(self):
        print 'Iniciar'

    def notificacion_libre(self,control):
        self.path = []
        self.state = 'libre'
        self.mov_pos = 0
        self.pedido_actual = None
        control.asignarPedidoRobot(self.nombre)


    def dibujarRuta(self, screen, nodes):
        if self.path:
            seg = [nodes[y][x].rect.center 
                    for (x, y) in self.path]
            pygame.draw.lines(screen, self.color, False,
                    seg, PATH_WIDTH)


    def BorrarRuta(self, screen, nodes):
        if self.path:
            seg = [nodes[y][x].rect.center 
                    for (x, y) in self.path]
            pygame.draw.lines(screen,(255,255,255) , False,
                    seg, PATH_WIDTH)


    def RobotAnimarCamino(self, screen):
        self.length_path = len(self.path)
        if self.mov_pos < self.length_path:
            self.source1 = self.path[self.mov_pos]
            x, y = self.source1
            nx, ny = x*NODE_SIZE, y*NODE_SIZE
            pygame.draw.rect(screen, self.color, Rect(nx, ny, NODE_SIZE, NODE_SIZE))
            self.mov_pos += 1
            return self.source1






    