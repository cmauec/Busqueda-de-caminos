from const.constants import * 
import pygame
from pygame.locals import *
import random

colorRobot = [(235,56,211),(255,109,5),(59,57,55),(36,90,240),(0,255,4),(49,18,204),(119,5,176)]
colorRobotTemp = []
pared_izq = (2,10,16,22,28,34,40,46,52,58,64,70,76,82) #Posiciones donde existe pared a la izq
pared_der = (6,12,18,24,30,36,42,48,54,60,66,74,78)   #Posiciones donde existe pared a la der
pared_arriba = 5   #Posiciones donde existe pared arrib
pared_abajo = 40    #Posiciones donde existe pared abaj


class Robot(object):

    def __init__(self,source,nombre):
        #Punto donde sale el robot
        self.colorRandom = random.choice(colorRobot)
        self.index_colorRandom = colorRobot.index(self.colorRandom)
        colorRobot.pop(self.index_colorRandom)
        self.source = source
        self.state = 'libre'
        self.esperando_producto = False
        self.esperando_robot = False
        self.robot_choque = None       #Es el nombre del robot al que tiene que esperar que pase para poner en accion al robot q esta esperando 
        self.tipo_choque = None      #Almacenamos el tipo de choque 
        self.nombre = nombre    
        self.path = []
        self.path_restante = []
        self.coordenadas_producto = []     #es el punto del camino no el de la pared
        self.color = self.colorRandom 
        self.init = 0
        self.pos = 30
        self.mov_pos = 0
        self.pedido_actual = None
        self.play_animation = False
        self.posicion_actual = source
        # rectangulo delimitador para colisones
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        self.rec_colision = pygame.Rect(nx, ny, NODE_SIZE, NODE_SIZE)
        #self.salida = None
        

    def dibujarRobot(self,screen):
        x, y = self.posicion_actual
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(screen, self.color, Rect(nx, ny, NODE_SIZE, NODE_SIZE))
       
    def agregarRuta(self,ruta,pedido):
        self.path = ruta
        self.path_restante = list(self.path)
        self.pedido_actual = pedido

    def play(self):
        self.play_animation = True

    def stop(self):
        self.play_animation = False

    def notificacion_libre(self,control):
        self.path = []
        self.state = 'libre'
        self.posicion_actual = self.source
        self.mov_pos = 0
        self.pedido_actual = None
        self.play_animation = False
        self.robot_choque = None
        self.tipo_choque = None
        #self.stop()
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


    def Mover(self):
        # Si las dos funciones son verdaderas - el robot camina, si esperando producto es falso (no hay productos para recoger) - el robot no camina (porq una de las condiciones no se cumple).
        if self.play_animation and not self.esperando_producto and not self.esperando_robot: 
            self.length_path = len(self.path_restante)
            if  self.length_path>0:
                self.mov_pos += 1
                self.path_restante.pop(0)
                try:
                    self.posicion_actual = self.path_restante[0]
                except:
                    self.posicion_actual = self.source
                x, y = self.posicion_actual
                nx, ny = x * NODE_SIZE, y * NODE_SIZE
                self.rec_colision = pygame.Rect(nx, ny, NODE_SIZE, NODE_SIZE).inflate(NODE_SIZE*2,NODE_SIZE*2)

   
    def estadoEsperandoProducto(self):
        self.esperando_producto = False






        








    