#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Breno Alef Dourado Sá'

#Number of problem constraints
clausesCount = 0

#At least one queen on each line
#(p1 ∨ ... ∨ p4) ∧ ... ∧ (p13 ∨ ... ∨ p16)
def existence(n):
	global clausesCount
	clauses = ""
	for i in range(0, n):
		value = ""
		for j in range(1,n+1):
			num = "" + str(j + n * i)
			value = str(value+num) + " "

		clauses += value+"0\n"
		clausesCount += 1
	return clauses

#Only one queen in each row
#(¬p1 ∨ ¬p2) ∧ (¬p1 ∨ ¬p3) ∧ (¬p1 ∨ ¬p4) ∧ (¬p2 ∨ ¬p3) ∧ ... ∧ (¬p15 ∨ ¬p16)
def rows(n):
	global clausesCount
	clauses = ""
	for i in range(0, n):
		for j in range(1, n):
			num = "" + str(j+n*i)
			for l in range(1, n - j + 1):
				aux = int(num) + l
				value = "-" + num + " -" + str(aux)
				clauses += value + " 0\n"
				clausesCount += 1
	return clauses

#Only one queen in each col
#(¬p1 ∨ ¬p5) ∧ (¬p1 ∨ ¬p9) ∧ (¬p1 ∨ ¬p13) ∧ (¬p5 ∨ ¬p9) ∧ ... ∧ (¬p12 ∨ ¬p16)
def cols(n):
	global clausesCount
	clauses = ""
	for j in range(1, n+1):
		for i in range(0, n):
			num = "" + str(j+n*i)
			for l in range(1, n-i):
				aux = int(num) + l * n #celula para combinacao
				value = "-" + num + " -" + str(aux)
				clauses += value + " 0\n"
				clausesCount += 1
	return clauses

#Only one queen in each diagonal
#(¬p1 ∨ ¬p6) ∧ (¬p1 ∨ ¬p11) ∧ (¬p1 ∨ ¬p16) ∧ (¬p2 ∨ ¬p5) ∧ ... ∧ (¬p12 ∨ ¬p15)
def diagonals(n):
	global clausesCount
	clauses = ""

	#superior left to right
	for i in range(0, n-1):
		for j in range(i, n-1):
			num = "" + str(j+1+n*i)
			for l in range(1, n-j):
				aux = int(num) + l * (n+1)
				value = "-" + num + " -" + str(aux)
				clauses += value + " 0\n"
				clausesCount += 1

	#inferior left to right
	for i in range(0, n-1):
		for j in range(0, i):
			num = "" + str(j + 1 + n * i)
			for l in range(1, n-i):
				aux = int(num) + l * (n + 1)
				value = "-" + num + " -" + str(aux)+ " 0"
				clauses += value + "\n"
				clausesCount += 1

	#superior right to left
	for i in range(0, n):
		for j in range(0, n-i):
			num = "" + str(j+1+n*i)
			for l in range(1, j+1):
				aux = int(num) + l * (n - 1)
				value = "-" + num + " -" + str(aux) + " 0"
				clauses += value + "\n"
				clausesCount += 1

	#inferior right to left
	for i in range(0, n):
		for j in range(n-i, n):
			num = "" + str(j+1+n*i)
			if((j + 1 + n * i) != (n * n)):
				for l in range(1, n-i):
					aux = int(num) + l * (n - 1)
					value = "-" + num + " -" + str(aux) + " 0"
					clauses += value + "\n"
					clausesCount += 1
	return clauses

def generateFile(n):
	if(n < 4):
		raise ValueError('Minimum dimension: 4')
		quit()

	res = ""
	res += existence(n)
	res += rows(n)
	res += cols(n)
	res += diagonals(n)

	file = open(str(n) +"queens.dimacs","w")
	file.write("c dimacs for the " + str(n) + " queens puzzle\n")
	file.write("p cnf " + str(n*n) + " " + str(clausesCount) + "\n")
	file.write(res)
	file.close()

if __name__ == '__main__':

	n = input("Board size: ")

	generateFile(n)

	print("Saved to: " + str(n) + "queens.dimacs")
