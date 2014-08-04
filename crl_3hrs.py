#! /usr/bin/python
# -*- coding: utf-8 -*-
# File Name		: crl_3hrs.py
# Author			 : 
# Creation Date: 2014 06 06 02:22 

from timeweather import *
import datetime
from urllib import urlopen

# Fetch source HTML of specified page
# Return: Page source, or exit if exception.
def get_page(url):
	try:
		page = urlopen(url).read()
		return page

	except Exception, err:
		print "Fail to get the page: " + str(err)
		exit()

# Assign new weather data into the table.
# Return: A table with filled data.
def fill_data(table, inlist, attr):
	if not table: # Create a new table for this execution
		table = [TIME_WEATHER() for unuse in range(len(inlist))]

	datetime.timedelta(days=1)
	count = 0
	delta = 0
	for e in inlist:
		if attr == 'thisTime':
			if e == 0: # Date plus 1 if over the midnight
				delta += 1
			today = str(datetime.datetime.now(GMT8()) + datetime.timedelta(days=delta))
			table[count].thisDate = today[:today.find(' ')]

		# Fill in corresponding attr. 
		exec('table[count].' + str(attr) + ' = e')
		count += 1
	return table

# Union table1 and table2, and sort it by date and time.
# Return: A table union by table1 and table2.
# Notice: Union direction is table1 <-- table2.
def union(table1, table2):
	newTable = []
	newTable += table1
	for p in table2:
		found = False
		for q in table1:
			if p == q:
				found = True
				break
		if found == False:
			newTable.append(p)
	from operator import attrgetter
	return sorted(newTable, key=attrgetter('thisDate', 'thisTime'))

# Find all tag ... endtag
# Return: A list with text in specified tag
def find_tag_text(instr, tag, endtag):
	resultList = []
	curPos = 0

	while True:
		curPos = instr.find(tag, curPos)
		if curPos == -1:
			break
		endPos = instr.find(endtag, curPos)
		resultList.append(instr[curPos + len(tag):endPos])
		curPos = endPos + 1
	
	return resultList

# Remove all tags (Reg: <(\w+)>)
# Same as ".text" in BeautifulSoup4
# Return: the string without any tag
def remove_all_tag(instr):
	s = ""
	fetch = True

	for ch in instr:
		if ch == '<' or ch == '>':
			fetch = not fetch
		if fetch and ch != '>' and ch != ' ':
			s += ch
	
	return s

# Fetch "number" (including float numbers).
# Return: the number in string type
def fetch_num(instr):
	nstr = ""
	for ch in instr:
		if not ch.isdigit() and ch != '.':
			break
		nstr += ch
	return nstr

# Fetch weather data from page source.
# Return: A table with all filled data.
def fetch_weather(page_src):
	table = []
	import re
	
	for d_with_tag in find_tag_text(page_src, "<tr>", "</tr>"):
		d = remove_all_tag(d_with_tag)
		title = d[1:d.find('\n', 1)]
		if title == "時間":
			tempList = [int(fetch_num(str(e))) for e in re.split("\n", d[d.find("\n", 1) + 1:]) if e]
			table = fill_data(table, tempList, 'thisTime')
		elif title == "溫度(℃)": 
			tempList = [float(fetch_num(str(e))) for e in re.split("\n", d[d.find("\n", 1) + 1:]) if e]
			table = fill_data(table, tempList, 'thisTemp')
		elif title == "相對溼度": 
			tempList = [float(fetch_num(str(e))) for e in re.split("\n", d[d.find("\n", 1) + 1:]) if e]
			table = fill_data(table, tempList, 'thisMoisture')
		elif title == "降雨機率":
			tempList = [float(fetch_num(str(e))) for e in re.split("\n", d[d.find("\n", 1) + 1:]) if e]
			tempList = (tempList[:-1] * 4) + [tempList[-1]]
			table = fill_data(table, tempList, 'thisRain')	

	return table

# Dump table into a binary file by using pickle.
# If there has a existed file, then load and union with existed and new one.
def record_weather(table, filePath):
	try: # Load the old table if existed.
                # "/curr/cody/Application/crlWeather/record.pkl"
		f = open(filePath, "rb")
		from pickle import load
		oldTable = load(f)
		f.close()
		print "Record loading successed, load " + str(len(oldTable)) + " data."
		table = union(oldTable, table)
		print "New data: " + str(len(table) - len(oldTable))
	 
	except Exception, err: # Or create a new one.
		print "Record not found. Create a new one."
		pass

	try: # Write the new table into a binary file.
		f = open(filePath, "wb")
		from pickle import dump
		dump(table, f)
		f.close()

	except Exception, err:
		print "Fail to record table: " + str(err)

	# Display the final table.
	for e in table:
		print e

if __name__ == "__main__":
	from time import ctime
	from time import time
	import sys

	startTime = time()
	print "Program start at " + ctime()
	try:
		filePath = str(sys.argv[1])
	except Exception, err:
		print "Fail to get the path of record file: " + str(err)
                
	page_src = get_page("http://www.cwb.gov.tw/V7/forecast/town368/3Hr/6300200.htm")

	print "Fetching data..."
	table = fetch_weather(page_src)
	record_weather(table, filePath)
	print "Done. Execution time: " + str(time() - startTime)

