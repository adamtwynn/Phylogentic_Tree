#!/usr/bin/python
import time
import sys
import numpy as np
import networkx as nx
import pygraphviz


#WPGMA function

def WPGMA(matrix):
    #open file and generate matrix
    file1 = open(matrix, 'r')
    if sys.version_info >= (3, 0):
        matrix = np.genfromtxt(matrix, dtype=None, encoding=None)
    else:
        matrix = np.genfromtxt(matrix, dtype=None)
    m = matrix.tolist()
    file1.close()
    #start timer
    start = time.time()
    tree=nx.Graph()
    #print original matrix
    print(m)
    
    for k in range(0,len(m)-3):

        #find minimum value
        smallest = float(m[2][1])
        x = m[0][1]
        y = m[2][0]
        xpos = 1
        ypos = 2
        n = 1

        for i in range(1, len(m)):
            n = n + 1
            for j in range(n, len(m)):
                temp = float(m[i][j])
      
                if float(temp) < smallest and float(temp) != 0:
                    smallest = temp
                    x = m[0][j]
                    y = m[i][0]
                    xpos = j
                    ypos = i



        #merge columns in correct place
        if x[0] < y[0]:
            species1 = x
            species2 = y
        else:
            species1 = y
            species2 = x              
        m[0][ypos] = species1+species2
        m[ypos][0] = species1+species2

        #add nodes and edges to tree
        tree.add_node(species1)
        tree.add_node(species2)
        tree.add_node(species1+species2)
        tree.add_edge(species1,species1+species2)
        tree.add_edge(species2,species1+species2)

        #caluclate averages for each value and replace values in column
        
        for i in range(1, len(m)):
            if  float(m[ypos][i]) == 0.0:
                m[i][ypos] = 0
                m[ypos][i] = 0

            elif float(m[xpos][i]) != 0.0:
                newvalue = (float(m[i][xpos]) + float(m[ypos][i]))/2
                m[i][ypos] = newvalue
                m[ypos][i] = newvalue
  
        #remove old row/column
        m.pop(xpos)
        for i in range(0, len(m)):
             del m[i][xpos]
        print(m)

    #add last nodes
    tree.add_node(m[0][1])
    tree.add_node(m[0][2])
    tree.add_node(m[0][1]+m[0][2])
    tree.add_edge(m[0][1],m[0][1]+m[0][2])
    tree.add_edge(m[0][2],m[0][1]+m[0][2])

    #draw and save graph
    T = nx.nx_agraph.to_agraph(tree)
    T.layout('dot')
    T.draw('tree.png')

    #Stop timer
    stop = time.time()
    time_taken=stop-start
    print(time_taken) 
    

