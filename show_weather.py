#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from timeweather import TIME_WEATHER
if len(sys.argv) > 1:
	from pickle import load
	f = open(sys.argv[1], "rb")
	table = load(f)
	f.close()
	for e in table:
		print e
	
