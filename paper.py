#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------
#       KAMOSHI CREATOR         |
#                  v0.1         |
#--------------------------------

from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ListProperty

from graphic import GraphicPoint, GraphicEdge2
from layer import Layer

from math import sqrt

__author__ = 'Temigo'


class PaperLayout(RelativeLayout):
    d = 30.
    IS_SELECTING = False
    first_point = None  # When selecting a couple of points
    last_point = None

    init_points = [GraphicPoint(0, 0), GraphicPoint(1, 0), GraphicPoint(0, 1), GraphicPoint(1, 1)]
    layers = ListProperty([Layer(points=init_points,
                                 edges=[GraphicEdge2(init_points[0], init_points[1]),
                                        GraphicEdge2(init_points[1], init_points[3]),
                                        GraphicEdge2(init_points[0], init_points[2]),
                                        GraphicEdge2(init_points[2], init_points[3])])])
                           # [GraphicEdge(0, 0, 1, 0), GraphicEdge(1, 0, 1, 1), GraphicEdge(0, 0, 0, 1), GraphicEdge(0, 1, 1, 1)])]
    current_layer = 0
    current_point = None

    def __init__(self, **kwargs):
        super(PaperLayout, self).__init__(**kwargs)
        for layer in self.layers:
            self.add_widget(layer)

    def on_layers(self, instance, value):
        """
        Callback when self.layers is changed
        :param instance:
        :param value:
        :return:
        """
        print "on_layers", instance, value
        with self.canvas:
            #self.canvas.clear()
            #self.add_widget(value)
            self.do_layout()

    def do_layout(self, *args):
        # self.canvas.clear()
        super(PaperLayout, self).do_layout(*args)

        for layer in self.layers:
            layer.draw()

    def on_touch_down(self, touch):
        """ Trigger selection
        :param touch:
        :return:
        """
        super(PaperLayout, self).on_touch_down(touch)
        print "Touch ! PaperLayout", self.children

        if self.current_point is not None:
            if self.IS_SELECTING:  # End of selection
                if self.current_point == self.first_point:
                    # Deselect
                    self.current_point.draw()
                else:
                    self.last_point = self.current_point
                    self.new_step()
                self.IS_SELECTING = False
                self.current_point = None
            else:  # Begin selection
                self.first_point = self.current_point
                self.IS_SELECTING = True

    def on_touch_move(self, touch):
        #touch.ud['line'].points += [touch.x, touch.y]
        pass

    @staticmethod
    def is_under_bisector(x, y, x1, y1, x2, y2):
        """
        Determines if the point M(x,y) should be mirrored against bisector of (x1, y1) and (x2, y2)
        Scalar product of 1->2 and 1->M should be less than half of distance 1-2
        :return:
        """
        length = sqrt(pow((x2 - x1), 2) + pow(y2 - y1, 2))
        a = ((x2 - x1) * (x - x1) + (y2 - y1) * (y - y1)) / length
        b = 1. / 2. * length
        if a == b:  # On the bisector
            return True, True
        elif a < b:
            return True, False
        else:
            return False, None

    def new_step(self):
        print "New step !", self.layers
        layers_stack = self.layers[self.current_layer:]
        x1 = self.first_point.x
        y1 = self.first_point.y
        x2 = self.last_point.x
        y2 = self.last_point.y
        for i in range(len(layers_stack)):
            layer = layers_stack[i]
            points_to_translate = []
            keep_point = {}
            mirror_point = {}
            for point in layer.layout.points:
                print point, len(layer.layout.points)
                # Position par rapport à la médiatrice
                b1, b2 = self.is_under_bisector(point.x, point.y, x1, y1, x2, y2)
                if b1:
                    points_to_translate.append(point)
                    keep_point[point] = b2  # Is it on bisector ?
                    #layer.remove_point(point)
            print points_to_translate
            for point in points_to_translate:
                # FIXME : changes when point is mirrored ? x and y are NumericProperty
                mirror_point[point] = (point.x, point.y)  # Old coordinates
                point.mirror(x1, y1, x2, y2)
                layer.remove_point(point)

                if keep_point[point]:
                    new_point = GraphicPoint(0, 0)  # FIXME calculate relative coordinates
                    new_point.x = point.x
                    new_point.y = point.y
                    layer.add_point(new_point)
            print points_to_translate, keep_point, layer.layout.edges
            new_edges = []
            edges_to_remove = []
            for edge in layer.layout.edges:
                # b1, b2 = self.is_under_bisector(edge.start.x, edge.start.y, x1, y1, x2, y2)
                # b3, b4 = self.is_under_bisector(edge.end.x, edge.end.y, x1, y1, x2, y2)
                b1 = edge.start in points_to_translate
                b2 = keep_point[edge.start] if b1 else False
                b3 = edge.end in points_to_translate
                b4 = keep_point[edge.end] if b3 else False
                print "Edge", edge, edge.start, edge.end, b1 ,b2, b3, b4
                if b2 and b4:  # Edge is within bisector
                    new_edge = GraphicEdge2(edge.start, edge.end)  # FIXME : start and stop have been duplicated
                    new_edges.append(new_edge)
                elif b2 or b4:  # Start (x)or end of edge is on bisector
                    pass
                else:  # Nor start nor end of edge is on bisector
                    if b1 and b3:  # Edge is fully under bisector
                        pass
                    elif b1 or b3:  # Edge intersects bisector
                        # layer.remove_edge(edge)
                        edges_to_remove.append(edge)
                        # Calculate intersection edge/bisector
                        (start_x, start_y) = mirror_point[edge.start] if b1 else (edge.start.x, edge.start.y)
                        (end_x, end_y) = mirror_point[edge.end] if b3 else (edge.end.x, edge.end.y)
                        t = ((start_x - (x1+x2)/2) * (x1 - x2) + (start_y - (y1+y2)/2) * (y1- y2)) / \
                            ((end_x - start_x) * (x2 - x1) + (end_y - start_y) * (y2 - y1))
                        x = start_x + t * (end_x - start_x)
                        y = start_y + t * (end_y - start_y)
                        # Intersection point
                        point = GraphicPoint(0, 0)  # FIXME calculate relative coordinates
                        point.x = x
                        point.y = y
                        edge1 = GraphicEdge2(point, edge.end)
                        edge2 = GraphicEdge2(edge.start, point)
                        new_edges.append(edge1)
                        new_edges.append(edge2)
                        layer.add_point(point)  # FIXME add to new layer too ?
                        print "Intersection", edge, point
                    else:  # Edge shouldn't be modified
                        pass

            for edge in edges_to_remove:
                layer.remove_edge(edge)
            for edge in new_edges:
                layer.add_edge(edge)

            # TODO flip color
            new_layer = Layer(points=points_to_translate)
            new_layer.recto = not new_layer.recto
            # self.add_widget(new_layer)  # FIXME breaks the code ?
            self.layers.insert(i, new_layer)

        print self.layers