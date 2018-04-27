# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 16:17:58 2018

@author: sanketchobe
"""

import numpy as np
import math
import argparse
import networkx as nx
import community as com
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from enum import Enum
import random
from random import randint
from networkx.algorithms.community import k_clique_communities 
from networkx.algorithms.community.centrality import girvan_newman
from networkx.algorithms.community import asyn_lpa_communities
from networkx.algorithms.community.quality import coverage
from networkx.algorithms.community.quality import performance
#from networkx.algorithms.community import LFR_benchmark_graph

    

To_Property =['Ballys','Caesars Palace','Cromwell','Flamingo','Harrahs_LV','Linq','Paris','Planet Hollywood','Rio']
To_Timestamp =['9/12/2015  12:08:00 PM','9/13/2015  2:00:00 PM','9/13/2015  2:58:00 PM','9/14/2015  3:48:00 AM','9/14/2015  11:05:00 AM','9/12/2015  9:51:00 PM','9/13/2015  8:52:00 AM']
Property_Region =['["Harrahs Lobby"]','["Ballys Lobby"]','["Ballys Conference Room"]','["Gaming"]','["Level 0"]','["Cromwell-Gaming"]','["Paris Restaurent"]','["Bacchannal Buffet"]','["Omnia Club"]'
                  ,'["Yard House"]','["Cromwell-Valet"]']
    
start_time = datetime.now()

#H =nx.gnp_random_graph(1000,0.60)
#H = nx.Graph()
#H =nx.read_gml('karate.gml',label='id')
H=nx.binomial_graph(200,0.60)

#edge_list =pd.read_csv('email-EU-core.txt',delimiter ='\t',header=None)
c=0
node_list =pd.read_csv('caesars_way_find.txt',delimiter ='\t',index_col=False)
for i,val in H.nodes(data=True):
    H.node[i]['Patron_Id'] =node_list['Patron_Id'][c]
    H.node[i]['From_Property'] =node_list['From_Property'][c]
    H.node[i]['From_Timestamp'] =node_list['From_Timestamp'][c]
    if node_list['To_Property'][c] >'':
        H.node[i]['To_Property'] =node_list['To_Property'][c]
    else:
        H.node[i]['To_Property'] =random.choice(To_Property)
    if node_list['To_Timestamp'][c] >'':
        H.node[i]['To_Timestamp'] =node_list['To_Timestamp'][c]
    else:
        H.node[i]['To_Timestamp'] =random.choice(To_Timestamp )
    if node_list['Property_Region'][c] =='[]':
        H.node[i]['Property_Region'] =random.choice(Property_Region )
    else:
        H.node[i]['Property_Region'] =node_list['Property_Region'][c]
    c=c+1
nx.write_edgelist(H,'caesars_edgelist.txt',delimiter ='\t',data=False)   
pos=nx.random_layout(H)
plt.figure()
nx.draw_random(H)
plt.show()

k_core =min(H.degree(nx.k_core(H).nodes()),key=lambda item:item[1])
print 'k-core of graph:',k_core[1]
"""
comm1_start_time = datetime.now()
comm1 = list(k_clique_communities(H,5))
print 'community k-clique:', len(comm1)
comm1_end_time = datetime.now()
print('Duration: {}'.format(comm1_end_time - comm1_start_time))
"""
print 'number of nodes:', len(H.nodes()), 'number of edges:', len(H.edges())
start_time = datetime.now()
prob_dict ={}
prob1_dict ={}
c =0
for item, dict1 in H.nodes(data=True):
      for key, value in dict1.items():
          if (key, value) in prob_dict.keys():
              prob_dict[(key,value)] =prob_dict[(key, value)] +1
          else:
              prob_dict[(key, value)] =1

#print 'prob-dict:', prob_dict
for key, value in prob_dict.items():
    if (float(float(value)/float(len(H.nodes()))) * 100) >= 10.0:
        prob1_dict[key] =float(float(value)/float(len(H.nodes()))) * 100

prob_dict =sorted([{v:k} for (k,v) in prob1_dict.items()], reverse=True)
print 'prob-dict:', prob_dict
class_dict ={}
i =0 
for item in prob_dict:
    for key, value in item.items():
        class_dict[value] = i
    i =i+1
print 'class-dict:', class_dict

atr_index ={}
atr_list =[]
for item, dict1 in H.nodes(data=True):
    for key, value in dict1.items():
        if (key, value) in class_dict.keys():
            atr_list.append(class_dict[(key, value)])
    atr_index[item] =atr_list
    atr_list =[]

print 'attribute node index:', atr_index

"""
calculate probability of edge attributes
"""
node_clss ={}
node_clss2 ={}
atr_index2 ={}
prob_matrix = np.zeros(shape=(len(class_dict),len(class_dict)))
prob_matrix1 = np.zeros(shape=(len(class_dict),len(class_dict)))
for edge in H.edges():
    list1 =[]
    list2 =[]
    list3 =[]
    list1 = atr_index[edge[0]]
    list2 = atr_index[edge[1]]
    list3 =set(list1).intersection(set(list2))
  #  print 'list3:', list3
    if len(list3) >0:  
        for it1 in list3:
            for it2 in list3:        
                prob_matrix[int(it1), int(it2)] = prob_matrix[int(it1), int(it2)] +1
            
    for it in list3:       
        if it in node_clss.keys():
            node_clss[it] =node_clss[it] +1
        else:
            node_clss[it] =1

"""
for i in range(len(class_dict)):
    for j in range(len(class_dict)):
   #     print node_clss[i+1]
    #    print node_clss[j+1]
        eij = abs(float(float((node_clss[i+1] * node_clss[j+1]))/float(len(H.edges()))))
     #   print eij
        if eij > 0:
            prob_matrix1[i,j] =abs(float(float(prob_matrix[i,j] - eij)/float(np.sqrt(eij*(1 -float(node_clss[i+1]/float(len(H.edges()))))*(1 -float(node_clss[j+1]/float(len(H.edges()))))))))
        else:
            prob_matrix1[i,j] =0.0
