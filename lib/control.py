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


letras = [
        #F
        (3,15),(3,16),(3,17),(3,18),(3,19),(3,20),(3,21),(3,22),(3,23),(3,24),(3,25),
        (4,15),(5,15),(6,15),(7,15),
        (4,20),(5,20),
        #E
        (10,15),(10,16),(10,17),(10,18),(10,19),(10,20),(10,21),(10,22),(10,23),(10,24),(10,25),
        (11,15),(12,15),(13,15),(14,15),
        (11,20),(12,20),
        (11,25),(12,25),(13,25),(14,25),
        #L
        (17,15),(17,16),(17,17),(17,18),(17,19),(17,20),(17,21),(17,22),(17,23),(17,24),(17,25),
        (18,25),(19,25),(20,25),(21,25),
        #I
        (24,15),(24,16),(24,17),(24,18),(24,19),(24,20),(24,21),(24,22),(24,23),(24,24),(24,25),
        #C
        (27,15),(27,16),(27,17),(27,18),(27,19),(27,20),(27,21),(27,22),(27,23),(27,24),(27,25),
        (28,15),(29,15),(30,15),(31,15),
        (28,25),(29,25),(30,25),(31,25),
        #I
        (34,15),(34,16),(34,17),(34,18),(34,19),(34,20),(34,21),(34,22),(34,23),(34,24),(34,25),
        #D
        (37,15),(37,16),(37,17),(37,18),(37,19),(37,20),(37,21),(37,22),(37,23),(37,24),(37,25),
        (41,16),(41,17),(41,18),(41,19),(41,20),(41,21),(41,22),(41,23),(41,24),
        (38,15),(39,15),(40,15),
        (38,25),(39,25),(40,25),
        #A
        (44,15),(44,16),(44,17),(44,18),(44,19),(44,20),(44,21),(44,22),(44,23),(44,24),(44,25),
        (48,15),(48,16),(48,17),(48,18),(48,19),(48,20),(48,21),(48,22),(48,23),(48,24),(48,25),
        (45,15),(46,15),(47,15),
        (45,20),(46,20),(47,20),
        #D
        (51,15),(51,16),(51,17),(51,18),(51,19),(51,20),(51,21),(51,22),(51,23),(51,24),(51,25),
        (55,16),(55,17),(55,18),(55,19),(55,20),(55,21),(55,22),(55,23),(55,24),
        (52,15),(53,15),(54,15),
        (52,25),(53,25),(54,25),
        #E
        (58,15),(58,16),(58,17),(58,18),(58,19),(58,20),(58,21),(58,22),(58,23),(58,24),(58,25),
        (59,15),(60,15),(61,15),(62,15),
        (59,20),(60,20),
        (59,25),(60,25),(61,25),(62,25),
        #S
        (65,15),(65,16),(65,17),(65,18),(65,19),(65,20),
        (69,20),(69,21),(69,22),(69,23),(69,24),(69,25),
        (65,15),(66,15),(67,15),(68,15),(69,15),
        (65,20),(66,20),(67,20),(68,20),(69,20),
        (65,25),(66,25),(67,25),(68,25),(69,25),
]

letras_formadas = []



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
        print 'Initializing Control'
        self.letras = 221
        self.photo = False
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
                self.num_minProductos = len(pedido.productos_nom)/4
                r.canastas[0].productosRecoger = pedido.productos_nom[: self.num_minProductos]
                r.canastas[1].productosRecoger = pedido.productos_nom[self.num_minProductos: self.num_minProductos*2 ]
                r.canastas[2].productosRecoger = pedido.productos_nom[self.num_minProductos*2: self.num_minProductos*3 ]
                r.canastas[3].productosRecoger = pedido.productos_nom[self.num_minProductos*3 :]                                
                r.agregarRuta(self.pathRobot,pedido)
                r.state = 'ocupado'
                r.iniciarRecorrido()
                return
            else:
                self.totalrobotlibres = self.totalrobotlibres - 1
        if self.totalrobotlibres == 0:
            self.pedidos.append(pedido)
            print 'Order added to the queue'

    def agregarPuntoLetra(self): #Agragamos un pedido a un robot
        for r in self.robots:
            if r.state == 'libre':
                # self.path.insert(0, (r.source))
                # self.path.append(self.salida)
                # self.path.append((r.source))
                #print self.path
                self.pathRobot = []
                try:
                    nodes_map_raw = self._get_str_map(r.source, letras[0]) # 
                    a = AStar(nodes_map_raw)
                    for i in a.step():
                        pass   
                    self.pathRobot += a.path
                except:
                        pass                                 
                r.agregarRuta(self.pathRobot)
                try:
                    r.letra = letras[0]
                except:
                    r.letra = None
                r.state = 'ocupado'
                r.iniciarRecorrido()
            try:
                letras.pop(0)
            except:
                pass
        
        


    def agregarRobot(self,robot):
        self.robots.append(robot)
        # print 'Robot agregado'

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
                # print r.state
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
            print 'No pending orders'


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
                        if DistanciaEntrePuntos(robot0.posicion_actual, robot1.posicion_actual) > 5:
                            robot0.esperando_robot = False
                            robot0.tipo_choque = None
                            robot0.robot_choque = None
                            robot1.esperando_robot = False
                            robot1.tipo_choque = None
                            robot1.robot_choque = None
                elif robot0.tipo_choque == 20 and robot1.tipo_choque == 20:
                    if robot1.robot_choque == robot0.nombre:
                        if DistanciaEntrePuntos(robot1.posicion_actual, robot0.posicion_actual) > 5:
                            robot0.esperando_robot = False
                            robot0.tipo_choque = None
                            robot0.robot_choque = None
                            robot1.esperando_robot = False
                            robot1.tipo_choque = None
                            robot1.robot_choque = None
                elif robot0.tipo_choque == 21 and robot1.tipo_choque == 21:
                        if DistanciaEntrePuntos(robot0.posicion_actual, robot1.posicion_actual) > 5:
                            robot0.esperando_robot = False
                            robot0.tipo_choque = None
                            robot0.robot_choque = None
                            robot1.esperando_robot = False
                            robot1.tipo_choque = None
                            robot1.robot_choque = None


    def moverRobots(self,screen):
        for robot in self.robots:
            if robot.play:
                robot.Mover()
            if robot.posicion_actual == robot.letra:
                # al finalizar el recorrido imprime los puntos de la trayectoria
                #print robot.path
                # self.quitarPedidoConcluido(robot.pedido_actual)                    
                robot.notificacion_libre(self)

    def show_photo(self,screen):  
        if self.photo:
            b = pygame.sprite.Sprite() # create sprite
            b.image = pygame.image.load("ui/gina.jpg")
            b.rect = b.image.get_rect() # use image extent values 
            b.rect.topleft = [1080, 180] # put the ball in the top left corner
            screen.blit(b.image, b.rect)

    def cogerProductos(self):
        for robot in self.robots:
            if len(robot.coordenadas_producto):
                if robot.posicion_actual == robot.coordenadas_producto[0]:
                    clear = lambda: os.system('cls')
                    clear()
                    for canasta in robot.canastas:
                        print 'Basket ' + canasta.nombreCanasta
                        print '----------'
                        print ''
                        print 'List 1 (to collect products)' 
                        print '-----------------------------'
                        print canasta.productosRecoger
                        print ''
                        print 'List 2 (products in the basket)' 
                        print '-------------------------------'
                        print canasta.productosCanasta
                        print ''
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
                    Timer(1,robot.estadoEsperandoProducto).start()   #Hace que el robot se detenga 4 segundos para recoger roductos
            else:
                robot.estadoGiro = None



