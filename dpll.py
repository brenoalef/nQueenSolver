#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Breno Alef Dourado Sá'

import sys
import copy

def dpll(clauses, val):
	clauses1 = copy.deepcopy(clauses)
	clauses1, val = simplify(clauses1, val)
	if len(clauses1) == 0:
		return val
	if [] in clauses1:
		return False
	atomic = atoms(clauses1)[0]
	clauses2 = copy.deepcopy(clauses1)
	clauses2.append([atomic])
	val2 = copy.deepcopy(val)
	result = dpll(clauses2, val2)
	if result != False:
		return result
	clauses2 = copy.deepcopy(clauses1)
	clauses2.append([-atomic])
	val2 = copy.deepcopy(val)
	result = dpll(clauses2, val2)
	return result


def simplify(clauses, val):
	clauses1 = copy.deepcopy(clauses)
	val1 = copy.deepcopy(val)
	while hasUnitClause(clauses1):
		literal = pureLiteral(clauses1)
		if literal not in val1:
			val1.append(literal)
		clauses1 = removeClausesWith(clauses1, literal)
		clauses1 = removeComplementLit(clauses1, literal)
	return clauses1, val1


def hasUnitClause(clauses):
	for clause in clauses:
		if len(clause) == 1:
			return True
	return False


def pureLiteral(clauses):
	for clause in clauses:
		if len(clause) == 1:
			return clause[0]
	return None


def removeClausesWith(clauses, literal):
	newClauses = []
	for clause in clauses:
		if literal not in clause:
			newClauses.append(clause)
	return newClauses


def removeComplementLit(clauses, literal):
	newClauses = []
	for clause in clauses:
		if -literal in clause:
			clause.remove(-literal)
		newClauses.append(clause)
	return newClauses


def atoms(clauses):
	atoms = []
	for clause in clauses:
		for p in clause:
			if abs(p) not in atoms:
				atoms.append(abs(p))
	return atoms


def readDimacs(dimacsFilePath):
	dimacsFile = open(dimacsFilePath, "r")
	clauses = []
	v = -1
	c = -1
	for line in dimacsFile:
		if line.startswith('c'):
			continue
		elif line.startswith('p'):
			s = line.split(" ")
			v = int(s[2])
			c = int(s[3])
			if s[1] != "cnf":
				raise ValueError("The file isn't in CNF")
		else:
			clause = []
			for p in line.split(" "):
				clause.append(int(p))
			if clause[-1] != 0:
				raise ValueError("Clause does not end with a 0 [%s]" % line)
			clauses.append(clause[:-1])
	dimacsFile.close()
	if c != len(clauses):
		raise ValueError("Number of clauses differs from the expected")
	if v != len(set([abs(p) for clause in clauses for p in clause])):
		raise ValueError("Number of vars differs from the expected")
	return clauses

if __name__ == '__main__':
	
	argv = sys.argv
  	if len(argv) != 2:
    		print("Usoage: %s <dimacs file path>" % argv[0])
    		quit()
    	
    	clauses = readDimacs(argv[1])
    	
    	result = dpll(clauses, [])
    	
    	if result != False:
    		print(result)
    	else:
    		print("Unsatisfiable")

