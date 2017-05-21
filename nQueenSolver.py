#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Breno Alef Dourado Sá'

from Tkinter import *
import nQueenCNF
import dpll

n = input("Board size: ")
nQueenCNF.generateFile(n)

clauses = dpll.readDimacs(str(n) + "queens.dimacs")

result = dpll.dpll(clauses, [])

if result != False:
	root = Tk()
	root.title(str(n) + ' queens')
	canvas = Canvas(root,bg='white',height=500,width=500)
	canvas.pack(side=TOP,padx=10,pady=10)
	queen = PhotoImage(file="queen.gif")
	queen = queen.subsample(n, n)
	board_rows=n
	board_cols=n
	x=1
	y=1
	square_size= 500/n
	for rows in range(board_rows):
		color_white = not (rows%2)
		for columns in range(board_cols):
			color="lightgray"
			if not color_white:
				color="red"
			x=columns*square_size
			y=rows*square_size
			canvas.create_rectangle(x, y, x+square_size, y+square_size, fill=color)
			if rows*n + columns + 1 in result:
				canvas.create_image(x, y, anchor = NW, image=queen)
			color_white = not color_white

	bou1 = Button(root,text='Close',width=25,command=root.quit)
	bou1.pack(side=RIGHT,padx=10,pady=10)

	root.mainloop()
else:
	print("Unsatisfiable")
