import pygame
import random 
import collections
from pygame.locals import *
from lib.pedido import *
from const.constants import * 
from algo.astar import *
from math import sqrt
import os
from threading import Timer

FONT_NAME = 'freesansbold.ttf'
cur_path = os.path.abspath(os.path.dirname(__file__))
ui_path = os.path.join(cur_path, '../ui')
pygame.font.init()

texto_choque = 'Choque robots'
texto_se_van_chocar = 'Se van a chocar'
font = pygame.font.Font(os.path.join(ui_path, FONT_NAME),40)
txt_choque = font.render(texto_choque,True,(0,0,0))
txt_se_van_chocar = font.render(texto_se_van_chocar,True,(0,0,0))

pared_izq = (2,10,16,22,28,34,40,46,52,58,64,70,76,82) #Posiciones donde existe pared a la izq
pared_der = (6,12,18,24,30,36,42,48,54,60,66,74,78)   #Posiciones donde existe pared a la der
pared_arriba = 5   #Posiciones donde existe pared arrib
pared_abajo = 40    #Posiciones donde existe pared abaj


def DistanciaEntrePuntos(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    h = sqrt((x**2) + (y**2))
    return h



def posibleChoque(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    return (x, y)




class Control(object):

    def __init__(self, nodes):
        print 'Inicializando Control'
        self.pedidos = []
        self.pedidosDibujar = []
        self.robots = []
        self.salida_norte = [(88,6),(88,8),(88,10)]
        self.salida_noreste = [(88,15),(88,17),(88,19)]
        self.salida_sur = [(88,35),(88,37),(88,39)]
        self.salida_suroeste = [(88,25),(88, 27),(88,29)]
        
        self.sections = [(1,8),(9,14),(15,20),(21,26),(27,32),(33,38),(39,44),(45,50),(51,56),(57,62),(63,68),(69,74),(75,80),(81,82)]
        #nos sirve para crear la sombra de los targets
        self.move_right_wall = (1,9,15,21,27,33,39,45,51,57,63,69,75,81) #aumentamos en x uno
        self.move_left_wall = (7,13,19,25,31,37,43,49,55,61,67,73,79) #disminuimos en x uno
        self.move_down_wall = 4 #aumentamos en y uno
        self.move_up_wall = 41 #disminuimos en Y uno
        self.wall_is_vertical = range(8,38)
        self.nodes = nodes

    def agregarPedido(self,pedido): #Agragamos un pedido a un robot
        self.pedidosDibujar.append(pedido)
        self.totalrobotlibres = len(self.robots)
        for r in self.robots:
            if r.state == 'libre':
                # si el robot esta en la parte de arriba tendra como salida al norte o al noreste
                if r.source[1]<8:
                    self.salida = self.salida_norte + self.salida_noreste
                    self.salida = random.choice(self.salida)
                    self.salida_dibujo = (self.salida[0]+1, self.salida[1])
                # si el robot esta en la parte inferior tendra como salida al sur o suroeste
                elif r.source[1]>37:
                    self.salida = self.salida_sur + self.salida_suroeste
                    self.salida = random.choice(self.salida)
                    self.salida_dibujo = (self.salida[0]+1, self.salida[1])
                self.path = pedido.productos
                self.path.insert(0, (r.source))
                self.path = self.gen_path(self.path)
                self.path = self.gen_path_order(self.path)
                r.coordenadas_producto = self.path[1:]
                self.path.append(self.salida)
                self.path.append((r.source))
                #print self.path
                self.pathRobot = []
                self.loop = 0  # Nos va a decir en q ciclo esta el for
                for t in range(len(self.path)-1):
                    try:
                        nodes_map_raw = self._get_str_map(self.path[t], self.path[t+1]) # 
                        a = AStar(nodes_map_raw)
                        for i in a.step():
                            pass   
                        if self.loop > 0:                     
                            self.pathRobot += a.path[1:]
                        else:
                            self.pathRobot += a.path
                    except:
                            pass
                    self.loop += 1  
                #Llenamos las 3 canastas de un robot con el pedido grande
                self.num_minProductos = len(pedido.productos_nom)/3
                r.canastas[0].productosRecoger = pedido.productos_nom[: self.num_minProductos]
                r.canastas[1].productosRecoger = pedido.productos_nom[self.num_minProductos: self.num_minProductos*2 ]
                r.canastas[2].productosRecoger = pedido.productos_nom[self.num_minProductos*2 :]                                
                r.agregarRuta(self.pathRobot,pedido)
                r.state = 'ocupado'
                r.iniciarRecorrido()
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
            p.productos.append(self.salida_dibujo)
            for producto in p.productos:
                x, y = producto
                nx, ny = x * NODE_SIZE, y * NODE_SIZE
                pygame.draw.rect(screen, color, 
                    Rect(nx, ny, NODE_SIZE, NODE_SIZE))
        

    def asignarPedidoRobot(self,nombre): #Asignamos pedidos que esten en espera a un robot que este libre
        if len(self.pedidos)>0:
            for r in self.robots:
                print r.state
                if r.nombre == nombre and r.state == 'libre':
                    if r.source[1]<8:
                        self.salida = self.salida_norte+self.salida_noreste
                        self.salida = random.choice(self.salida)
                        self.salida_dibujo = (self.salida[0]+1, self.salida[1])
                    #si el robot esta en la parte inferior tendra como salida al sur o suroeste
                    elif r.source[1]>37:
                        self.salida = self.salida_sur+self.salida_suroeste
                        self.salida = random.choice(self.salida)
                        self.salida_dibujo = (self.salida[0]+1, self.salida[1])
                    self.path = self.pedidos[0].productos
                    self.path.insert(0, r.source)
                    self.path = self.gen_path(self.path)
                    self.path = self.gen_path_order(self.path)
                    r.coordenadas_producto = self.path[1:]
                    self.path.append(self.salida)
                    self.path.append(r.source)
                    self.pathRobot = []
                    self.loop = 0  # Nos va a decir en q ciclo esta el for
                    for t in range(len(self.path)-1):
                        try:
                            nodes_map_raw = self._get_str_map(self.path[t], self.path[t+1]) # Hace que se el robot se quede en el producto 2tiempos
                            a = AStar(nodes_map_raw)
                            for i in a.step():
                                pass   
                            if self.loop > 0:                     
                                self.pathRobot += a.path[1:]
                            else:
                                self.pathRobot += a.path
                        except:
                                pass
                        self.loop += 1 
                    r.agregarRuta(self.pathRobot,self.pedidos[0])
                    r.state = 'ocupado'
                    r.iniciarRecorrido()
                    self.pedidos.pop(0)
                    return
        else:
            print 'No hay pedidos en espera'


    def quitarPedidoConcluido(self, pedido):
        indexPedido = self.pedidosDibujar.index(pedido)
        self.pedidosDibujar.pop(indexPedido)


    def quitarRobot(self, robot):
        indexRobot = self.robots.index(robot)
        self.robots.pop(indexRobot)



    def gen_path(self, targets):
        # cambiamos la posicion de los puntos de los productos para que esten fuera de la estanteria, para crear el camino del robot, ya que un robot no puede estar sobre la estanteria   
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
        path = list(collections.OrderedDict.fromkeys(path))
        return path


    # Para ordenar los targets de menor a mayor (por seccion)    
    def gen_path_order(self, targets):
        path = []
        for s in self.sections:
            path_section = []
            for t in targets:
                if t[0] in range(s[0], s[1]+1):
                    try:
                        path_section.append(t)
                    except:  
                        pass
            if len(path)>0:
                path_section.insert(0,path[-1]) #hace que el ultimo punto de la seccion sea el primer punto de la siguiente seccion
            path_section = self.path_order_distance(path_section)
            path = path +path_section
        path = list(collections.OrderedDict.fromkeys(path))
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
        path = list(collections.OrderedDict.fromkeys(targets_order))
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

    def resetChoqueRobot(self):
        self.robots_movimiento1 = []
        self.robots_temporal1 = []
        for robot in self.robots:
            if robot.play:
                self.robots_movimiento1.append(robot)
        self.robots_temporal1 = self.robots_movimiento1[1:]            
        for robot0 in self.robots_movimiento1:
            for robot1 in self.robots_temporal1:
                if robot0.tipo_choque == 1 and robot1.tipo_choque == 1:
                    if robot0.robot_choque == robot1.nombre:
                        if robot0.esperando_robot == False:
                            robot0.esperando_robot = True
                        if DistanciaEntrePuntos(robot0.posicion_actual, robot1.posicion_actual) > 3:
                            robot0.esperando_robot = False
                            robot0.tipo_choque = None
                            robot0.robot_choque = None
                            robot1.esperando_robot = False
                            robot1.tipo_choque = None
                            robot1.robot_choque = None
                elif robot0.tipo_choque == 20 and robot1.tipo_choque == 20:
                    print 'entra 20'
                    if robot1.robot_choque == robot0.nombre:
                        print '20 20'
                        if robot1.esperando_robot == False:
                            print '20 20 20'
                            robot1.esperando_robot = True
                        if DistanciaEntrePuntos(robot1.posicion_actual, robot0.posicion_actual) > 3:
                            print '20 20 20 20'
                            robot0.esperando_robot = False
                            robot0.tipo_choque = None
                            robot0.robot_choque = None
                            robot1.esperando_robot = False
                            robot1.tipo_choque = None
                            robot1.robot_choque = None
                elif robot0.tipo_choque == 21 and robot1.tipo_choque == 21:
                    print 'entra 21'
                    if robot0.robot_choque == robot1.nombre:
                        print  '21 21'
                        if robot0.esperando_robot == False:
                            print '21 21 21'
                            robot0.esperando_robot = True
                        if DistanciaEntrePuntos(robot0.posicion_actual, robot1.posicion_actual) > 3:
                            print '21 21 21 21'
                            robot0.esperando_robot = False
                            robot0.tipo_choque = None
                            robot0.robot_choque = None
                            robot1.esperando_robot = False
                            robot1.tipo_choque = None
                            robot1.robot_choque = None

    def moverRobots(self,screen):
        #Calculamos choques en los robots
        self.robots_movimiento = []
        self.robots_temporal = []
        self.probabilidad_desvio = []
        for robot in self.robots:
            if robot.play:
                self.robots_movimiento.append(robot)
        self.robots_temporal = self.robots_movimiento[1:]
        for robot0 in self.robots_movimiento:
            for robot1 in self.robots_temporal:
                if robot0.tipo_choque == None and robot1.tipo_choque == None:
                    if robot0.rec_colision.colliderect(robot1.rec_colision):  
                        if robot0.path_restante[1]==robot1.path_restante[1]:
                            screen.blit(txt_se_van_chocar,(170,30)) # Escribe texto en pantalla

                            # Asignamos el tipo de choque de los robots involucrados y el nombre con el que estan en choque cada uno  
                            robot0.tipo_choque = 1
                            robot0.robot_choque = robot1.nombre 
                            robot1.tipo_choque = 1
                            robot1.robot_choque = robot0.nombre

                            # Calculamos la mejor direccion para que se desvie el robot
                            # Creamos un vector con todas las posibilidades de desvio alrededor del robot
                            self.probabilidad_desvio = [(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0], robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1),(robot0.posicion_actual[0], robot0.posicion_actual[1]-1),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1)]
                            # Quitamos las opciones no validas
                            self.probabilidad_desvio.remove(robot1.path_restante[1])
                            if robot0.posicion_actual[0] in pared_izq:
                                #Antes de borrar el elemto revizamos si esta en el vector. Cuando el choque se produce en la parte sup. o infe. que no hay pared a la izq o der y el punto de choque esta en la posicion de la pared.El codigo primero quitaba el punto de  choque pero este punto tambien pertenece a los puntos que hay q quitar por la pared, entonces se queria quitar un punto que ya no existia
                                if (robot0.posicion_actual[0]-1, robot0.posicion_actual[1]) in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]))
                                if (robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1) in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                                if (robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1) in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                            elif robot0.posicion_actual[0] in pared_der:
                                if (robot0.posicion_actual[0]+1, robot0.posicion_actual[1]) in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]))
                                if (robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1) in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1))
                                if (robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1) in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                            elif robot0.posicion_actual[1] == pared_arriba:
                                if (robot0.posicion_actual[0], robot0.posicion_actual[1]-1) in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]-1))
                                if (robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1) in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                                if (robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1) in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                            elif robot0.posicion_actual[1] == pared_abajo:
                                if (robot0.posicion_actual[0], robot0.posicion_actual[1]+1) in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]+1))
                                if (robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1) in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                                if (robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1) in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1))
                            if robot1.path_restante[2] in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove(robot1.path_restante[2])
                            elif robot1.path_restante[3] in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove(robot1.path_restante[3])                          
                            self.coordenada_desvio = random.choice(self.probabilidad_desvio)                 
                            robot0.path_restante.insert(1, self.coordenada_desvio)
                            robot0.path_restante.insert(2, robot0.path_restante[0])
                        elif (robot0.path_restante[1]==robot1.path_restante[0])and(robot0.path_restante[0]==robot1.path_restante[1]):
                            screen.blit(txt_choque,(170,30))
                            robot0.tipo_choque = 2
                            robot0.robot_choque = robot1.nombre 
                            robot1.tipo_choque = 2
                            robot1.robot_choque = robot0.nombre
                            self.probabilidad_desvio = [(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0], robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1),(robot0.posicion_actual[0], robot0.posicion_actual[1]-1),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1)]
                            
                            if robot0.posicion_actual[0] in pared_izq:
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                            elif robot0.posicion_actual[0] in pared_der:
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1)) 
                            elif robot0.posicion_actual[1] == pared_arriba:
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                            elif robot0.posicion_actual[1] == pared_abajo:
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]+1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1))
                            self.probabilidad_desvio.remove(robot1.path_restante[0])
                            if robot1.path_restante[1] in self.probabilidad_desvio:
                                self.probabilidad_desvio.remove(robot1.path_restante[1])
                            elif robot1.path_restante[2] in self.probabilidad_desvio:
                                self.probabilidad_desvio.remove(robot1.path_restante[2])                                                     
                            self.coordenada_desvio = random.choice(self.probabilidad_desvio)                                
                            robot0.path_restante.insert(1, self.coordenada_desvio)
                            robot0.path_restante.insert(2, robot0.path_restante[0])



                # elif robot0.esperando_producto and robot1.play and not robot1.esperando_robot:
                #     if (DistanciaEntrePuntos(robot0.posicion_actual, robot1.posicion_actual) == 1 ) or (DistanciaEntrePuntos(robot0.posicion_actual, robot1.posicion_actual) == sqrt(2)):
                #         #robot0.play = False
                #         #robot1.play = False
                #         print 'colision, rob0-esperando, rob1-mov'                                                        
                #         robot0.robot_choque = robot1.nombre
                #         robot1.robot_choque = robot0.nombre
                #         robot0.tipo_choque = 20
                #         robot1.tipo_choque = 20
                        
                #         print robot0.posicion_actual
                #         print robot1.posicion_actual
                #         print robot1.path_restante[1]
                #         print robot0.path_restante[1]
                #         #if robot1.path_restante[1][0] == robot0.posicion_actual[0]:                      
                #         print 'Gina'
                #         self.probabilidad_desvio = [(robot1.posicion_actual[0]+1, robot1.posicion_actual[1]),(robot1.posicion_actual[0]+1, robot1.posicion_actual[1]+1),(robot1.posicion_actual[0], robot1.posicion_actual[1]+1),(robot1.posicion_actual[0]-1, robot1.posicion_actual[1]+1),(robot1.posicion_actual[0]-1, robot1.posicion_actual[1]),(robot1.posicion_actual[0]-1, robot1.posicion_actual[1]-1),(robot1.posicion_actual[0], robot1.posicion_actual[1]-1),(robot1.posicion_actual[0]+1, robot1.posicion_actual[1]-1)]
                        
                #         if robot1.posicion_actual[0] in pared_izq:
                #             self.probabilidad_desvio.remove((robot1.posicion_actual[0]-1, robot1.posicion_actual[1]))
                #             self.probabilidad_desvio.remove((robot1.posicion_actual[0]-1, robot1.posicion_actual[1]-1))
                #             self.probabilidad_desvio.remove((robot1.posicion_actual[0]-1, robot1.posicion_actual[1]+1))
                #         elif robot1.posicion_actual[0] in pared_der:
                #             self.probabilidad_desvio.remove((robot1.posicion_actual[0]+1, robot1.posicion_actual[1]))
                #             self.probabilidad_desvio.remove((robot1.posicion_actual[0]+1, robot1.posicion_actual[1]-1))
                #             self.probabilidad_desvio.remove((robot1.posicion_actual[0]+1, robot1.posicion_actual[1]+1)) 
                #         elif robot1.posicion_actual[1] == pared_arriba:
                #             self.probabilidad_desvio.remove((robot1.posicion_actual[0], robot1.posicion_actual[1]-1))
                #             self.probabilidad_desvio.remove((robot1.posicion_actual[0]-1, robot1.posicion_actual[1]-1))
                #             self.probabilidad_desvio.remove((robot1.posicion_actual[0]+1, robot1.posicion_actual[1]-1))
                #         elif robot1.posicion_actual[1] == pared_abajo:
                #             self.probabilidad_desvio.remove((robot1.posicion_actual[0], robot1.posicion_actual[1]+1))
                #             self.probabilidad_desvio.remove((robot1.posicion_actual[0]-1, robot1.posicion_actual[1]+1))
                #             self.probabilidad_desvio.remove((robot1.posicion_actual[0]+1, robot1.posicion_actual[1]+1))
                #         self.probabilidad_desvio.remove(robot0.posicion_actual)
                #         if robot0.path_restante[1] in self.probabilidad_desvio:
                #             self.probabilidad_desvio.remove(robot0.path_restante[1])
                #         elif robot0.path_restante[2] in self.probabilidad_desvio:
                #             self.probabilidad_desvio.remove(robot0.path_restante[2])                                                     
                #         self.coordenada_desvio = random.choice(self.probabilidad_desvio)
                #         #self.coordenada_desvio = (robot1.posicion_actual[0]+1, robot1.posicion_actual[1])                             
                #         robot1.path_restante.insert(1, self.coordenada_desvio)
                #         robot1.path_restante.insert(2, robot1.path_restante[0])




                          
                # elif robot1.esperando_producto and robot0.play and not robot0.esperando_robot:
                #     if (DistanciaEntrePuntos(robot1.posicion_actual, robot0.posicion_actual) == 1) or (DistanciaEntrePuntos(robot1.posicion_actual, robot0.posicion_actual) == sqrt(2)):
                #         #robot0.play = False
                #         #robot1.play = False
                #         print 'colision, rob1-esperando, rob0-mov'                            
                #         robot0.robot_choque = robot1.nombre
                #         robot1.robot_choque = robot0.nombre
                #         robot0.tipo_choque = 21
                #         robot1.tipo_choque = 21
                       
                #         print robot1.posicion_actual
                #         print robot0.posicion_actual
                #         print robot0.path_restante[1]
                #         print robot1.path_restante[1]
                #         #if robot0.path_restante[1][0] == robot1.posicion_actual[0]:
                #         print 'Gina1'
                #         self.probabilidad_desvio = [(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0], robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1),(robot0.posicion_actual[0], robot0.posicion_actual[1]-1),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1)]                            
                #         if robot0.posicion_actual[0] in pared_izq:
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                #         elif robot0.posicion_actual[0] in pared_der:
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1)) 
                #         elif robot0.posicion_actual[1] == pared_arriba:
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]-1))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                #         elif robot0.posicion_actual[1] == pared_abajo:
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]+1))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1))
                #         self.probabilidad_desvio.remove(robot1.posicion_actual)
                #         if robot1.path_restante[1] in self.probabilidad_desvio:
                #             self.probabilidad_desvio.remove(robot1.path_restante[1])
                #         elif robot1.path_restante[2] in self.probabilidad_desvio:
                #             self.probabilidad_desvio.remove(robot1.path_restante[2])                                                     
                #         self.coordenada_desvio = random.choice(self.probabilidad_desvio)
                #         #self.coordenada_desvio = (robot0.posicion_actual[0]+1, robot0.posicion_actual[1])                              
                #         robot0.path_restante.insert(1, self.coordenada_desvio)
                #         robot0.path_restante.insert(2, robot0.path_restante[0])
                        

                # elif robot1.esperando_producto and robot0.esperando_producto: 
                #     robot0.play = False
                #     robot1.play = False                        
                #     if (robot0.path_restante[1]==robot1.path_restante[0])and(robot0.path_restante[0]==robot1.path_restante[1]):
                #         robot0.tipo_choque = 3
                #         robot0.robot_choque = robot1.nombre 
                #         robot1.tipo_choque = 3
                #         robot1.robot_choque = robot0.nombre
                #         self.probabilidad_desvio = [(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0], robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1),(robot0.posicion_actual[0], robot0.posicion_actual[1]-1),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1)]
                        
                #         if robot0.posicion_actual[0] in pared_izq:
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                #         elif robot0.posicion_actual[0] in pared_der:
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1)) 
                #         elif robot0.posicion_actual[1] == pared_arriba:
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]-1))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                #         elif robot0.posicion_actual[1] == pared_abajo:
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]+1))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                #             self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1))
                #         self.probabilidad_desvio.remove(robot1.path_restante[0])
                #         if robot1.path_restante[1] in self.probabilidad_desvio:
                #             self.probabilidad_desvio.remove(robot1.path_restante[1])
                #         elif robot1.path_restante[2] in self.probabilidad_desvio:
                #             self.probabilidad_desvio.remove(robot1.path_restante[2])                                                     
                #         self.coordenada_desvio = random.choice(self.probabilidad_desvio)                                
                #         robot0.path_restante.insert(1, self.coordenada_desvio)
                #         robot0.path_restante.insert(2, robot0.path_restante[0])
                #         print 'Gina3'

                            

            try: 
                self.robots_temporal.pop(0)
            except:
                pass

        for robot in self.robots:
            if robot.play:
                    robot.Mover()
            if robot.posicion_actual == (robot.source[0]+1,robot.source[1]):
                # al finalizar el recorrido imprime los puntos de la trayectoria
                #print robot.path
                self.quitarPedidoConcluido(robot.pedido_actual)                    
                robot.notificacion_libre(self)

    def cogerProductos(self):
        for robot in self.robots:
            if len(robot.coordenadas_producto):
                if robot.posicion_actual == robot.coordenadas_producto[0]:
                    robot.esperando_producto = True
                    robot.play = False
                    robot.coordenadas_producto.pop(0)
                    robot.flagGirar = True
                    for canasta in robot.canastas:
                        for producto in canasta.productosRecoger:                                                      
                            if producto[1][1] in self.wall_is_vertical:   #[1]-coordenadas del producto y [1]-y
                                if producto[1][0] in self.move_right_wall:
                                    pn1 = (producto[1][0]+1,producto[1][1])
                                    canastaOrientacion = 'der'
                                elif producto[1][0] in self.move_left_wall:
                                    pn1 = (producto[1][0]-1,producto[1][1]) 
                                    canastaOrientacion = 'izq'
                            else:
                                if producto[1][1] == self.move_down_wall:
                                    pn1 = (producto[1][0], producto[1][1]+1)
                                    canastaOrientacion = 'arriba'
                                elif producto[1][1] == self.move_up_wall:
                                    pn1 = (producto[1][0],producto[1][1]-1) 
                                    canastaOrientacion = 'abajo'
                            try:                                                                          
                                if robot.coordenadas_producto[0] == pn1:                                
                                    canasta.productosCanasta.append(producto)
                                    canasta.productosRecoger.remove(producto)
                                    robot.estadoGiro = [canasta.nombreCanasta,canastaOrientacion]
                            except:
                                pass
                                robot.estadoGiro = None
                    Timer(4,robot.estadoEsperandoProducto).start()   #Hace que el robot se detenga 4 segundos para recoger roductos
            else:
                robot.estadoGiro = None



