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


class Client(object):
    
    def __init__(self, ui_path):

        self.ui = UI(ui_path)
        self.robot = Robot((4, 1),'gina', self.ui.node_color[SOURCE])
        self.robot_uno = Robot((4, 45),'mile',(15, 108, 125))
        self.robot_dos = Robot((5, 1),'mauro',(15, 108, 125))
        self.source = self.robot.source
        self.source_uno = self.robot_uno.source
        self.control = Control(self.ui.nodes)
        self.control.agregarRobot(self.robot)
        self.control.agregarRobot(self.robot_uno)
        self.control.agregarRobot(self.robot_dos)
        self.flag = 0


        self.init = 0
        self.init_uno = 0
        self.play_animation = False
        self.pos = 30
        self.mov_pos = 0
        self.mov_pos_uno = 0 
        self.targets_with_source = []
        self.targets_with_source_uno = []
        self.path = []
        self.path_uno = []
                

        # general status
        self.status = DRAWING
        self.editable = False
        self.erasing = False
        self.drag = None


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
            
            #Dibujamos el color de fondo para el mapa
            self.ui._draw_background()
            #Dibujamos el mapa inicial
            self.ui._draw_map_init()
            #Dibujamos las lineas separadoras de cada nodo
            #self.ui._draw_grid_lines()
            #self.pedido.dibujarProductos(self.ui.screen,self.ui.node_color[TARGET])
            #self.pedido_uno.dibujarProductos(self.ui.screen,(250,154,0))
            self.robot.dibujarRobot(self.ui.screen)
            self.robot_uno.dibujarRobot(self.ui.screen)
            self.robot_dos.dibujarRobot(self.ui.screen)
            self.control.dibujarPedidos(self.ui.screen)
            self.robot.dibujarRuta(self.ui.screen, self.ui.nodes)
            #self.control.dibujarPedidos()
            #self._draw_source()
            #self._draw_target_path()
            #self._draw_path()
            self.length_path = len(self.targets_with_source)
            self.length_path_uno = len(self.targets_with_source_uno) #ve cuantos targets tiene la trayectoria 
            #punto verde dinamico
            if self.play_animation:
                if self.init == 0:    #para que el retardo en la animacion se ejecute a  partir del segundo ciclo
                    time.sleep(0.5)
                if self.mov_pos < self.length_path:
                        self.source1 = self.targets_with_source[self.mov_pos]
                        x, y = self.source1
                        nx, ny = x*NODE_SIZE, y*NODE_SIZE
                        pygame.draw.rect(self.ui.screen, self.ui.node_color[SOURCE], Rect(nx, ny, NODE_SIZE, NODE_SIZE))
                        self.mov_pos += 1
            self.init += self.init

            #punto dinamico para el robot dos
            if self.play_animation:
                if  self.init_uno == 0:    #para que el retardo en la animacion se ejecute a  partir del segundo ciclo
                    time.sleep(0.5)
                if self.mov_pos_uno < self.length_path_uno:
                        self.source1_uno = self.targets_with_source_uno[self.mov_pos_uno]
                        x, y = self.source1_uno
                        nx, ny = x*NODE_SIZE, y*NODE_SIZE
                        pygame.draw.rect(self.ui.screen, (15,108,125), Rect(nx, ny, NODE_SIZE, NODE_SIZE))
                        self.mov_pos_uno += 1
            self.init_uno += self.init_uno
            
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

            
        elif event.key == K_r: 
            print self.robot.state
            print self.robot_uno.state
            print self.robot_dos.state
            print self.control.pedidos

        elif event.key == K_s: 
            self.robot.state = 'libre'
            self.robot.notificacion_libre(self.control)

        elif event.key == K_t:
                  
            self.p1 = self.control.pedidosDibujar[0]
            self.control.quitarPedidoConcluido(self.p1)

        elif event.key == K_y:
            print self.robot.path



        elif event.key == K_ESCAPE:
            self._quit()

    def _draw_source(self):
        """Source and target nodes are drawed on top of other nodes.
        """

        #para dibujar punto de salida del robot dos
        x1, y1 = self.salida_uno
        nx1, ny1 = x1 * NODE_SIZE, y1 * NODE_SIZE
        pygame.draw.rect(self.ui.screen, (15, 108, 125), 
                Rect(nx1, ny1, NODE_SIZE, NODE_SIZE)) 

    def _draw_target_path(self):
        """Source and target nodes are drawed on top of other nodes.
        """
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(self.ui.screen, self.ui.node_color[SOURCE], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE)) 
        #dibujando la trayectoria del robot uno
        for target in self.targets_with_source:
            x, y = target
            nx, ny = x * NODE_SIZE, y * NODE_SIZE
            pygame.draw.rect(self.ui.screen, self.ui.node_color[TARGET_PATH_COLOR], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE))

        #dibujando la trayectoria del robot dos
        ORANGE = (242,196, 131)
        for target in self.targets_with_source_uno:
            x, y = target
            nx, ny = x * NODE_SIZE, y * NODE_SIZE
            pygame.draw.rect(self.ui.screen, ORANGE, 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE))

    def _draw_path(self):
        if self.path:
            seg = [self.ui.nodes[y][x].rect.center 
                    for (x, y) in self.path]
            pygame.draw.lines(self.ui.screen, Color(PATH_COLOR), False,
                    seg, PATH_WIDTH)

        if self.path_uno:
            seg = [self.ui.nodes[y][x].rect.center 
                    for (x, y) in self.path_uno]
            pygame.draw.lines(self.ui.screen, (204,189,167), False,
                    seg, PATH_WIDTH)

    def _reset(self):
        """Reset all nodes to be NORMAL and clear the node infos
        """
        self.path = []
        for row in self.nodes:
            for node in row:
                node.status = NORMAL
                node.f = None
                node.g = None
                node.h = None
                node.parent = None

    def _reset_except_block(self):
        """Same as _reset, but does not clear the blocked nodes
        """
        self.path = []
        for row in self.ui.nodes:
            for node in row:
                if node.status != BLOCKED:
                    node.status = NORMAL
                node.f = None
                node.g = None
                node.h = None
                node.parent = None

    def _get_str_map(self,sourceA,targetA):
        """Generate a string represented map from the current nodes' status.
        """
        final_str = []
        for row in self.ui.nodes:
            str = []
            for node in row:
                if node.pos == sourceA:
                    str.append(SOURCE)
                elif node.pos == targetA :
                    str.append(TARGET)
                else: 
                    str.append(node.status)
            str.append('\n')
            final_str.append(''.join(str))
        return ''.join(final_str)

    
if __name__ == '__main__':
   
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ha:p:', ['help'])
        for o, a in opts:
            if o in ('-h', '--help'):
                print_help()
                raise SystemExit
           
    except (getopt.GetoptError, ValueError):
        print 'Argumentos invalidos\n'
        print_help()
        raise SystemExit
    cur_path = os.path.abspath(os.path.dirname(__file__))
    ui_path = os.path.join(cur_path, 'ui')
    

    client = Client(ui_path)
    client.run()
