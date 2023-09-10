import pandas as pd
import csv
file_name=input()
data=[]
#The 3 parameters below should be changed based on the experiment and excel format.
TOTAL_DAYS=50
POPULATION=9
start_index=1 #The index at which actual data starts.
sheet=pd.read_csv(file_name)
for i in range(0,54,6):
    
    rob_count=sheet.columns[i]
    rob_result=sheet.columns[i+1]
    trade_count=sheet.columns[i+2]
    trade_result=sheet.columns[i+3]
    master=sheet.columns[i+4]
    farm_count=sheet.columns[i+5]
    day_of_obedience=1
    for cell in master:
        if cell!=-1:
            break
        day_of_obedience+=1
    #STATS FOR ROBBING
    pre_rob_count=rob_count[day_of_obedience-2+start_index]#It is unclear whether on the day of obedience, the person robbed in a status of obedience or as a free man, so right now this data point is discarded.
    post_rob_count=rob_count[TOTAL_DAYS-1+start_index]-pre_rob_count-(rob_count[day_of_obedience-1+start_index]-rob_count[day_of_obedience-2+start_index])
    
    pre_rebel=rob_count[day_of_obedience-2+start_index]
    post_rebel=rob_count[TOTAL_DAYS-1+start_index]-pre_rebel-(rob_count[day_of_obedience-1+start_index]-rob_result[day_of_obedience-2+start_index])
    
    #STATS FOR FARM
    pre_farm_count=farm_count[day_of_obedience-2+start_index]
    post_farm_count=farm_count[TOTAL_DAYS-1+start_index]-pre_farm_count-(rob_count[day_of_obedience-1+start_index]-farm_count[day_of_obedience-2+start_index])
    
    #STATS FOR TRADE
    pre_trade_count=rob_count[day_of_obedience-2+start_index]
    post_trade_count=rob_count[TOTAL_DAYS-1+start_index]-pre_trade_count-(rob_count[day_of_obedience-1+start_index]-trade_count[day_of_obedience-2+start_index])
    
    pre_accept=trade_count[day_of_obedience-2+start_index]
    post_accept=trade_count[TOTAL_DAYS-1+start_index]-pre_accept-(rob_count[day_of_obedience-1+start_index]-trade_result[day_of_obedience-2+start_index])
    
    if day_of_obedience>TOTAL_DAYS-2:master=True
    else:master=False
    pre_days=day_of_obedience-1
    post_days=1 if master else TOTAL_DAYS-day_of_obedience-1
    data.append((pre_rob_count/(pre_days),post_rob_count/(post_days),pre_rebel/pre_rob_count, post_rebel/post_rob_count, pre_farm_count/(pre_days),post_farm_count/post_days,pre_trade_count/pre_days,post_trade_count/post_days,pre_accept/pre_trade_count,post_accept/post_trade_count))
print(f'Pre-obedience rob rate:{sum([x[0] for x in data])/POPULATION}, post-obedience rob rate:{sum([x[1] for x in data])/POPULATION}.')
print(f'Pre-obedience rob obey rate:{sum([x[2] for x in data])/POPULATION}, post_obedience rob obey rate:{[sum([x[3] for x in data])/POPULATION]}.')
print(f'Pre-obedience farm rate:{sum([x[4] for x in data])/POPULATION}, post-obedience farm rate:{sum([x[5] for x in data])/POPULATION}.')
print(f'Pre-obedience trade rate:{sum([x[6] for x in data])/POPULATION}, post-obedience trade rate:{sum([x[7] for x in data])/POPULATION}.')
print(f'Pre-obedience trade acceptance rate:{sum([x[8] for x in data])/POPULATION}, post-obedience trade acceptance rate:{sum([x[9] for x in data])/POPULATION}')
    