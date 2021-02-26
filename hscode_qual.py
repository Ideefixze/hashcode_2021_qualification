import sys
import math
import random

class Street():

    def __init__(self, L, name, from_node, to_node):
        self.L = L
        self.name = name
        self.from_node = from_node
        self.to_node = to_node

class Node():

    def __init__(self, id):
        self.id = id
        self.incoming = dict()
        self.schedule = dict()

    def add_incoming_street(self, street):
        self.incoming[street.name] = street
        self.schedule[street.name] = 1 #remember to ignore 0 later in solution

    def prune_unused_street(self,street_name):
        if(self.schedule.get(street_name,False)):
            self.schedule[street_name] = 0 

    def change_schedule(self, street_name, val):
        if(self.schedule.get(street_name,False)):
            self.schedule[street_name] = val

    def get_schedule(self):
        non_zero = {(k,v) for (k,v) in self.schedule.items() if v!=0}
        if (len(self.schedule)==0 or len(non_zero)==0):
            return None
        else:
            sch = str(self.id)+"\n"+str(len(non_zero))+"\n"
            for k,v in non_zero: #k - street, v - time
                sch = sch + f"{k} {v}\n"
        
        return sch[:len(sch)-1]

def main():
    TIME, I, ST, C, SC = input().split()
    TIME = int(TIME)
    I = int(I)
    ST = int(ST)
    C = int(C)
    SC = int(SC)

    nodes = list()
    for i in range(0,I):
        nodes.append(Node(i))

    streets = list()
    streets_dict = dict()
    for i in range(0,ST):
        a,b,name,l = input().split()
        s = Street(int(l),name,nodes[int(a)],nodes[int(b)])
        nodes[int(b)].add_incoming_street(s)
        streets.append(s)
        streets_dict[name] = s

    paths = list()
    for i in range(0,C):
        start,*path = input().split()
        paths.append(path)

    #unused streets

    all_streets = set(x.name for x in streets)

    all_streets_in_paths = set()
    for i in paths:
        for j in i:
            all_streets_in_paths.add(j)

    pruned_streets = all_streets.difference(all_streets_in_paths)

    for i in pruned_streets:
        for j in nodes:
            j.prune_unused_street(i)


    #prio
    all_streets_uses = dict()

    for i in paths:
        streets_in_paths_L = sum(streets_dict[x].L for x in i)
        for j in i:
            #streets_visited_L = 0
            #for a in i:
               # streets_visited_L = streets_dict[a].L + streets_visited_L 

            if(all_streets_uses.get(j,-1)==-1):
                all_streets_uses[j]=1.0/streets_in_paths_L
            else:
                all_streets_uses[j]=all_streets_uses[j]+1.0/streets_in_paths_L
    
    avg_use = (sum(v for (k,v) in all_streets_uses.items()))/(len(all_streets_uses))

    for k,v in all_streets_uses.items():
        for i in nodes:
            i.change_schedule(k,int(v/avg_use)+1)
    

    #print schedules
    schedules = list()
    for i in range(0,I):
        s = nodes[i].get_schedule()
        if(s!=None):
            schedules.append(s)
        
    print(len(schedules))
    for i in schedules:
        print(i)

main()