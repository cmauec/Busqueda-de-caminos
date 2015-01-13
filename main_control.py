 #!/usr/bin/env python

# Copyright (C) 2011 by Xueqiao Xu <xueqiaoxu@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys
import time
import datetime
import cPickle
import threading
import random
import pygame
import uuid

from pygame.locals import *
from const.constants import * 
from algo.astar import *

from ui.ui import *
from lib.robot import *
from lib.pedido import *
from lib.control import *


posicionRobot = [(4, 1), (6, 1), (8, 1), (4, 45), (6, 45), (8, 45)]


def CrearRobots(robots):
    listaRobots = [] 
    for n in range(robots):
        posicionRobotRandom = random.choice(posicionRobot)
        index_posicionRobotRandom = posicionRobot.index(posicionRobotRandom)
        posicionRobot.pop(index_posicionRobotRandom)
        robot = Robot(posicionRobotRandom, uuid.uuid4())
        listaRobots.append(robot)
    return listaRobots


class Client(object):
    
    def __init__(self, ui_path):

        self.ui = UI(ui_path)

        # Creamos robots
        self.robots = CrearRobots(6)
        '''self.robot = Robot((4, 1),'gina')
        self.robot_uno = Robot((4, 45),'mile')
        self.robot_dos = Robot((5, 1),'mauro')
        self.robot_3 = Robot((6, 45),'carlos')'''
         
        # Creacion del control del sistema
        self.control = Control(self.ui.nodes)
        
        # Agragamos robots al control
        for robot in self.robots:
            self.control.agregarRobot(robot)
        '''self.control.agregarRobot(self.robot)
        self.control.agregarRobot(self.robot_uno)
        self.control.agregarRobot(self.robot_dos)
        self.control.agregarRobot(self.robot_3)'''

        self.play_animation = False
                

        # general status
        self.status = ''


    def run(self):
        """
        Iniciamos el bucle principal
        """
        # handle events
        while self.status != EXIT:

            for event in pygame.event.get():
                if event.type == QUIT:
                    self._quit()
                elif event.type == KEYDOWN:
                    self._handle_keyboard(event)
            
            # Dibujamos el color de fondo para el mapa
            self.ui._draw_background()

            # Dibujamos el mapa inicial
            self.ui._draw_map_init()

            # Dibujamos las lineas separadoras de cada nodo
            #self.ui._draw_grid_lines()

            # Dibujamos todos los pedidos pendientes de entrega
            self.control.dibujarPedidos(self.ui.screen)

            # Dibuajamos la animacion del robot y notificamos al control cuando el robot finalizo su trabajo
            if self.play_animation:
                for robot in self.robots:
                    robot.dibujarRuta(self.ui.screen, self.ui.nodes)
                    # Dibuajamos al robot en una posicion y la comparamos con la posicion final del robot.
                    if  robot.RobotAnimarCamino(self.ui.screen) == (robot.source[0]+1,robot.source[1]):
                        self.control.quitarPedidoConcluido(robot.pedido_actual)
                        robot.notificacion_libre(self.control)


            '''if self.play_animation:
                self.robot_uno.dibujarRuta(self.ui.screen, self.ui.nodes)
                if  self.robot_uno.RobotAnimarCamino(self.ui.screen) == (self.robot_uno.source[0]+1,self.robot_uno.source[1]):
                    self.control.quitarPedidoConcluido(self.robot_uno.pedido_actual)
                    self.robot_uno.notificacion_libre(self.control)


            if self.play_animation:
                self.robot_dos.dibujarRuta(self.ui.screen, self.ui.nodes)
                if  self.robot_dos.RobotAnimarCamino(self.ui.screen) == (self.robot_dos.source[0]+1,self.robot_dos.source[1]):
                    self.control.quitarPedidoConcluido(self.robot_dos.pedido_actual)
                    self.robot_dos.notificacion_libre(self.control)


            if self.play_animation:
                self.robot_3.dibujarRuta(self.ui.screen, self.ui.nodes)
                if  self.robot_3.RobotAnimarCamino(self.ui.screen) == (self.robot_3.source[0]+1,self.robot_3.source[1]):
                    self.control.quitarPedidoConcluido(self.robot_3.pedido_actual)
                    self.robot_3.notificacion_libre(self.control)'''


            # Dibujamos a los robots en pantalla
            for robot in self.robots:
                robot.dibujarRobot(self.ui.screen)
            '''self.robot.dibujarRobot(self.ui.screen)
            self.robot_uno.dibujarRobot(self.ui.screen)
            self.robot_dos.dibujarRobot(self.ui.screen)
            self.robot_3.dibujarRobot(self.ui.screen)'''



                                  
            # update screen
            pygame.display.update()

            # control frame rate
            self.ui.clock.tick(FPS_LIMIT)



    def _quit(self):
        """Initiate termination
        """
        pygame.quit()
        raise SystemExit


    def _handle_keyboard(self, event):
        """Handle keyboard events
        """
        
        if event.key == K_SPACE:
            nombre = uuid.uuid4()
            self.pedido = Pedido(nombre)
            self.control.agregarPedido(self.pedido)
            self.play_animation = True 
            print self.pedido.nombre
        

        elif event.key == K_ESCAPE:
            self._quit()

       
if __name__ == '__main__':
   
    
    cur_path = os.path.abspath(os.path.dirname(__file__))
    ui_path = os.path.join(cur_path, 'ui')
    

    client = Client(ui_path)
    client.run()
