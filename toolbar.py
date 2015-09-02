#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------
#       KAMOSHI CREATOR         |
#                  v0.1         |
#--------------------------------

from kivy.uix.widget import Widget

__author__ = 'Temigo'


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