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


            if self.robots[0].play_animation  and self.robots[1].play_animation: 
                if (self.robots[0].direccionRobot('posterior') == 'arriba' and self.robots[1].direccionRobot('posterior') == 'abajo') or (self.robots[0].direccionRobot('posterior') == 'abajo' and self.robots[1].direccionRobot('posterior') == 'arriba'):
                    if self.robots[0].path_restante[1] == self.robots[1].path_restante[1]: #primer caso de choque

                        if self.robots[0].posicion_actual[0] in robot_move_right_wall:
                            self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0]+1, self.robots[0].posicion_actual[1] )
                            for i in range(TIEMPO_ESPERA_COLISION):
                                self.robots[0].path_restante.insert(0, self.robots[0].posicion_actual)     

                        elif self.robots[0].posicion_actual[0] in robot_move_left_wall:
                            self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0]-1, self.robots[0].posicion_actual[1])
                            for i in range(TIEMPO_ESPERA_COLISION):
                                self.robots[0].path_restante.insert(0, self.robots[0].posicion_actual)
                                
                        print 'Se van a chocar en la siguiente posicion'

                    elif (self.robots[0].path_restante[0] == self.robots[1].path_restante[1]) or (self.robots[0].path_restante[1] == self.robots[1].path_restante[0]):
                        if self.robots[0].posicion_actual[0] in robot_move_right_wall:
                            self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0]+1, self.robots[0].posicion_actual[1] )
                            for i in range(TIEMPO_ESPERA_COLISION):
                                self.robots[0].path_restante.insert(0, self.robots[0].posicion_actual)

                        elif self.robots[0].posicion_actual[0] in robot_move_left_wall:
                            self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0]-1, self.robots[0].posicion_actual[1])
                            for i in range(TIEMPO_ESPERA_COLISION):
                                self.robots[0].path_restante.insert(0, self.robots[0].posicion_actual)
                        print 'Se chocaron'

                elif (self.robots[0].direccionRobot('posterior') == 'derecha' and self.robots[1].direccionRobot('posterior') == 'izquierda') or (self.robots[0].direccionRobot('posterior') == 'izquierda' and self.robots[1].direccionRobot('posterior') == 'derecha'):
                    pass
                elif ((self.robots[0].esperandoProducto() and self.robots[1].direccionRobot('posterior') == 'abajo') or (self.robots[0].esperandoProducto() and self.robots[1].direccionRobot('posterior') == 'arriba')) or ((self.robots[1].esperandoProducto() and self.robots[0].direccionRobot('posterior') == 'abajo') or (self.robots[1].esperandoProducto() and self.robots[0].direccionRobot('posterior') == 'arriba')):                    
                    if self.robots[0].path_restante[1] == self.robots[1].path_restante[1]:
                        if self.robots[0].posicion_actual[0] in robot_move_right_wall:
                            self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0]+1, self.robots[0].posicion_actual[1] )

                        elif self.robots[0].posicion_actual[0] in robot_move_left_wall:
                            self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0]-1, self.robots[0].posicion_actual[1])
                        print 'Se van a chocar en la siguiente posicion2 '
                    elif (self.robots[0].path_restante[0] == self.robots[1].path_restante[1]) or (self.robots[0].path_restante[1] == self.robots[1].path_restante[0]):
                        if self.robots[0].posicion_actual[0] in robot_move_right_wall:
                            self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0]+1, self.robots[0].posicion_actual[1] )

                        elif self.robots[0].posicion_actual[0] in robot_move_left_wall:
                            self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0]-1, self.robots[0].posicion_actual[1])
                        print 'Se chocaron2'



            # if self.robots[0].posicion_actual == self.robots[1].posicion_actual:
            #     print 'los robots se chocaron'  
                '''print self.robots[0].posicion_actual
                print self.robots[1].posicion_actual                  
                self.robots[0].play_animation = False                
                index_posicion_actual = self.robots[0].path.index(self.robots[0].posicion_actual)
                punto_anterior_robot = self.robots[0].path[index_posicion_actual - 1]
                if self.robots[0].posicion_actual[1] > punto_anterior_robot[1]:
                    print 'robot desde arriba'
                    self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0], self.robots[0].posicion_actual[1] - 1)
                elif self.robots[0].posicion_actual[1] <punto_anterior_robot[1]: 
                    print 'robot desde abajo'
                    self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0], self.robots[0].posicion_actual[1] + 1)                

                if self.robots[0].posicion_actual[0] in robot_move_right_wall:
                    self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0]+1, self.robots[0].posicion_actual[1] )

                elif self.robots[0].posicion_actual[0] in robot_move_left_wall:
                    self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0]-1, self.robots[0].posicion_actual[1] )

                elif self.robots[0].posicion_actual[1] == robot_move_down_wall:
                    self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0], self.robots[0].posicion_actual[1] +1)

                elif self.robots[0].posicion_actual[1] == robot_move_up_wall:
                    self.robots[0].posicion_actual = (self.robots[0].posicion_actual[0], self.robots[0].posicion_actual[1] -1)
                self.robots[0].play_animation = True

                x, y = self.robots[0].posicion_actual
                nx, ny = x * NODE_SIZE, y * NODE_SIZE
                self.robots[0].rec_colision = pygame.Rect(nx, ny, NODE_SIZE, NODE_SIZE)'''


            '''if self.robots[1].rec_colision.colliderect(self.robots[0].rec_colision):
                print 'los robots se chocaron'  
                print self.robots[0].posicion_actual
                print self.robots[1].posicion_actual                  
                self.robots[1].play_animation = False                
                index_posicion_actual = self.robots[1].path.index(self.robots[1].posicion_actual)
                punto_anterior_robot = self.robots[1].path[index_posicion_actual - 1]
                if self.robots[1].posicion_actual[1] > punto_anterior_robot[1]:
                    print 'robot desde arriba'
                    self.robots[1].posicion_actual = (self.robots[1].posicion_actual[0], self.robots[1].posicion_actual[1] - 1)
                elif self.robots[1].posicion_actual[1] <punto_anterior_robot[1]: 
                    print 'robot desde abajo'
                    self.robots[1].posicion_actual = (self.robots[1].posicion_actual[0], self.robots[1].posicion_actual[1] + 1)                

                if self.robots[1].posicion_actual[0] in robot_move_right_wall:
                    self.robots[1].posicion_actual = (self.robots[1].posicion_actual[0]+1, self.robots[1].posicion_actual[1] )

                elif self.robots[1].posicion_actual[0] in robot_move_left_wall:
                    self.robots[1].posicion_actual = (self.robots[1].posicion_actual[0]-1, self.robots[1].posicion_actual[1] )

                elif self.robots[1].posicion_actual[1] == robot_move_down_wall:
                    self.robots[1].posicion_actual = (self.robots[1].posicion_actual[0], self.robots[1].posicion_actual[1] +1)

                elif self.robots[1].posicion_actual[1] == robot_move_up_wall:
                    self.robots[1].posicion_actual = (self.robots[1].posicion_actual[0], self.robots[1].posicion_actual[1] -1)
                self.robots[1].play_animation = True

                x, y = self.robots[1].posicion_actual
                nx, ny = x * NODE_SIZE, y * NODE_SIZE
                self.robots[1].rec_colision = pygame.Rect(nx, ny, NODE_SIZE, NODE_SIZE)'''
                



            if self.robots[0].play_animation == True:
                try: 
                    direccion_robot = self.robots[0].direccionRobot('posterior')
                    if not direccion_robot in ['arriba', 'derecha', 'abajo','izquierda','bloque 3']:
                        print self.robots[0].posicion_actual
                        print 'diagonal'
                except:
                    pass
            # print self.robots[0].posicion_actual
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
