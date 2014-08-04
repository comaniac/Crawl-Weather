#! /usr/bin/python
# -*- coding: utf-8 -*-

# A time slice, recording related information
class TIME_WEATHER (object):
  thisDate = ''
  thisTime = 0
  thisTemp = 0
  thisMoisture = 0
  thisRain = 0
  thisVol = -1

  def __str__(self):
    if self.thisVol == -1:
      return str(self.thisDate) + "\t" + str(self.thisTime) + "\t" + str(self.thisTemp) + "\t" + str(self.thisMoisture) + "\t" + str(self.thisRain)
    else:
      return str(self.thisDate) + "\t" + str(self.thisTime) + "\t" + str(self.thisTemp) + "\t" + str(self.thisMoisture) + "\t" + str(self.thisVol)

  def __eq__(self, another):
    return (self.thisDate == another.thisDate and self.thisTime == another.thisTime and self.thisTemp == another.thisTemp and self.thisMoisture == another.thisMoisture and self.thisRain == another.thisRain and self.thisVol == another.thisVol)


import datetime
class GMT8(datetime.tzinfo):
	def utcoffset(self, dt):
		return datetime.timedelta(hours=8)

	def dst(self, dt):
		return datetime.timedelta(0)

def remove_duplicate(table):
	newTable = []
	for e in table:
		found = False
		for p in newTable:
			if e.thisDate == p.thisDate and e.thisTime == p.thisTime:
				found = True
				break
		if not found:
			newTable.append(e)
	return newTable
