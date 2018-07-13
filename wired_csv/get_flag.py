#!/bin/env python


import fastcsv	# Quick csv reading
import io

# Comma indexed, ie k0 is the word after the fourth comma
ks = [4,6,8,  10,12,14]

kr1 = 16
kr2 = 18

# Mapping for key strober in/out
pin2pos_in = {
	4 : 10,
	6 : 11,
	2 : 12, 
	7 : 13,
	5 : 14,
	1 : 15,
	0 : 16,
	3 : 17,
}

pin2pos_out = {
	1 : 1,
	4 : 2,
	6 : 3,
	2 : 4,
	7 : 5,
	0 : 6,
	3 : 7,
	5 : 8,
}

# Zero to one, one to zero
o2o = { 0 : 1, 1: 0}

# Key mapping for atari keyboard input
keyboard = {
	(1,10): "7",
	(2,10) : "6",
	(3,10) : "U",
	(4,10) : "Y",
	(7,10) : "N",
	(5,11) : "J",
	(6,11) : "H",
	(7,11) : " ",
	(1,12) : "8",
	(2,12) : "5",
	(3,12) : "I",
	(4,12) : "T",
	(5,12) : "K",
	(6,12) : "G",
	(7,12) : "M",
	(8,12) : "B",
	(1,13) : "9",
	(2,13) : "4",
	(3,13) : "O",
	(4,13) : "R",
	(5,13) : "L",
	(6,13) : "F",
	(7,13) : ",",
	(8,13) : "V",
	(1,14) : "0",
	(2,14) : "3",
	(3,14) : "P",
	(4,14) : "E",
	(5,14) : ";",
	(6,14) : "D",
	(7,14) : ".",
	(8,14) : "C",
	(1,15) : "<",
	(2,15) : "2",
	(3,15) : "-",
	(4,15) : "W",
	(5,15) : "+",
	(6,15) : "S",
	(7,15) : "/",
	(8,15) : "X",
	(1,16) : ">",
	(2,16) : "1",
	(3,16) : "=",
	(4,16) : "Q",
	(5,16) : "*",
	(6,16) : "A",
	(8,16) : "Z",
	(1,17) : "del",
	(2,17) : "esc",
	(3,17) : "\\n",
	(4,17) : "\t",
	(6,17) : "cps"
}


def find_time(time):
	ret = [-1]*6
	times = [-1]*6
	last_times = times
	with fastcsv.Reader(io.open("data.csv")) as reader:
		for row_num, row in enumerate(reader):
			if row_num == 0:
				continue
			for i,k in enumerate(ks):
				if row[k-1].strip() == '':
					continue
				# if the key changed after that point in time, don't change the value
				if float(row[k-1]) <= time:
					times[i] = float(row[k-1])
					ret[i] = int(row[k])
				elif ret[i] == -1:
					if abs(float(row[k-1])-time) < 3e-07 and abs(float(row[k-1])-time) < abs(float(times[i])-time):
						times[i] = float(row[k-1])
						ret[i] = int(row[k])

				#print('\r', time, "->", times, end='\r')

				

	#print()
	return ret



### MAIN PROGRAM FLOW

result = ""

kr1_last = 999
last_time = 0
count = 1
output = ""

print("OUTPUT:")
with fastcsv.Reader(io.open("data.csv")) as reader:
	for row_num,row in enumerate(reader):
		if row_num == 0:
			continue
		if row[kr1].strip() == '':
			break
		if int(row[kr1]) != kr1_last:
			if int(row[kr1]) == 0:

				if abs(float(row[kr1-1])-last_time) < 0.05:
					continue
				last_time = float(row[kr1-1])

				ktimes = find_time(float(row[kr1-1]))
				
				if -1 in ktimes:
					print("Could not find time %s" % row[kr1-1].strip() + ": " + str(ktimes))
					exit(1)

				for i,k in enumerate(ktimes):
					#ktimes[i] = o2o[int(k)]
					pass

				k012 = ktimes[:3]
				k345 = ktimes[3:]

				k012.reverse()
				k345.reverse()

				k012_s = "".join(str(k) for k in k012)
				k345_s = "".join(str(k) for k in k345)


				k012_b = int(k012_s,2)
				k345_b = int(k345_s,2)

				p_in = pin2pos_in[k012_b]
				p_out = pin2pos_out[k345_b]

				char = keyboard[(min(p_in,p_out),max(p_in,p_out))]
				result += char
				output += "line:" + str(row_num) +" "+ "%.9f" % float(row[kr1-1]) + " " + str(k012_s) + "-" + str(k012_b) + " " + str(k345_s) + "-" + str(k345_b) + " " + str((min(p_in,p_out),max(p_in,p_out))) + " " + str(char) + "\n"
				count += 1
				for i in range(count-1):
					print('\x1b[1A\x1b[2k', end='\r')
					i += 1
				print("OUTPUT:",result, "\n", output,end='\r')


			kr1_last = int(row[kr1])


print(result)
