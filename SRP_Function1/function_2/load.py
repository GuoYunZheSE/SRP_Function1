import  os
import numpy
import re
import time
from Identify import Identify
def load(instance_name,fullpath):
    t=time.time()
    path=fullpath
    os.chdir(path)
    print('Preloading...')
    File_Number=0
    for filename in os.listdir():
        os.chdir(os.path.join(path,filename))   
        for txtname in os.listdir():
            m_file=[txtname.split('.')[0]]
            m_file.append(filename)
            instance_name.append(m_file)
            file=open(txtname,'r')
            for eachline in file.readlines():
                if eachline[:4]=='lbl=':
                    Temp_Data=re.split('lbl\=| str\=| end\=| hide\=',eachline[4:].strip('\n'))
           
                if eachline[:5]=='pos =':
                    Temp=eachline[6:-3].strip(';').split('; ')
                    Temp_ROI=[]
                    if len(Temp)>1:
                        for cordinate in range(len(Temp)):
                            Temp_Cordinate=Temp[cordinate].split(' ')
                            Temp_ROI.append([float(Temp_Cordinate[0]),float(Temp_Cordinate[1]),float(Temp_Cordinate[2]),float(Temp_Cordinate[3])])
                    else:
                        Temp_ROI.append('None')
                    instance_name[File_Number].append(Identify(Temp_Data[0],Temp_Data[1],Temp_Data[2],Temp_Data[3],Temp_ROI))
            File_Number+=1
    print('Loading Complete time used:',time.time()-t)
    return  instance_name
