'''
Created on Feb 9, 2016

@author: akshat
'''

from itertools import product
from functools import reduce

# Initialize variables
init_barrels = 100000.0
years = 3
prices = [20,30]

#List of tuples containing possible options of oil percentages that can be drilled in a year and associated costs
options = [(0.0,0),(0.2,130000),(0.36,300000)]


# Create all possible states of number of barrels left at start of each year
barrels= set()
for year in range(years,0,-1):
    for option in product(next(zip(*options)), repeat = year-1):
        if len(option) == 0:
            barrels.add((1,init_barrels))
        elif len(option) == 1 :
            barrels.add((2,(1-option[0])*init_barrels))
        else:
            barrels.add((year,round(reduce(lambda x, y: (1-x)*(1-y), option)*init_barrels,1)))

# Tuple containing possible number of barrels at start of each year and the year
print(barrels)
#{(3, 100000.0), (3, 80000.0), (3, 64000.0), (3, 51200.0), (3, 40960.0), (2, 100000.0), (2, 80000.0), (2, 64000.0), (1, 100000.0)}

# Cartesian product of barrels and prices, gives all possible states where state includes barrels,price and time 
states = set(product(barrels,prices))
print(states)
#{((1, 100000.0), 20), ((2, 100000.0), 30), ((2, 80000.0), 30), ((2, 100000.0), 20), ((3, 80000.0), 20), ((3, 64000.0), 20), ((3, 100000.0), 30), ((3, 80000.0), 30), ((3, 64000.0), 30), ((3, 100000.0), 20), ((3, 51200.0), 20), ((3, 51200.0), 30), ((3, 40960.0), 20), ((3, 40960.0), 30), ((2, 64000.0), 20), ((2, 80000.0), 20), ((2, 64000.0), 30), ((1, 100000.0), 30)}


# Dictionary containing maximum profits possible in a given state in the third year
states_dict = {}
for state in states:
    if(state[0][0]==years):
        states_dict[state] = max(0,max([option[0]*state[0][1]*state[1]-option[1] for option in options]))
    
    
print(states_dict)
#{((3, 40960.0), 30): 142367.99999999994, ((3, 100000.0), 30): 780000.0, ((3, 40960.0), 20): 33840.0, ((3, 100000.0), 20): 420000.0, ((3, 80000.0), 30): 564000.0, ((3, 64000.0), 30): 391200.0, ((3, 51200.0), 30): 252960.0, ((3, 80000.0), 20): 276000.0, ((3, 51200.0), 20): 74800.0, ((3, 64000.0), 20): 160800.0}

# Dynamic Programming: Update maximum profit for state at time t based on possible transition states at time t+1
for t in range(years-1,0,-1):
    for state in states:
        if state[0][0]==t:
            possible_next_barrels_and_profit = [(state[0][1]*(1-option[0]),option[0]*state[0][1]*state[1]-option[1]) for option in options]
            max_profit = 0
            for val in possible_next_barrels_and_profit:
                max_profit = max(max_profit,val[1]+(1/2)*(states_dict[((t+1,val[0]),prices[0])]+states_dict[((t+1,val[0]),prices[1])]))
            states_dict[state] = max_profit

print(states_dict)           
# Final States: {((2, 64000.0), 30): 479304.0, ((2, 80000.0), 20): 466000.0, ((3, 100000.0), 30): 780000.0, ((3, 80000.0), 20): 276000.0, ((3, 51200.0), 30): 252960.0, ((2, 100000.0), 30): 1056000.0, ((3, 64000.0), 20): 160800.0, ((2, 100000.0), 20): 696000.0, ((3, 40960.0), 20): 33840.0, ((2, 80000.0), 30): 727880.0, ((3, 40960.0), 30): 142367.99999999994, ((1, 100000.0), 30): 1164592.0, ((2, 64000.0), 20): 289880.0, ((3, 80000.0), 30): 564000.0, ((3, 64000.0), 30): 391200.0, ((3, 100000.0), 20): 420000.0, ((3, 51200.0), 20): 74800.0, ((1, 100000.0), 20): 876000.0}
