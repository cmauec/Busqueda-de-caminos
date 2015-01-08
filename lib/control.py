from const.constants import * 
import pygame
from pygame.locals import *
from lib.pedido import *
import random 
from algo.astar import *



class Control(object):

    def __init__(self, nodes):
        print 'Inicializando Control'
        self.pedidos = []
        self.pedidosDibujar = []
        self.robots = []
        self.salida_norte = [(89,6),(89,8),(89,10)]
        self.salida_noreste = [(89,15),(89,17),(89,19)]
        self.salida_sur = [(89,35),(89,37),(89,39)]
        self.salida_suroeste = [(89,25),(89,27),(89,29)]
        self.sections = [(1,8),(9,14),(15,20),(21,26),(27,32),(33,38),(39,44),(45,50),(51,56),(57,62),(63,68),(69,74),(75,80),(81,82)]
        #nos sirve para crear la sombra de los targets
        self.move_right_wall = (1,9,15,21,27,33,39,45,51,57,63,69,75,81) #aumentamos en x uno
        self.move_left_wall = (7,13,19,25,31,37,43,49,55,61,67,73,79) #disminuimos en x uno
        self.move_down_wall = 4 #aumentamos en y uno
        self.move_up_wall = 41 #disminuimos en Y uno
        self.wall_is_vertical = range(8,38)
        self.nodes = nodes

    def agregarPedido(self,pedido):
        self.pedidosDibujar.append(pedido)
        self.totalrobotlibres = len(self.robots)
        for r in self.robots:
            if r.state == 'libre':
                #si el robot esta en la parte de arriba tendra como salida al norte o al noreste
                if r.source[1]<8:
                    self.salida = self.salida_norte+self.salida_noreste
                    self.salida = random.choice(self.salida)
                #si el robot esta en la parte inferior tendra como salida al sur o suroeste
                elif r.source[1]>37:
                    self.salida = self.salida_sur+self.salida_suroeste
                    self.salida = random.choice(self.salida)
                self.path = pedido.productos
                self.path.insert(0, r.source)
                self.path = self.gen_path(self.path)
                self.path = self.gen_path_order(self.path)
                self.path.append(self.salida)
                self.path.append(r.source)
                self.pathRobot = []
                for t in range(len(self.path)):
                    if t+1 < len(self.path):
                        nodes_map_raw = self._get_str_map(self.path[t], self.path[t+1])
                        try:
                            a = AStar(nodes_map_raw)
                            for i in a.step():
                                pass
                            self.pathRobot += a.path
                        except:
                            pass 
                r.agregarRuta(self.pathRobot)
                r.state = 'ocupado'
                return
            else:
                self.totalrobotlibres = self.totalrobotlibres - 1
        if self.totalrobotlibres == 0:
            self.pedidos.append(pedido)
            print 'Pedido agregado a la cola'
        

    def agregarRobot(self,robot):
        self.robots.append(robot)
        print 'Robot agregado'

    def dibujarPedidos(self, screen):
        for p in self.pedidosDibujar:
            color = p.color
            for producto in p.productos:
                x, y = producto
                nx, ny = x * NODE_SIZE, y * NODE_SIZE
                pygame.draw.rect(screen, color, 
                    Rect(nx, ny, NODE_SIZE, NODE_SIZE))
        
    

    def cambiarEstadoRobot(self,robot):
        print 'cambiar'

    def asignarPedidoRobot(self,nombre):
        if len(self.pedidos)>0:
            for r in self.robots:
                if r.nombre == nombre and r.state == 'libre':
                    if r.source[1]<8:
                        self.salida = self.salida_norte+self.salida_noreste
                        self.salida = random.choice(self.salida)
                    #si el robot esta en la parte inferior tendra como salida al sur o suroeste
                    elif r.source[1]>37:
                        self.salida = self.salida_sur+self.salida_suroeste
                        self.salida = random.choice(self.salida)
                    self.path = self.pedidos[0].productos
                    self.path.insert(0, r.source)
                    self.path = self.gen_path(self.path)
                    self.path = self.gen_path_order(self.path)
                    self.path.append(self.salida)
                    self.path.append(r.source)
                    self.pathRobot = []
                    for t in range(len(self.path)):
                        if t+1 < len(self.path):
                            nodes_map_raw = self._get_str_map(self.path[t], self.path[t+1])
                            try:
                                a = AStar(nodes_map_raw)
                                for i in a.step():
                                    pass
                                self.pathRobot += a.path
                            except:
                                pass 
                    r.agregarRuta(self.pathRobot)
                    r.state = 'ocupado'
                    self.pedidos.pop(0)
                    return
        else:
            print 'No hay pedidos en espera'


    def quitarPedidoConcluido(self, pedido):
        indexPedido = self.pedidosDibujar.index(pedido)
        self.pedidosDibujar.pop(indexPedido)



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

    def _get_str_map(self,sourceA,targetA):
        """Generate a string represented map from the current nodes' status.
        """
        final_str = []
        for row in self.nodes:
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


