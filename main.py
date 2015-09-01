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
from kivy.uix.scatterlayout import ScatterLayout
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.slider import Slider

from math import sqrt
__author__ = 'Temigo'

#Builder.load_file('kamoshicreator.kv')


class GraphicEdge(Widget):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super(GraphicEdge, self).__init__(**kwargs)
        self.points = [x1, y1, x2, y2]

    def draw(self):
        print "Drawing edge"
        with self.parent.parent.canvas:
            Color(0, 0, 0)
            Line(points=self.points, width=1.0)


class GraphicPoint(Widget):
    d = 30.  # Diameter

    def __init__(self, x, y, **kwargs):
        super(GraphicPoint, self).__init__(**kwargs)
        self.pos_hint = {'x': x, 'y': y}
        self.size_hint=(None, None)
        self.size = (self.d, self.d)

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
        self.size = self.parent.size
        self.pos = self.parent.pos
        with self.parent.canvas:
            Color(0, 1, 0, 0.5)
            Rectangle(pos=self.pos, size=self.size)
            for point in self.points:
                point.draw()

            for edge in self.edges:
                edge.draw()
            print "Drawing LayerLayout"

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
            self.canvas.clear()  # FIXME efface les layers antérieures ?
            if self.recto:  # color according to recto/verso
                Color(1, 0, 0, 0.5)
            else:
                Color(1, 1, 1, 0.5)  # White
            Rectangle(pos=self.pos, size=self.size)  # Paper
        self.layout.draw()

    def on_touch_down(self, touch):
        super(Layer, self).on_touch_down(touch)
        print "Touch ! Layer"


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
    layers = [Layer(points=[GraphicPoint(0, 0), GraphicPoint(1, 0), GraphicPoint(0, 1), GraphicPoint(1, 1)],
                    edges=[GraphicEdge(0, 0, 1, 0)])]
    current_layer = 0
    current_point = None

    def __init__(self, **kwargs):
        super(PaperLayout, self).__init__(**kwargs)
        for layer in self.layers:
            self.add_widget(layer)

    def do_layout(self, *args):
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