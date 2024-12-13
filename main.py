import scratchattach as sa
import subprocess
from getpass import getuser

# ----------------------------------- #

id = "ID_HERE"
user = "Username"
project = "projectid"

session = sa.login_by_id(id, username=user) # Log in
cloud = session.connect_cloud(project)      # Log in + Connect
events = cloud.events(use_logs=True)        # Log in + Connect + Update

#print the name of the user logged in
compuser = getuser()
print(compuser)

# ----------------------------------- #

d_space = ["00"]
a_space = [" "]

d_caps = [
            "01","02","03","04", "05","06","07","08","09",
            "10","11","12","13", "14","15","16","17","18",
            "19","20","21","22", "23","24","25","26"
       ]
a_caps = [
            "A","B","C","D","E", "F","G","H","I","J","K",
            "L","M","N","O","P", "Q","R","S","T","U","V",
            "W","X","Y","Z"
        ]

d_lower = [
            "27","28","29","30", "31","32","33","34","35",
            "36","37","38","39", "40","41","42","43","44",
            "45","46","47","48", "49","50","51","52"
            ]
a_lower = [
            "a","b","c","d","e", "f","g","h","i","j","k",
            "l","m","n","o","p", "q","r","s","t","u","v",
            "w","x","y","z"
            ]

d_numbers = [
            "53","54","55","56", "57","58","59","60","61",
            "62"
            ]
a_numbers = [
            "0","1","2","3","4", "5","6","7","8","9"
            ]

d_special = [
            "63","64","65","66", "67","68","69","70","71",
            "72","73","74","75", "76","77","78","79","80",
            "81","82","83","84", "85","86","87","88","89",
            "90","91","92","93", "94"
            ]
a_special = [
            ".",",","\"","'","?","!","@","_","*","#","$",
            "%","&","(",")","+","-","/",":",";","<","=",
            ">","[","\\","]","^","{","|","}","~","\n"
            ]

dChars = d_space + d_caps + d_lower + d_numbers + d_special
aChars = a_space + a_caps + a_lower + a_numbers + a_special

print(len(dChars))
print(len(aChars))

# ----------------------------------- #

def convert(text): # From Python to Scratch -- to Decimal
    dec = []
    for c in range(0,len(text)):
        try:
            dec.append(dChars[aChars.index(text[c])])
        except:
            print(f"Error reading ", c)
    return("".join(dec)[0:254]) # Crop for Scratch

def convert_back(text): # From Scratch to Python -- to Text
    cha = []
    for c in range(0,int(len(text)),2):
        cha.append((aChars[dChars.index(f"{text[c]}{text[c+1]}")]))
    return("".join(cha))

print("Searching for a new command...")

# ----------------------------------- #

running = False # So setting variables doesn't trigger and create an infinite loop
pwd = f"/home/{compuser}"

@events.event
def on_set(activity):
    global running
    global pwd
    global compuser

    if running == False and activity.username != None:

        if activity.var == "PWD":
            running = True ###
            # pwd = convert_back(activity.value)
            pwd = pwd.replace("~", f"/home/{compuser}")
            cloudpwd = convert(pwd.replace(f"/home/{compuser}", "~"))
            cloud.set_var("PWD", cloudpwd)
            running = False ###

        # ------------------------------- #

        if activity.var == "Output": # If the event is a command
            running = True ###
            command = activity.value
            oldresult = cloud.get_var("Input")

            print("Found command from: ", activity.username) # Print the command the Scratcher has input
            propercommand = convert_back(activity.value)
            print(propercommand)

            try:
                input = subprocess.check_output(f"{propercommand};echo;echo $PWD", cwd=pwd, shell=True, stderr=subprocess.STDOUT)
                input = input.decode("utf-8").strip() # To be sent to Scratch

                pwd = str(input.split("\n")[-1])

                if input.count("\n") > 0:
                    input = '\n'.join(input.split("\n")[:-1])
                else:
                    input = ""

            except subprocess.CalledProcessError as error:
                input = error.output.decode("utf-8") if error.output else str(error)
            
            # So it can be set independently and display a tilde for the home directory
            cloudpwd = convert(pwd.replace(f"/home/{compuser}", "~"))

            print(input)
            print(f"pwd: {pwd}")

            input = convert(input)

            if input == oldresult:
                print("Both results are the same.")
                if not input.startswith("99"): # So Scratch can see the update
                    input = "99"+input
                else:
                    input = input[2:]

            cloud.set_var("PWD", cloudpwd)
            cloud.set_var("Input", input)
            running = False ###
    else:
        print(f"Variable {activity.var} updated by {activity.username}, but busy")

events.start()
