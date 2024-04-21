import pandas as pd
import numpy as np
import random
from datetime import datetime,timedelta

NR_OF_COMPLAINTS=20

complaintTypes=["Missing Product","Damaged Product","Wrong product","Late","Other"]


myTable=pd.read_csv("./data/Berlin_crimes.csv")


keepColumns=["Year","District","Code","Location","Theft","Local"]

keepTable=myTable[keepColumns]

complaintLocationToTable=keepTable["Code"].sample(n=NR_OF_COMPLAINTS).tolist()
complaintTypeToTable=[]

for i in range(0,NR_OF_COMPLAINTS):
    complaintTypeToTable.append(complaintTypes[random.randrange(0,len(complaintTypes))])


endTable=pd.DataFrame(zip(complaintLocationToTable,complaintTypeToTable),columns=["Code","Complaint"])

#print(endTable)

startTime=datetime.strptime("00:00:00","%H:%M:%S")
randomTimes= [(startTime+timedelta(seconds=random.randint(0, 24 * 60 * 60 - 1))).strftime("%H:%M:%S") for i in range(0,NR_OF_COMPLAINTS)]

endTable["Time"]=randomTimes

endTable.to_csv("./data/complaints.csv",index=False)