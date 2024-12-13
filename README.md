# scratch2bash
The backend for a Bash terminal in Scratch!

![image](https://github.com/user-attachments/assets/494a3ee3-09fd-410d-a19b-dbfae547ccd0)

Known issues:
- Obviously, the repeated commands, which I could easily fix, but I don't have much time 😭
- Running an interative command softlocks the system (e.g. `sudo <command>`)

This is quite a big security risk, so only do this if you know that! It's more of a proof-of-concept than anything really 😂
## Setup
- Start by remixing the [bash2scratch](https://scratch.mit.edu/projects/1106466810/) project!

Now open your terminal in your favourite environment (this *could* work with Windows, but I haven't really tested nor been interested in it haha)
1. Install the requirements
   ```bash
   sudo apt update && sudo apt upgrade
   sudo apt install python3
   ```
   If you want this to run in the background, install screen too.
   ```bash
   sudo apt install screen
   ```
2. Copy and paste the following:
   ```bash
   mkdir bash2scratch
   cd bash2scratch
   curl -o main.py https://raw.githubusercontent.com/Fox595676/scratch2bash/refs/heads/main/main.py

   echo "Enter your session ID (this can be found by opening developer tools on Scratch etc, https://github.com/TimMcCool/scratchattach/wiki/Get-your-session-id):"
   read id
   echo "Enter your username:"
   read username
   echo "Enter your project ID (the numbers at the end of your remixed project):"
   read project_id

   sed -i "s/id = \"ID_HERE\"/id = \"$id\"/" main.py
   sed -i "s/user = \"Username\"/user = \"$username\"/" main.py
   sed -i "s/project = \"projectid\"/project = \"$project_id\"/" main.py
   
   python -m venv .
   source bin/activate
   python -m pip install -U scratchattach
   ```
3. Start the script (make sure you're in the same directory as you ran the install script in!):
   ```bash
   bin/python3 bash2scratch.py
   ```
4. If you want to have this running in the background, paste the following, and press Ctrl + A, then Ctrl + D to exit.
   ```bash
   screen -S bash2scratch bash -c "~/scratchAttach/bin/python3 ~/scratchAttach/bash2scratch.py"
   ```
5. If you want to reconnect, type
   ```bash
   screen -r bash2scratch
   ```
