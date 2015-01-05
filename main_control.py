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
        self.robot = Robot((4, 1),'gina')
        self.robot_uno = Robot((4, 45),'mile')
        self.robot_dos = Robot((5, 1),'mauro')
        self.source = self.robot.source
        self.source_uno = self.robot_uno.source
        self.control = Control()
        self.control.agregarRobot(self.robot)
        self.control.agregarRobot(self.robot_uno)
        self.control.agregarRobot(self.robot_dos)
        self.flag = 0


        self.init = 0
        self.init_uno = 0
        self.play_animation = False
        self.pos = 30
        self.mov_pos = 0
        self.mov_pos_uno = 0 #inicio robot dos
        #este punto representa el lugar a donde regresa el robot despues de dejar los productos (self.source_end)
        self.source_end = (4,1)
        self.salida_norte = [(89,6),(89,8),(89,10)]
        self.salida_noreste = [(89,15),(89,17),(89,19)]
        self.salida_sur = [(89,35),(89,37),(89,39)]
        self.salida_suroeste = [(89,25),(89,27),(89,29)]
        #si el robot esta en la parte de arriba tendra como salida al norte o al noreste
        if self.source[1]<8:
            self.salida = self.salida_norte+self.salida_noreste
            self.salida = random.choice(self.salida)
        #si el robot esta en la parte inferior tendra como salida al sur o suroeste
        elif self.source[1]>37:
            self.salida = self.salida_sur+self.salida_suroeste
            self.salida = random.choice(self.salida)
        #genera punto de salida del robot dos    
        if self.source_uno[1]<8:
            self.salida_uno = self.salida_norte+self.salida_noreste
            self.salida_uno = random.choice(self.salida_uno)
        elif self.source_uno[1]>37:
            self.salida_uno = self.salida_sur+self.salida_suroeste
            self.salida_uno = random.choice(self.salida_uno)
        self.targets_with_source = []
        self.targets_with_source_uno = []
        #self.lenght_targets = len(self.targets)
        self.path = []
        self.path_uno = []
        #nos sirve para crear la sombra de los targets
        self.move_right_wall = (1,9,15,21,27,33,39,45,51,57,63,69,75,81) #aumentamos en x uno
        self.move_left_wall = (7,13,19,25,31,37,43,49,55,61,67,73,79) #disminuimos en x uno
        self.move_down_wall = 4 #aumentamos en y uno
        self.move_up_wall = 41 #disminuimos en Y uno
        #parametro para tomar en cuenta targets solo a lo largo de la pared.
        self.wall_is_vertical = range(8,38)
        #coordenadas para dividir el mapa en secciones verticalmente, son las coordenadas de la pared del centro
        self.sections = [(1,8),(9,14),(15,20),(21,26),(27,32),(33,38),(39,44),(45,50),(51,56),(57,62),(63,68),(69,74),(75,80),(81,82)]
        

        # general status
        self.status = DRAWING
        self.editable = False
        self.erasing = False
        self.drag = None

        

    def gen_path(self, targets):
        #generamos la trayectoria pasando por la sombra de los targets
        path = []
        for t in targets:
            if t[1] in self.wall_is_vertical:
                if t[0] in self.move_right_wall:
                    t = (t[0]+1,t[1])
                elif t[0] in self.move_left_wall:
                    t = (t[0]-1,t[1]) 
            else:
                if t[1] == self.move_down_wall:
                    t = (t[0],t[1]+1)
                elif t[1] == self.move_up_wall:
                    t = (t[0],t[1]-1)
             
            path.append(t)
        return path


    # Para ordenar los targets de menor a mayor (por seccion)    
    def gen_path_order(self, targets):
        path = []
        for s in self.sections:
            path_section = []
            for t in targets:
                if t[0] in range(s[0], s[1]+1):
                    try:
                        #path.append(t)
                        path_section.append(t)
                    except:  
                        pass
            if len(path)>0:
                path_section.insert(0,path[-1]) #hace que el ultimo punto de la seccion sea el primer punto de la siguiente seccion
            path_section = self.path_order_distance(path_section)
            path = path +path_section
        return path

    def path_order_distance(self, targets):
        #haciendo el sol con cada target
        targets_order = []
        temp = []
        targets_temp = []
        for t in targets:
            targets_temp.append(t)
        for t1 in targets:
            if len(targets_order) == 0: 
                element = targets_temp[0]
                targets_order.append(targets_temp[0])
                targets_temp.remove(element)
            else:
                element = targets_order[-1]
            temp = []
            targets_temp_order = []
            for t2 in targets_temp:
                targets_temp_order.append(t2)
            if len(targets_temp_order)>0:
                for t in targets_temp_order:
                    nodes_map_raw = self._get_str_map(element, t)
                    try:
                        a = AStar(nodes_map_raw)
                        for i in a.step():
                            pass
                        v1 = len(a.path) #tomando el tamano de la trayectoria
                    except:
                        v1 = 0
                    t = (v1,t[0],t[1]) # tomando el tamano de la distancia menor y su coordenada para tomar como siguiente punto de inicio (sol)
                    temp.append(t)
                    temp.sort()
                element_near = (temp[0][1],temp[0][2])
                targets_order.append(element_near)
                targets_temp.remove(element_near)
        return targets_order


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
            self.robot.dibujarRobot(self.ui.screen,self.ui.node_color[SOURCE])
            self.robot_uno.dibujarRobot(self.ui.screen,(15, 108, 125))
            self.robot_dos.dibujarRobot(self.ui.screen,(15, 108, 125))
            self.control.dibujarPedidos(self.ui.screen)
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
            self.pedido = Pedido()
            self.control.agregarPedido(self.pedido)

            
        elif event.key == K_r: 
            print self.robot.state
            print self.robot_uno.state
            print self.robot_dos.state
            print self.control.pedidos

        elif event.key == K_s: 
            self.robot.state = 'libre'
            self.robot.notificacion_libre(self.control)

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
