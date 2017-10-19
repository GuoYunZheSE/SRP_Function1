from load import *
from search import *
result=[]
path=r'G:\SRP_Function1\SRP_Function1\DataSet'
result=load(result,path)
print(search_frame('set00','V000',751,result))
print(search_video('set00','V000',result))
print(search_dataset('set00',result))
print(search_all_multiprocess(result,4))
