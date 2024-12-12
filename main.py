import scratchattach as sa
import requests
import json
from random import randint
import subprocess
from time import sleep

d_s = ["00"]
a_s = [" "]

d_A = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26"]
a_A = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
#print(len(d_A),len(a_A))

d_a = ["27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52"]
a_a = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
#print(len(d_a),len(a_a))

d_n = ["53","54","55","56","57","58","59","60","61","62"]
a_n = ["0","1","2","3","4","5","6","7","8","9"]
#print(len(d_n),len(a_n))
6364656667686970717273747576777879808182838485868788899091929394
d_special = ["63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94"]
a_special = [".",",","\"","'","?","!","@","_","*","#","$","%","&","(",")","+","-","/",":",";","<","=",">","[","\\","]","^","{","|","}","~","\n"]
#print(len(d_special),len(a_special))
dChars = d_s + d_A + d_a + d_n + d_special
aChars = a_s + a_A + a_a + a_n + a_special

print(len(dChars))
print(len(aChars))

user = "USERNAMEHERE"
userid = "IDHERE"
projectid = "IDHERE"
session = sa.login_by_id(id, username=user)

cloud = session.connect_cloud(projectid)
print("Connected!")


# From Python to Scratch -- to Decimal
def convert(text):
    dec = []
    for c in range(0,len(text)):
        try:
            dec.append(dChars[aChars.index(text[c])])
        except:
            print("Error processing ",text[c])
    return("".join(dec)[0:129])

# From Scratch to Python -- to Text
def convert_back(text):
    cha = []
    for c in range(0,int(len(text)),2):
        cha.append((aChars[dChars.index(f"{text[c]}{text[c+1]}")]))
    return("".join(cha))

def grabData(amount):
    cont = 0
    while cont < 10:
        data = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={projectid}&limit={amount}&offset=0")
        if data.status_code == 200:
            data = data.text
            data_json = json.loads(data)
            return data_json
        else:
            print(f"Error {data.status_code}, trying again.")
            cont += 1
            sleep(1)
    print(f"Error {data.status_code}, resorting to placeholder after {cont} attempts.")
    grabData(amount)
    exit
    # I'm aware how horendous this part is :sob:
    placeholder = '[{"user":"null","verb":"null","name":"null","value":"0","timestamp":0}]'
    data_json = json.loads(placeholder)
    return data_json

data_json = grabData(10)

# Make this read from the JSON!
pwd = "/home/avagoosa/"

# Don't. Even.
oldcommand = 999
command = 999

for i in range(0, len(data_json)):
    if data_json[i]["verb"] == "set_var" and data_json[i]["name"] == "☁ Output":
        oldcommand = data_json[i]["value"]
        command = oldcommand
        break

if oldcommand == 999:
    print("No previous commands found.")
else:
    print("Last command:\n", convert_back(oldcommand))

print("Searching for a new command...")

while True:
    found = False
    data_json = grabData(10)
#   print("Refreshed data...")
    for i in range(0, len(data_json)):
        if data_json[i]["verb"] == "set_var" and data_json[i]["name"] == "☁ Output":
            command = data_json[i]["value"]
            
            if command == oldcommand:
                found = False
                break
            else:
                found = True
                print("Found new command from :", data_json[i]["user"])
                propercommand = convert_back(data_json[i]["value"])
                # pwd = data_json[i]["verb"] == "set_var" and data_json[i]["name"] == "☁ PWD"
                print(propercommand)
                break

    if command != oldcommand:
        oldcommand = command
        ran = f" {randint(100,999)}" # So it can be sent again
        try:
            input = subprocess.check_output(f"{propercommand};echo \n$PWD", cwd=pwd, shell=True, stderr=subprocess.STDOUT)
            input = input.decode("utf-8").strip()
            pwd = str(input.split("\n")[-1])
            if input.count("\n") > 0:
                input = '\n'.join(input.split("\n")[:-1])
            else:
                input = "No output."
            cloudpwd = convert(pwd)
        except subprocess.CalledProcessError as error:
            input = error.output.decode("utf-8") if error.output else str(error)
        print(input)
        print(f"pwd: {pwd}")
        input = convert(input)
        cont = 0
        while cont < 5:
            try:
                    cloud.set_var("PWD", cloudpwd)
                    sleep(0.1)
                    cloud.set_var("Input", input)
            except:
                print("Failed to set cloud variables, trying again.")
            cont += 1
            sleep(0.5)
        if cont == 5:
            print("Failed to set cloud variables, giving up.")
    sleep(2)
