#!/usr/bin/python
# -*- coding: utf-8 -*-

#import kivy
#kivy.require('1.8.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button

from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Mesh, Point
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty
from kivy.uix.slider import Slider

from math import sqrt
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


class PaperWidget(Widget):
    select = ListProperty([(100, 100), (300, 300), (100, 300), (300, 100)])
    d = 30.
    IS_SELECTING = False
    first_point = None # When selecting a couple of points
    last_point = None

    def __init__(self, **kwargs):
        super(PaperWidget, self).__init__(**kwargs)
        (root_x, root_y) = self.pos
        with self.canvas:
            Color(1, 1, 0)
            for point in self.select:
                (x, y) = point
                Ellipse(pos=(x - self.d / 2+root_x, y - self.d / 2+root_y), size=(self.d, self.d))

    def on_touch_down(self, touch):
        current_point = None
        for point in self.select:
            (x, y) = point
            if sqrt(pow(x - touch.x, 2) + pow(y-touch.y,2)) <= self.d:
                current_point = point
                with self.canvas:
                    Color(1,0,0)
                    Ellipse(pos=(x - self.d / 2, y - self.d / 2), size=(self.d, self.d))
                break

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
        pass


class KamoshiPaintLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(KamoshiPaintLayout, self).__init__(**kwargs)


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