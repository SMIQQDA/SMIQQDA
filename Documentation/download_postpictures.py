import requests
import json
from datetime import *
import os
import time

#file = "dataset_instagram-post-scraper_2023-02-18_13-21-52-192.json"
file = "filename.json"
f = open(file, 'r', encoding='utf-8')
contents = json.load(f)
f.close()

#path = "C:/Users/jtiago/Documents/Example corpora"
path = "path_name"
os.chdir(path=path)

if "comptes" not in os.listdir():
    os.mkdir("comptes")
if "jours" not in os.listdir():
    os.mkdir("jours")

#one line per post
k = 1
for c in contents:
    print(k)
    #directory per account
    username = c["ownerUsername"]
    if username not in os.listdir(path="comptes"):
        os.mkdir("comptes/"+username)
    dir1 = "comptes/"+username+"/"

    #directory per date
    timestamp = c["timestamp"]
    d = datetime.fromisoformat(timestamp[:-1])
    if str(d.year) not in os.listdir(path="jours"):
        os.mkdir("jours/"+str(d.year))
    if str(d.month) not in os.listdir(path="jours/"+str(d.year)):
        os.mkdir("jours/"+str(d.year)+"/"+str(d.month))
    if str(d.day) not in os.listdir(path="jours/"+str(d.year)+"/"+str(d.month)):
        os.mkdir("jours/"+str(d.year)+"/"+str(d.month)+"/"+str(d.day))
    dir2 = "jours/"+str(d.year)+"/"+str(d.month)+"/"+str(d.day)+"/"
    date = datetime.strftime(d, "%d-%m-%y_%H-%M-%S")
    
    jsonname = username+"_"+date+".json"
    
    if c["type"] == "Video":
        if jsonname in os.listdir(path=dir1):
            os.remove(path=dir1+jsonname)
            os.remove(path=dir2+jsonname)
        k=k+1
        continue
    if jsonname not in os.listdir(path=dir1):
        jsonfile1 = open(dir1+jsonname, "w")
        jsonfile2 = open(dir2+jsonname, "w")
        json.dump(c, jsonfile1)
        json.dump(c, jsonfile2)
        jsonfile1.close()
        jsonfile2.close()

    
    if c["type"] == "Image":
        name = username+"_"+date+"_1_1"+".jpg"
        link = c["displayUrl"]
        if name not in os.listdir(path=dir1):
            try:
                result = requests.get(link)
                if result.status_code >= 300:
                    raise ConnectionError
            except:
                print("Erreur en téléchargent le post de "+username + " à l'URL " + c["url"] + " au display URL " +link + " du "+timestamp+"\n")
            else:
                theFile = open(dir1+name, "wb")
                theFile.write(result.content)
                theFile.close()
                theFile2 = open(dir2+name, "wb")
                theFile2.write(result.content)
                theFile2.close()
                result.close()


    #2 to 10 images
    elif c["type"] == "Sidecar":
        for i in range(len(c["images"])):
            link = c["images"][i]
            name = username+"_"+date+"_"+str(i+1)+"_"+str(len(c["images"]))+".jpg"
            if name not in os.listdir(path=dir1):
                try:
                    result = requests.get(link)
                    if result.status_code >= 300:
                        raise ConnectionError
                except:
                    print("Erreur en téléchargeant le post de "+ username + " à l'URL " + c["url"] + " au display URL " + link + " du " + timestamp + " image "+str(i)+"\n")
                else:
                    theFile = open(dir1+name, "wb")
                    theFile.write(result.content)
                    theFile.close()
                    theFile2 = open(dir2+name, "wb")
                    theFile2.write(result.content)
                    theFile2.close()
                    result.close()
    k+=1
