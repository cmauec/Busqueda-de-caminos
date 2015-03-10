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
from threading import Timer



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

def CrearRobot():
    try: 
        posicionRobotRandom = random.choice(posicionRobot)
        index_posicionRobotRandom = posicionRobot.index(posicionRobotRandom)
        posicionRobot.pop(index_posicionRobotRandom)
        robot = Robot(posicionRobotRandom, uuid.uuid4())
        return robot 
    except:
        return False




class Client(object):
    
    def __init__(self, ui_path):

        self.ui = UI(ui_path)

        # Creamos robots
        self.robots = CrearRobots(2)
             
        # Creacion del control del sistema
        self.control = Control(self.ui.nodes)
        
        # Agragamos robots al control
        for robot in self.robots:
            self.control.agregarRobot(robot)
                

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
            self.ui._draw_grid_lines()

            # Dibujamos todos los pedidos pendientes de entrega
            self.control.dibujarPedidos(self.ui.screen)


            self.robots_movimiento = []
            self.robots_alerta = []
            self.robots_choque =[]   #Es el vector donde entran los robots que con seguridad se van a chocar
            for robot in self.robots:
                if robot.play_animation:
                    self.robots_movimiento.append(robot)
            self.robots_temporal = self.robots_movimiento[1:]
            for robot0 in self.robots_movimiento:
                for robot1 in self.robots_temporal:
                    comparacion = posibleChoque(robot0.posicion_actual, robot1.posicion_actual)
                    if OpcionesChoque.has_key(comparacion):                        
                        if 1 in comparacion or -1 in comparacion:
                            if robot0.path_restante[0] == robot1.path_restante[1] and robot0.path_restante[1] == robot1.path_restante[0] :
                                print 'Se chocaron'
                        elif 2 in comparacion or -2 in comparacion:
                            if robot0.path_restante[1] == robot1.path_restante[1]:
                                print 'Se van a chocar'

                    try: 
                        self.robots_temporal.pop(0)
                    except:
                        pass


            '''for robot in self.robots:
                if len(robot.coordenadas_producto) > 0:
                    if robot.posicion_actual == robot.coordenadas_producto[0]:
                        robot.esperando_producto = True
                        robot.coordenadas_producto.pop(0)
                        Timer(2,robot.estadoEsperandoProducto).start()   #Hace que el robot se detenga 3 segundos para recoger roductos'''



            # Dibuajamos la animacion del robot
            for robot in self.robots:
                robot.dibujarRuta(self.ui.screen, self.ui.nodes)
                robot.dibujarRobot(self.ui.screen)
                if robot.play_animation == True:
                    robot.Mover()    
                if robot.posicion_actual == (robot.source[0]+1,robot.source[1]):
                    # al finalizar el recorrido imprime los puntos de la trayectoria
                    #print robot.path
                    self.control.quitarPedidoConcluido(robot.pedido_actual)
                    robot.notificacion_libre(self.control)
                                                 
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
            print self.pedido.nombre


        elif event.key == K_s:
            self.robotNuevo = CrearRobot()
            if self.robotNuevo:
                self.robots.append(self.robotNuevo)
                self.control.agregarRobot(self.robotNuevo)


        elif event.key == K_a:
            for robot in self.robots:
                if robot.state == 'libre':
                    indexRobot = self.robots.index(robot)
                    self.robots.pop(indexRobot)
                    posicionRobot.append(robot.source)
                    self.control.quitarRobot(robot)
                    colorRobot.append(robot.color)
                    return


        elif event.key == K_e:
            for robot in self.robots:
                robot.stop()

        elif event.key == K_r:
            for robot in self.robots:
                robot.play()


        elif event.key == K_t:
            print self.robots[0].direccionRobot('posterior')
            print self.robots[0].posicion_actual
                
             

        

        elif event.key == K_ESCAPE:
            self._quit()



       
if __name__ == '__main__':
   
    
    cur_path = os.path.abspath(os.path.dirname(__file__))
    ui_path = os.path.join(cur_path, 'ui')
    

    client = Client(ui_path)
    client.run()
