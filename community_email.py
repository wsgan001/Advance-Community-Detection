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
from networkx.readwrite import json_graph   
from networkx.algorithms.community import k_clique_communities 
from networkx.algorithms.community.centrality import girvan_newman
#from networkx.algorithms.community import LFR_benchmark_graph

World ={'city':['Las Vegas','Reliegh','New York','Los Angeles','Phoenix'],
      'school':['UNLV','UCLA','SUNY','NCSU','ASU'],
      'role':['Student','Professor','Athelte'],     
      'country':['USA']}



USA ={'city':['Las Vegas'],
      'school':['UNLV'],
      'employer':['Caesars'],
      'role':['Student','Developer','HR','Manager','Professor','Director','CEO','Team lead','QA analyst','Business Analyst','BI Developer','Software Engineer'],
      'Sports':['Soccer','Baseball','Basketball','Golf','Tennis','Swimming','Boxing'],
      'Vehicle':['Toyota','Hyundai','Cheverolet','Mercedez','Audi','Jeep','BMW','Honda','Scooter'],      
      'country':['USA']}

Asia ={'city':['Mumbai','Tokyo'],
      'school':['IITB','VJTI','UTA'],
      'employer':['TCS','Amazon','Caesars','Google','Microsoft'],
      'role':['Student','Developer','HR','Manager','Professor','Director','CEO','Team lead','QA analyst','Business Analyst','BI Developer','Software Engineer','Technician','Assitant Teacher','Consultant'],
      'Sports':['Soccer','Basketball','Golf','Tennis','Swimming','Boxing','Cricket','Table Tennis','Badminton','Kabaddi'],
      'Vehicle':['Toyota','Hyundai','Cheverolet','Mercedez','Audi','Jeep','BMW','Honda','Scooter','Tata','Maruti','Suzuki','Bajaj'],      
      'country':['India','Japan']}
      



edge_list =pd.read_csv('email-EU-core.txt',delimiter =' ', header =None)
print edge_list
for i in range(len(edge_list[0])):
    if edge_list[0][i] == edge_list[1][i]:
        continue
    else:
        H.add_edge(edge_list[0][i],edge_list[1][i])

attribute_list =pd.read_csv('email-Eu-core-department-labels.txt',delimiter =' ', header =None)
print len(attribute_list[0])
j=0
for i in H.nodes():
    H.node[i]['Department']=attribute_list[1][i]
    j=j+1
j=0

pos=nx.random_layout(H)
plt.figure()
nx.draw(H,node_size=800,pos=pos,node_color='y', with_labels=True)
plt.show()


clss ={}
x=0
count =0
for i in H.nodes():
    clss ={}
    for j,k in World.items():
        clss[j] =random.choice(k)
    H.node[i]['city'] =clss['city']
    H.node[i]['school']=clss['school']
    H.node[i]['role']=clss['role']
    H.node[i]['country']=clss['country']
    count =count+1

print 'node attributes:',H.nodes(data=True)
print 'number of nodes:', len(H.nodes()), 'number of edges:', len(H.edges())

k_core =min(H.degree(nx.k_core(H).nodes()),key=lambda item:item[1])
print 'k-core of graph:',k_core[1]

comm1_start_time = datetime.now()
comm1 = list(k_clique_communities(H,3))
print 'community k-clique:', len(comm1)
comm1_end_time = datetime.now()
print('Duration: {}'.format(comm1_end_time - comm1_start_time))


"""
comm2_start_time = datetime.now()
comm2 = list(girvan_newman(H))
print 'community girvan-newman:', len(comm2)
comm2_end_time = datetime.now()
print('Duration: {}'.format(comm2_end_time - comm2_start_time))
"""
"""
calculate probability of node attributes
"""
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

print 'prob-dict:', prob_dict
for key, value in prob_dict.items():
    if (float(float(value)/float(len(H.nodes()))) * 100) >= 20.0:
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

#print 'attribute node index:', atr_index

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
                prob_matrix[int(it1)-1, int(it2)-1] = prob_matrix[int(it1)-1, int(it2)-1] +1
            
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
    if val1 > 1.0:
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
                if jcd >= 40.0:
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
                      #  for it in list(diff):
                        #    if it in attr_class_dict.values():
                       #         c =c+1
                    
                            
           #     print 'node signature:', sig, l1
            if l1 ==0 and c==0 and jcd < 40.0:    
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
    node_count =attr_index_class[cl]['count']    
    if H.degree(item) >= k_core[1] and node_count >0:
        itm_lst =nx.algorithms.bfs_tree(H,item)
        while count <= node_count:
            for itm in itm_lst.nodes():
                if H.degree(itm) >=k_core[1]:
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
        comm1[cl] =nodelist
        pos =nx.spring_layout(H)
        k =nx.Graph(H.subgraph(nodelist))
        comm2[cl] =k.edges()
   #     print('query2:',cl,'is graph connected:',nx.is_connected(k))
      #  print('query2:',cl,'subgraph edges:',k.edges())
   # print('is it a partition:',nx.algorithms.community.is_partition(H,nodelist))
        plt.figure()
        nx.draw(k,node_size=800,pos=pos,node_color='y', with_labels=True)
        plt.show()
        count =0
        nodelist =[]
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))       

    
color =['r','g','y','m','c']
for cl,nod in comm1.items():
    x=random.choice(color)
    nx.draw(nx.Graph(H.subgraph(nod)),nx.spring_layout(H),with_labels=True,nodelist=nod,edge_list=H.edges(),node_size=800,node_color=x,edge_color=x)   
plt.show()
