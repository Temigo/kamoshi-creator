#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Ellipse, Line, Mesh, Point, Rectangle
from kivy.uix.widget import Widget

__author__ = 'Temigo'


class LayerLayout(RelativeLayout):
    def __init__(self, points=None, edges=None, **kwargs):
        super(LayerLayout, self).__init__(**kwargs)

        if points is None:
            points = []
        if edges is None:
            edges = []
        self.points = points
        self.edges = edges  # Existing folds

        for point in self.points:
            self.add_widget(point)
        for edge in self.edges:
            self.add_widget(edge)

    def draw(self):
        print "LayerLayout draw", self.points
        self.size = self.parent.size
        self.pos = self.parent.pos
        with self.parent.canvas:
            Color(0, 1, 0, 0.5)
            Rectangle(pos=self.pos, size=self.size)
            for point in self.points:
                point.draw()
            for edge in self.edges:
                edge.draw()

    def on_touch_down(self, touch):
        super(LayerLayout, self).on_touch_down(touch)
        print "Touch ! LayerLayout"


class Layer(Widget):
    def __init__(self, points=None, edges=None, **kwargs):
        """
        Defines a paper layer
        :param points: :class: ` list`  of :class: GraphicPoint
        :param kwargs:
        :return:
        """
        super(Layer, self).__init__(**kwargs)
        self.pos_hint = {'x': 0, 'y': 0}
        self.size_hint = (1, 1)

        self.recto = True  # Flag recto/verso
        self.layout = LayerLayout(points, edges, size=self.size, pos=(0,0))

        self.add_widget(self.layout)

    def draw(self):
        """
        Draw the layer in its canvas
        :return:
        """
        with self.canvas:
            self.canvas.clear()  # FIXME efface les layers antérieures ? Non car n'efface que cette layer ?
            if self.recto:  # color according to recto/verso
                Color(1, 0, 0, 0.5)
            else:
                Color(1, 1, 1, 0.5)  # White
            Rectangle(pos=self.pos, size=self.size)  # Paper
        self.layout.draw()

    def on_touch_down(self, touch):
        super(Layer, self).on_touch_down(touch)
        print "Touch ! Layer"

    def remove_point(self, point):
        self.layout.remove_widget(point)
        self.layout.points.remove(point)

    def add_point(self, point):
        self.layout.add_widget(point)
        self.layout.points.append(point)