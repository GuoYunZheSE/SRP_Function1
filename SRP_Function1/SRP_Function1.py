import  os
import numpy
import re
from Identify import Identify
Instance=[]
path=r'c:\users\user\documents\visual studio 2017\Projects\SRP_Function1\SRP_Function1\DataSet'
os.chdir(path)
print('Please input the frame of the image: ')
ID=input()
for filename in os.listdir():
    Instance.append(filename)
    file=open(filename,'r')
    for eachline in file.readlines():
        if eachline[:4]=='lbl=':
            Temp_Data=re.split('lbl\=| str\=| end\=| hide\=',eachline)
            eachline+=1
        if eachline[:5]=='pos =':
            Temp_ROI=eachline[6:-3].split(';')
        Instance[Instance.index(filename)].append(Identify(Temp_Data[1],Temp_Data[2],Temp_Data[3],Temp_Data[4],Temp_ROI))
    #process each txt