print 'attr edge count:', prob_matrix, prob_matrix1
"""
for key, val in node_clss.items():
    val1 =float(float(val)/float(len(H.edges()))) *100
    if val1 >= 1.0:
        node_clss2[key] =val1               
        
print 'attr edge count:', node_clss2

       
#print 'communities:',nx.algorithms.community.girvan_newman(H)
 
Attr_Index1 ={}
attr_list =np.zeros(len(class_dict))
for item, dict1 in H.nodes(data=True):
    deg = H.degree(item)
    attr_list =[]
    for key, val in dict1.items():
        if (key, val) in class_dict.keys():
            if class_dict[(key, val)] in node_clss2.keys():
           #     print 'node attr clss:', class_dict[(key, val)], node_clss2[class_dict[(key, val)]]
                attr_list.append(class_dict[(key, val)])
   # print 'attr list:', item, attr_list
    Attr_Index1[item] =attr_list

print "Attribute Index structure", Attr_Index1, len(H.nodes())
              
cl=0   
attr_index_class ={}
attr_class_dict={}
attr_list1 =[]
attr_list2 =[]
clss_list =[]
clss =[]
l1 =0
l2 =0
count =0
for node, sig in H.nodes(data=True):
    list1 = Attr_Index1[node]
    deg = H.degree(node)
    clss_list=[]
   # print 'list1:', list1, deg, k_core[1], 'node:', node
    l2 =0
    if deg >= k_core[1] and len(list1) >0:
        if not attr_index_class:
            if l2 ==0:
                cl = cl+1
                count =count+1
                attr_index_class[cl] ={'node':node, 'attr': list1, 'count':count}
                attr_class_dict[cl] =list1
              #  print 'attr clss:', attr_index_class, cl
                clss_list.append(cl)
                sig['class'] = clss_list
            l2 =l2+1
        else:
            for key, dict1 in attr_index_class.items():
                list2 = dict1['attr']
              #  print 'list2:', list2, 'list1:', list1
                jcd = float(float(len(set(list1).intersection(set(list2))))/float(len(set(list1).union(set(list2))))) * 100
                union = list(set(list1).union(set(list2)))
                diff = set(list1).difference(set(list2))
                common = set(list1).intersection(set(list2))
               # print 'jcd:', jcd, 'diff:', diff, 'attr_indx:', attr_index_class
                if jcd >= 60.0:
                    l1=l1+1
                    if len(diff) ==0:
                        dict1['count']=dict1['count'] +1
                    else:
                        dict1['attr'] = union
                        dict1['count']=dict1['count'] +1
                        attr_class_dict[key] =union
                    if 'class' not in sig.keys():
                        clss_list.append(key)
                        sig['class'] = clss_list
                    else:
                        if key in sig['class']:
                            continue
                        else:
                            clss_list = sig['class']
                            clss_list.append(key)
                            sig['class']= clss_list
                    break
                else:
                    if len(common) >0:
                        if len(list1) < len(list2):
                            if set(list1).issubset(set(list2)):
                                c =c+1
                                attr_index_class[key]['attr'] =list(set(list1).union(set(list2)))
                                attr_index_class[key]['count']=attr_index_class[key]['count'] +1
                                attr_class_dict[key] =list(set(list1).union(set(list2)))
                                if 'class' not in sig.keys():
                                    clss_list.append(key)
                                    sig['class'] = clss_list
                                else:
                                    if key in sig['class']:
                                        continue
                                    else:
                                        clss_list = sig['class']
                                    clss_list.append(key)
                                    sig['class']= clss_list
                                break
                        else:                     
                            for it in list1:
                                if it in list2:
                                    c =c+1
                                    attr_index_class[key]['attr'] =list(set(diff).union(set(list2)))
                                    attr_index_class[key]['count']=attr_index_class[key]['count'] +1
                                    attr_class_dict[key] =list(set(diff).union(set(list2)))
                                    if 'class' not in sig.keys():
                                        clss_list.append(key)
                                        sig['class'] = clss_list
                                    else:
                                        if key in sig['class']:
                                            continue
                                        else:
                                            clss_list = sig['class']
                                            clss_list.append(key)
                                            sig['class']= clss_list
                                    break
                      #  for it in list(diff):
                        #    if it in attr_class_dict.values():
                       #         c =c+1
                    
                            
           #     print 'node signature:', sig, l1
            if l1 ==0 and c==0 and jcd < 60.0:    
                cl =cl+1
                count =count+1
                attr_index_class[cl] ={'node':node, 'attr': list1, 'count':count}
                attr_class_dict[cl] =list1
                        
                if 'class' not in sig.keys():
                        clss_list.append(cl)
                        sig['class'] = clss_list
                else:
                    if cl in sig['class']:
                        continue
                    else:
                        clss_list = sig['class']
                        clss_list.append(cl)
                        sig['class']= clss_list
               # print sig['class']
            l1 =0
            list2 =[]
           # print 'node signature:', sig
            c=0                                   
    list1 =[]
    count =0
    attr_list1 =[]
    attr_list2 =[]
                    


print 'attribute index structure\n:', attr_index_class
#print 'nodes with attributes:\n', H.nodes(data =True)

comm1 ={}
comm2 ={}  
nodelist =[]  
for cl in attr_index_class.keys():
    item =attr_index_class[cl]['node']
    if H.degree(item) >= k_core[1] and 'class' in H.node[item].keys():
        node_count =attr_index_class[cl]['count']
        itm_lst =nx.algorithms.bfs_tree(H,item)
        while count <= node_count:
            for itm in itm_lst.nodes():
                if H.degree(itm) >=k_core[1] and 'class' in H.node[itm].keys():
                    count =count+1
                    signature =H.node[itm]['class']
                    #print signature
                    if cl in signature:
                        if not nodelist:
                            nodelist.append(item)
                #       print 'path1:',nx.shortest_path_length(H,source=item, target=itm), 'source:', item, 'target:', itm
                            if (nx.shortest_path_length(H,source=item, target=itm)) <=3:
                #        print 'shortest path length:',nx.shortest_path_length(H,source=item, target=itm),'source:',item,'target:',itm
                   # if (H.has_edge(item,itm) or H.has_edge(itm,item)):
                                nodelist.append(itm)
                        else:
                            for it in nodelist:
                    #    print 'path2:',nx.shortest_path_length(H,source=itm, target=it), 'source:', itm, 'target:', it
                                if (nx.shortest_path_length(H,source=itm, target=it)) <=3:
                  #          print 'shortest path length:',nx.shortest_path_length(H,source=itm, target=it),'source:',itm,'target:',it
                      #  if (H.has_edge(itm,it) or H.has_edge(it,itm)):
                                    if itm in nodelist:
                                        continue
                                    else:
                                        nodelist.append(itm)
        print('query2:',cl,'nodelist:',nodelist)
        comm1[cl] =set(nodelist)
        pos =nx.random_layout(H)
        k =nx.Graph(H.subgraph(nodelist))
        comm2[cl] =k.edges()
   #     print('query2:',cl,'is graph connected:',nx.is_connected(k))
        #print('query2:',cl,'subgraph edges:',k.edges())
   # print('is it a partition:',nx.algorithms.community.is_partition(H,nodelist))
        plt.figure()
        nx.draw(k,node_size=1500,pos=pos,node_color='y', with_labels=True)
        plt.show()
        count =0
        nodelist =[]
        
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

"""
color =['r','g','y','m','c']
for cl,nod in comm1.items():
    x=random.choice(color)
    nx.draw_networkx(nx.Graph(H.subgraph(nod)),nx.spring_layout(H),with_labels=True,nodelist=nod,edge_list=H.edges(),node_size=1500,node_color=x,edge_color=x)   
plt.show()
"""