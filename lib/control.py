from const.constants import * 
import pygame
from pygame.locals import *
from lib.pedido import *

class Control(object):

    def __init__(self):
        print 'Inicializando Control'
        self.pedidos = []
        self.robots = []
        self.salida_norte = [(89,6),(89,8),(89,10)]
        self.salida_noreste = [(89,15),(89,17),(89,19)]
        self.salida_sur = [(89,35),(89,37),(89,39)]
        self.salida_suroeste = [(89,25),(89,27),(89,29)]

    def agregarPedido(self,pedido):
        self.totalrobotlibres = len(self.robots)
        for r in self.robots:
            if r.state == 'libre':
                r.agregarRuta('ruta')
                r.state = 'ocupado'
                return
            else:
                self.totalrobotlibres = self.totalrobotlibres - 1
        if self.totalrobotlibres == 0:
            self.pedidos.append(pedido)
            print 'Pedido agregado a la cola'
        print 'Pedido agregado'

    def agregarRobot(self,robot):
        self.robots.append(robot)
        print 'Robot agregado'

    def dibujarPedidos(self):
        '''for producto in self.productos:
            x, y = producto
            nx, ny = x * NODE_SIZE, y * NODE_SIZE
            pygame.draw.rect(screen, color, 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE))'''
        print 'dibujar pedidos'

    def cambiarEstadoRobot(self,robot):
        print 'cambiar'

    def asignarPedidoRobot(self,nombre):
        if len(self.pedidos)>0:
            for r in self.robots:
                if r.nombre == nombre and r.state == 'libre':
                    r.agregarRuta('ruta')
                    r.state = 'ocupado'
                    self.pedidos.pop(0)
                    return
        else:
            print 'No hay pedidos en espera'