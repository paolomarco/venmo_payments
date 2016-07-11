# coding: utf-8

import json
import os.path
import sys
import numpy
import datetime
import networkx as nx
import matplotlib.pyplot as plt
from dateutil.parser import parse  
def median(lst):
    return numpy.median(numpy.array(lst))

inFile = sys.argv[1]
outFile = sys.argv[2]

payments = [json.loads(line) for line in open(inFile)] #load the data

created_time = payments[0]["created_time"] #extract time of first payment for max time stamp

max_time_stamp = parse(created_time) #assign max time stamp out of the for loop

G = nx.Graph() #initate a networkx graph
plt.ion()

output = open(outFile, "w")

counter = 0

for p in payments: #initiate for loop
    
    target = p['target'] #get target of p payment
    actor =  p['actor'] #get actor of p payment
    created_time = p['created_time'] #get created time of payment
    created_time = parse(created_time) #convert to datetime.datetime object
    
    if target is not None and actor is not None and created_time is not None:
        G.add_edge(actor, target, time= created_time)
        d = nx.degree(G)
        degrees = list(d.values())
        rolling_median = median(degrees)
        rolling_median = "{0:.2f}".format(rolling_median)
        output.write("%s\n" % rolling_median)
   
    elapsed_time = max_time_stamp - created_time #compute difference
    elapsed_seconds = elapsed_time.total_seconds() #in seconds
    
    if elapsed_seconds < 0: #check to see if the time of incoming transaction is bigger than previous max

        max_time_stamp = created_time #set new max if it is
        
    for v in G.edges(data=True): #loop through the current edges
          
            y = (v[2]) #extract the datetime object
            y = list(y.values()) #get the value out of the dictionary
            elapsed_time = max_time_stamp - y[0] #calculate time difference
            elapsed_seconds = elapsed_time.total_seconds() #convert to seconds
            
            if elapsed_seconds > 59: #if greater than 60 seconds
                
                G.remove_edge(*v[:2]) #remove the edge 
   
    disconnected = [node for node,degree in G.degree().items() if degree == 0]
    G.remove_nodes_from(disconnected)
    counter = counter + 1
    f = plt.figure()
    nx.draw(G, ax=f.add_subplot(111))
    os.makedirs(os.path.dirname('./images/'), exist_ok=True)
    f.savefig("./images/numberOfTransactionsRead" + str(counter) + ".png")
       
output.close()

