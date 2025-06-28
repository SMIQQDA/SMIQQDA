import requests
import json
import os

#file = "datasetProfiles.json"
file = "filename.json"
f = open(file, 'r', encoding='utf-8')
contents = json.load(f)
f.close()

#path = "C:/Users/jtiago/Documents/Example corpora"
path = "path_name"
os.chdir(path=path)

path_in = "profiles_pic"
if path_in not in os.listdir():
    os.mkdir(path_in)
path2 = "all"
if path2 not in os.listdir(path=path_in):
    os.mkdir(path_in+'/'+path2)

k = 1
for c in contents:
    print(k)
    #directory per account
    username = c["username"]
    if username not in os.listdir(path=path_in):
        os.mkdir(path_in+ '/' + username)
    dir1 = path_in+'/'+username+"/"
    dir2 = path_in+'/'+path2+'/'

    pic = c["profilePicUrl"]

    name = username+"_pic.jpg"
    if name not in os.listdir(path=dir1):
        try:
            result = requests.get(pic)
            if result.status_code >= 300:
                raise ConnectionError
        except:
            print("Erreur en téléchargent la photo de "+ username + " à l'url "+ pic + "\n") 
        else:
            theFile = open(dir1+name, "wb")
            theFile.write(result.content)
            theFile.close()
            theFile2 = open(dir2+name, "wb")
            theFile2.write(result.content)
            theFile2.close()
            result.close()
    k += 1
