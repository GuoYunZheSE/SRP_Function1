import  os
import numpy
import re
from Identify import Identify
Instance=[]
path=r'G:\GITHUB\SRP_Function1\SRP_Function1\DataSet'
os.chdir(path)
print('Preloading...')
Count=1
File_Number=0
ROI_Result=[[]]
Hide_Result=[[]]

for filename in os.listdir():
    m_file=[filename.split('.')[0]]
    Instance.append(m_file)
    file=open(filename,'r')
    for eachline in file.readlines():
        if eachline[:4]=='lbl=':
            Temp_Data=re.split('lbl\=| str\=| end\=| hide\=',eachline[4:].strip('\n'))
           
        if eachline[:5]=='pos =':
            Temp_ROI=eachline[6:-3].split(';')
            Instance[File_Number].append(Identify(Temp_Data[0],Temp_Data[1],Temp_Data[2],Temp_Data[3],Temp_ROI))
    File_Number+=1

def Search(Comand):
    if Picture_Path!='exit':
        Name_Split=Picture_Path.split('_')
        Dataset_Name=Name_Split[0]
        Frame_Number=Name_Split[1]
        eachfile_number=0
        Count=0;

        for eachfile in Instance:
            if Dataset_Name in eachfile:
                for eachobject_number in range(1,len(Instance[eachfile_number])):
                    if int(Instance[eachfile_number][eachobject_number].Begin)<=int(Frame_Number) and int(Instance[eachfile_number][eachobject_number].End)>=int(Frame_Number):
                        Tem_ROI=Instance[eachfile_number][eachobject_number].Lable+Instance[eachfile_number][eachobject_number].ROI[int(Frame_Number)-int(Instance[eachfile_number][eachobject_number].Begin)]
                        ROI_Result.append(Tem_ROI)
                        Tem_Hide=Instance[eachfile_number][eachobject_number].Lable+Instance[eachfile_number][eachobject_number].Hide
                        Hide_Result.append(Tem_Hide)
            eachfile_number+=1


        print('ROI:')
        for i in range(1,len(ROI_Result)):
            print(ROI_Result[i])
        print('Hide:')
        for i in range(1,len(Hide_Result)):
            print(Hide_Result[i])
        print("Input 'exit' for exiting, you can still input Picture ID:")

while True:
    print('Please input the ID of the image: ')
    Picture_Path=input()
    if(Picture_Path!='exit'):
        Search(Picture_Path)
    else:
        break