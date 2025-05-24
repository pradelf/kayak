import pandas as pd

proxy = pd.read_csv("Free_Proxy_List.csv")
proxy
proxy_list = [f"{row[0]}:{row[1]}" for row in zip(proxy["ip"],proxy["port"])]
proxy_list[:3]

textfile = open("listofproxies.txt", "w")
for element in proxy_list:
    textfile.write(element + "\n")
textfile.close()
