#!/usr/bin/python
# -*- coding: utf-8 -*-
# KAMOSHI CREATOR
# Main file

#import kivy
#kivy.require('1.8.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button

from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Mesh, Point, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ListProperty
from kivy.uix.slider import Slider

from math import sqrt
__author__ = 'Temigo'

#Builder.load_file('kamoshicreator.kv')


class GraphicEdge(Widget):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super(GraphicEdge, self).__init__(**kwargs)
        self.points = [x1, y1, x2, y2]

    def draw(self):
        with self.canvas:
            Color(0, 0, 0)
            Line(points=self.points, width=1.0)


class GraphicPoint(Widget):
    d = 30.  # Diameter

    def __init__(self, x, y, **kwargs):
        super(GraphicPoint, self).__init__(**kwargs)
        #self.x = x
        #self.y = y
        #self.pos = (x, y)
        self.pos = (x,y)
        #self.size_hint = (None, None)
        #self.size = (30, 30)

    def draw(self, selected=False):
        print "Drawing GraphicPoint", self  # FIXME Occurs 3 times ?
        with self.parent.canvas:
            print self.pos_hint, self.size, self.parent.pos, self.parent.size, self.x
            if selected:
                Color(0, 1, 1)
            else:
                Color(1, 0, 0)
            Ellipse(pos=self.pos, size=(self.d, self.d))

    def on_touch_down(self, touch):
        print "Touch !"
        self.draw(selected=True)


class Layer(Widget):
    def __init__(self, points=None, **kwargs):
        """
        Defines a paper layer
        :param points: :class: ` list`  of :class: GraphicPoint
        :param kwargs:
        :return:
        """
        super(Layer, self).__init__(**kwargs)

        self.pos_hint = {'x': 0, 'y': 0}
        self.size_hint = (1, 1)

        if points is None:
            points = []
        self.points = points
        self.edges = []  # Existing folds
        self.recto = True  # Flag recto/verso

        for point in self.points:
            self.add_widget(point, index=1)
        for edge in self.edges:
            self.add_widget(edge)

    def draw(self):
        """
        Draw the layer in its canvas
        :return:
        """
        with self.canvas:
            self.canvas.clear()  # FIXME efface les layers antérieures ?
            if self.recto:  # color according to recto/verso
                Color(1, 0, 0, 0.5)
            else:
                Color(1, 1, 1, 0.5)  # White
            #Rectangle(pos=self.pos, size=self.size)  # Paper

            for point in self.points:
                point.draw()

            for edge in self.edges:
                edge.draw()


class Toolbar(Widget):
    def __init__(self, **kwargs):
        super(Toolbar, self).__init__(**kwargs)
        print "toolbar"

    def new(self):
        print "New"

    def save(self):
        print "Save"

    def open(self):
        print "Open"

    def valley_moutain(self):
        print "Valley/Mountain"

    def scale(self):
        print "Scale"


class PaperLayout(RelativeLayout):
    d = 30.
    IS_SELECTING = False
    first_point = None # When selecting a couple of points
    last_point = None
    layers = [Layer(points=[GraphicPoint(0, 0), GraphicPoint(150, 100)])]
    current_layer = 0

    def __init__(self, **kwargs):
        super(PaperLayout, self).__init__(**kwargs)
        for layer in self.layers:
            self.add_widget(layer)

    def do_layout(self, *args):
        super(PaperLayout, self).do_layout(*args)
        for layer in self.layers:
            layer.draw()

    def on_touch_down(self, touch):
        current_point = None

        if current_point is not None:
            if self.IS_SELECTING:
                self.last_point = current_point
                self.IS_SELECTING = False
                self.new_step()
            else:
                self.first_point = current_point
                self.IS_SELECTING = True
                #touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        #touch.ud['line'].points += [touch.x, touch.y]
        pass

    def new_step(self):
        print "New step !"


class PaperWidget(Widget):
    def __init__(self, **kwargs):
        super(PaperWidget, self).__init__(**kwargs)


class KamoshiPaintLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(KamoshiPaintLayout, self).__init__(**kwargs)


class LayersLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(LayersLayout, self).__init__(**kwargs)


class LayersSlider(Slider):
    def __init__(self, **kwargs):
        super(LayersSlider, self).__init__(**kwargs)


class KamoshiCreatorMain(Widget):
    def __init__(self, **kwargs):
        super(KamoshiCreatorMain, self).__init__(**kwargs)


class KamoshiCreatorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(KamoshiCreatorLayout, self).__init__(**kwargs)


class KamoshiCreatorApp(App):
    def build(self):
        return KamoshiCreatorLayout()

if __name__ == '__main__':
    KamoshiCreatorApp().run()