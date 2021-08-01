from function import *

apiURL= getAPI(input("please input your space url or uid:\n"))
bvList = getBV(apiURL)
print(bvList)