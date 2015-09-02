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

from graphic import GraphicEdge, GraphicPoint
from layer import Layer, LayerLayout

__author__ = 'Temigo'

#Builder.load_file('kamoshicreator.kv')


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
    first_point = None  # When selecting a couple of points
    last_point = None
    layers = ListProperty([Layer(points=[GraphicPoint(0, 0), GraphicPoint(1, 0), GraphicPoint(0, 1), GraphicPoint(1, 1)],
                    edges=[GraphicEdge(0, 0, 1, 0)])])
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
        with self.canvas:
            #self.canvas.clear()
            self.do_layout()
        super(PaperLayout, self).on_layers(instance, value)

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
        if a == b:
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

            for point in layer.layout.points:
                print point, len(layer.layout.points)
                # Position par rapport à la médiatrice
                b1, b2 = self.is_under_bisector(point.x, point.y, x1, y1, x2, y2)
                if b1:
                    points_to_translate.append(point)
                    keep_point[point] = b2
                    #layer.remove_point(point)

            for point in points_to_translate:
                point.mirror(x1, y1, x2, y2)
                layer.remove_point(point)
                if keep_point[point]:
                    new_point = GraphicPoint(0, 0)
                    new_point.x = point.x
                    new_point.y = point.y
                    layer.add_point(new_point)

            # TODO flip color
            new_layer = Layer(points=points_to_translate)  # TODO : edges
            self.layers.insert(i, new_layer)
        print self.layers


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