import  os
path=r'c:\users\user\documents\visual studio 2017\Projects\SRP_Function1\SRP_Function1\DataSet'
os.chdir(path)
print('Please input the frame of the image: ')
ID=input()
for filename in os.listdir():
    file=open(filename,'r')
    #process each txt

