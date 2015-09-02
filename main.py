#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------
#       KAMOSHI CREATOR         |
#                  v0.1         |
#--------------------------------

#import kivy
#kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget

# Used in kv file
from paper import PaperLayout
from toolbar import Toolbar

__author__ = 'Temigo'


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