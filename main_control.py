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
 
posicionRobot = [
                    #Arriba
                    #fila 1
                    (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1),
                    (15, 1), (16, 1), (17, 1), (18, 1), (19, 1), (20, 1), (21, 1), (22, 1), (23, 1), (24, 1),
                    (25, 1), (26, 1), (27, 1), (28, 1), (29, 1), (30, 1), (31, 1), (32, 1), (33, 1), (34, 1),
                    (35, 1), (36, 1), (37, 1), (38,1),(39,1),(40,1),
                    #fila 2
                    (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2),
                    (15, 2), (16, 2), (17, 2), (18, 2), (19, 2), (20, 2), (21, 2), (22, 2), (23, 2), (24, 2),
                    (25, 2), (26, 2), (27, 2), (28, 2), (29, 2), (30, 2), (31, 2), (32, 2), (33, 2), (34, 2),
                    (35, 2), (36, 2), (37, 2), (38, 2), (39, 2), (40, 2), (41, 2), (42, 2), (43, 2), (44, 2),
                    (45, 2), (46, 2), (47, 2), (48, 2), (49, 2), (50, 2), (51, 2), (52, 2), (53, 2), (54, 2),
                    (55, 2), (56, 2), (57, 2), (58, 2), (59, 2), (60, 2), (61, 2), (62, 2), (63, 2), (64, 2),
                    (65, 2), (66, 2), (67, 2), (68, 2), (69, 2), (70, 2), (71, 2), (72, 2), (73, 2), (74, 2),
                    (75, 2), (76, 2), (77, 2), (78, 2), (79, 2),
                    #Abajo
                    #fila 1
                    (5, 44),(6,44),(7,44),(8,44),(9,44),(10, 44),(11,44),(12,44),(13,44),(14,44),
                    (15, 44),(16,44),(17,44),(18,44),(19,44),(20, 44),(21,44),(22,44),(23,44),(24,44),
                    (25, 44), (26, 44), (27, 44), (28, 44), (29, 44), (30, 44), (31, 44), (32, 44), (33, 44), (34, 44),
                    (35, 44), (36, 44), (37, 44), (38, 44), (39,44),
                    #fila 2
                    (5, 43),(6,43),(7,43),(8,43),(9,43),(10, 43),(11,43),(12,43),(13,43),(14,43),
                    (15, 43),(16,43),(17,43),(18,43),(19,43),(20, 43),(21,43),(22,43),(23,43),(24,43),
                    (25, 43), (26, 43), (27, 43), (28, 43), (29, 43), (30, 43), (31, 43), (32, 43), (33, 43), (34, 43),
                    (35, 43), (36, 43), (37, 43), (38, 43), (39,43), (40, 43), (41, 43), (42, 43), (43, 43), (44, 43),
                    (45, 43), (46, 43), (47, 43), (48, 43), (49, 43), (50, 43), (51, 43), (52, 43), (53, 43), (54, 43),
                    (55, 43), (56, 43), (57,43), (58, 43), (59, 43), (60, 43), (61, 43), (62, 43), (63, 43), (64, 43),
                    (65, 43), (66, 43), (67, 43), (68, 43), (69, 43), (70, 43), (71, 43), (72, 43), (73, 43), (74, 43),
                    (75, 43), (76, 43), (77, 43), (78, 43), (79, 43),
                ]
#posicionRobot = [(1, 1), (1, 1)]


def CrearRobots(robots):
    '''Creamos una lista de robots. Parametro robot indica cuantos robots creamos'''
    listaRobots = [] 
    for n in range(robots):
        posicionRobotRandom = random.choice(posicionRobot)      
        index_posicionRobotRandom = posicionRobot.index(posicionRobotRandom)
        posicionRobot.pop(index_posicionRobotRandom)
        robot = Robot(posicionRobotRandom, uuid.uuid4())
        canastaA = CanastaRobot('A', 1) #1 - arriba
        canastaB = CanastaRobot('B', 2) #2 - der
        canastaC = CanastaRobot('C', 3) #3 - izq
        canastaD = CanastaRobot('D', 4) #4 - abajo
        robot.canastas.append(canastaA)
        robot.canastas.append(canastaB)
        robot.canastas.append(canastaC)
        robot.canastas.append(canastaD)
        listaRobots.append(robot)
    return listaRobots

def CrearRobot():
    '''Creamos un robot dinamicamente'''
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
        self.robots = CrearRobots(221)
             
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
        while self.status != EXIT:
            # manejamos eventos de la apliacion
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
            # self.ui._draw_grid_lines()

            # Movemos a los robots
            self.control.moverRobots(self.ui.screen)

            # Mdibujamos foto
            self.control.show_photo(self.ui.screen)

            # Dibujamos a los robots
            for robot in self.robots:
                robot.dibujarRobotMensaje(self.ui.screen)

            if self.control.letras < 5:
                self.control.photo = True
                                                 
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
        """Handle keyboard event
        """

        if event.key == K_g:
            pygame.mixer.music.load("m.wav")                        
            pygame.mixer.music.play(-1)
            self.control.agregarPuntoLetra()

        elif event.key == K_m:
            print letras
            for r in self.robots:
                print r.path_restante


        elif event.key == K_ESCAPE:
            self._quit()



       
if __name__ == '__main__':
   
    
    cur_path = os.path.abspath(os.path.dirname(__file__))
    ui_path = os.path.join(cur_path, 'ui')
    

    client = Client(ui_path)
    client.run()
