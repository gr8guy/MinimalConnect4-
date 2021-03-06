# -*- coding: utf-8 -*-
"""
Created on Thu May 22 14:34:20 2014

@author: ankur
"""



#Change the number of ROWS and COLUMNS here for your graph
COLUMN = 20
ROW = 20
#COLUMN = 35
#ROW = 22


#Give source and destination values
SOURCE = (0,10)
DEST = (15,1)


import propython as profiler
import networkx as nx
import matplotlib.pyplot as plt

pos = None
def read_file_draw_graph():
    global pos
    with open('sample.txt') as file:
        array2d = [[int(digit) for digit in line.split()] for line in file]
    
    #Number the nodes using this count value
    #pos is the i,j index of the node, left bottom - 0,0
    count = 1 
    G = nx.Graph()    
    for j in range(COLUMN):
        for i in range(ROW):
            if array2d[ROW-1-i][j] == 0:
                G.add_node(count,pos=(j,i))
            count +=1 
  
    pos=nx.get_node_attributes(G,'pos')
 
    #fetch the attribute position and correspondingly create the edges   
    for index in pos.keys():
        for index2 in pos.keys():
            if pos[index][0] == pos[index2][0] and pos[index][1] == pos[index2][1] -1 :
                G.add_edge(index,index2,weight=1)
            if pos[index][1] == pos[index2][1] and pos[index][0] == pos[index2][0] -1 :
                G.add_edge(index,index2,weight=1)

    return G

#returns the node with minimum distance value + index    
def minimum_distance_node(unvisited_nodes):
    
 
    nodeIndex = None
    minDistance = float("inf")
    for k in unvisited_nodes:
        if  G.node[k]['distance'] < minDistance:
            minDistance = G.node[k]['distance']
            nodeIndex = k
    
    return nodeIndex,minDistance

#Takes source and destination indexes in the graph as input   
def dijkstra(G,source,destination):
    
    fringe = G.nodes()
    paths = {source:[source]}
   
    #all nodes at infinite distance    
    for n in fringe:
         G.add_node(n,distance=float("inf"),visited=False)
    node_distance = nx.get_node_attributes(G,'distance') 
    
    #source at distance 0
    G.add_node(source,distance=0,visited=True)

    while len(fringe) !=0:

        minDistNodeIndex, distanceMin = minimum_distance_node(fringe)
        
        #just to optimize, if destination is found break here
        #remove this line to find out all the paths
        if ( minDistNodeIndex == destination):
            break
        #print "minDistNodeIndex",minDistNodeIndex
        G.add_node(minDistNodeIndex,visited=True)
        
        #mark this node visited and remove from nodes for consideration
        neighbors = G.neighbors(minDistNodeIndex)
        fringe.remove(minDistNodeIndex)
        
        
        unvisited_neighbors = [neighbor for neighbor in neighbors if G.node[neighbor]['visited'] == False ]
              
        for n in unvisited_neighbors: 
            edge_data_of_node = G.get_edge_data(minDistNodeIndex,n)
       
            if distanceMin + edge_data_of_node['weight'] < node_distance[n]:
                node_distance[n] = distanceMin + edge_data_of_node['weight']
                
                #update the new distance and store it in the path                
                G.add_node(n,distance=node_distance[n])
                paths[n] = paths[minDistNodeIndex] + [n]
              
    return G,paths  
    
    
    
if __name__ == "__main__":

    G = read_file_draw_graph()
    for n in G.nodes():
        if G.node[n]['pos'] == SOURCE:
            source = n 
        if G.node[n]['pos'] == DEST:
            destination = n
    
    print source, destination
    G, paths = dijkstra(G,source,destination)
    
    #Uncomment this to profile your code
    '''
    t1 = 0 
    for i in range(0,1000):
        timer = profiler.timewith()
        
        G, paths = dijkstra(G,10,302)
        t1 += timer.checkpoint()
    
    print t1/1000  #0.025826000452
    '''
    
    print paths[destination]
    nx.draw(G,pos)
    nx.draw(G,pos,nodelist=paths[destination],node_color = 'b')
    plt.show()
    