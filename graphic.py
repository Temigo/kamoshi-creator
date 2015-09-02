#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Mesh, Point, Rectangle

from math import sqrt

__author__ = 'Temigo'


class GraphicEdge(Widget):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super(GraphicEdge, self).__init__(**kwargs)
        self.points = [x1, y1, x2, y2]
        self.pos_hint = {'x': x1, 'y': y1}
        self.x2 = x2
        self.y2 = y2

    def draw(self):
        print "Drawing edge"
        with self.parent.parent.canvas:
            Color(0, 0, 0)
            (x, y) = self.to_parent(self.x2 * self.parent.size[0], self.y2 * self.parent.size[1])
            Line(points=[self.x, self.y, x, y], width=5)
            print self.x, self.y, x, y

class GraphicPoint(Widget):
    d = 30.  # Diameter

    def __init__(self, x, y, **kwargs):
        super(GraphicPoint, self).__init__(**kwargs)
        self.pos_hint = {'x': x, 'y': y}
        self.size_hint = (None, None)
        self.size = (self.d, self.d)

    def __repr__(self):
        return "<GraphicPoint (%d, %d)>" % (self.x, self.y)

    def draw(self, selected=False):
        # FIXME Occurs 3 times ?
        print self.pos, self.size
        with self.parent.parent.canvas:
            if selected:
                Color(0, 1, 1)
            else:
                Color(1, 0, 0)
            Ellipse(pos=self.pos, size=(self.d, self.d))

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            print "Touch !"
            self.draw(selected=True)
            self.parent.parent.parent.current_point = self
        super(GraphicPoint, self).on_touch_down(touch)

    def mirror(self, x1, y1, x2, y2):
        """
        Mirror the point against bisector of 1(x1, y1) and 2(x2, y2)
        :return:
        """
        x = self.x
        y = self.y
        # Length of 1-2
        length = sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))
        # Scalar product of 1->M and 1->2
        a = ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / length
        # Shorter distance of M to bisector of 1-2
        distance = abs(length/2. - a)

        self.x = x + 2 * distance * (x2 - x1) / length
        self.y = y + 2 * distance * (y2 - y1) / length