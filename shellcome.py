# import libraries
import datetime
import os
import random

# Variables
happening_today = []
usenamefor = []
do_normal = False

# Fallback variables incase someone made a really bad config file
birthday = "00"
birthmonth = "00"
use_rng = False
normal = "#"

# Real subprograms:
def checkdate(pEvent, pDate, pBirthday):
    if pEvent == "newyear":
        if pDate == "0101":    # 1st of January, not 5.
            return True
    if pEvent == "birthday":
        if pDate == pBirthday:
            return True
    if pEvent == "valentines":
        if pDate == "1402":
            return True
    if pEvent == "stpatricks":
        if pDate == "1703":
            return True
    if pEvent == "halloween":
        if pDate == "3110":
            return True
# Mental illness subprograms (print the ascii)
def show_ascii(pEvent, pUsername):
    if pEvent == "birthday":
        print("Happy Birthday" + pUsername)
        print("""          ,     
     ,    |    ,
   __|____|____|__
   |~ ~ ~ ~ ~ ~ ~|
   | ~ ~ ~ ~ ~ ~ |
___|_____________|___
|\\/\\/\\/\\/\\/\\/\\/\\/\\/\\|
|~ ~ ~ ~ ~ ~ ~ ~ ~ ~|
|___________________|""")

    if pEvent == "newyear":
        print("Happy New Year" + pUsername)
        print("""          :                      . 
       '.\\'/.'      ,  '  ,    '.:,'    
       -= o =-       \\ | /   -- -+- -- 
  *''* .'/.\\'.    - == @ == -  ,':'.     .      
 *_\\/_*   :  .''.    / | \\       '    .'.:.'.     
 * /\\ *     :_\\/_:  '  ,  '     *     -=:o:=-    
  *..*      : /\\ :             *      '.':'.'         
             '..'            *           '    """)
    
    if pEvent == "valentines":
        print("Happy Valentine's Day" + pUsername)
        print(""",d88b.d88b,     ,d88b.d88b,     ,d88b.d88b,     ,d88b.d88b,     ,d88b.d88b,
88888888888     88888888888     88888888888     88888888888     88888888888
`Y8888888Y'     `Y8888888Y'     `Y8888888Y'     `Y8888888Y'     `Y8888888Y'
  `Y888Y'         `Y888Y'         `Y888Y'         `Y888Y'         `Y888Y'
    `Y'             `Y'             `Y'             `Y'             `Y'     """)
    if pEvent == "stpatricks":
        print("Happy St. Patrick's Day!" + pUsername)
        print("""
     .-. .-.
    (   Y   )
 .-.:.  |  ,;.-.
(     `;|:`     )
(    ,' ╎ '.    )
 '--'   ╎   '--'
        ;.    ,
         ';.-' """)

    if pEvent == "halloween":
        print("Happy Halloween!") 
        # No, I am not putting an apostrophe between the E's.
        print("""      __)"[__    
  .-'\\-"  "-/`'-.
 /  (o) __ (o)   \\
]      /__\\       L
|                 |
J   (\\/\\/\\/\\/)    [
 \\   \\/\\/\\/\\/    /
  "-._      _,-"
      \"\"\"\"\"\"    """)


# Constants
DEFAULT_CONFIG = """# Config for Shellcome. Ignores lines that begin with "#".
# If you mess up badly look at the code or delete this file to regenerate it.
# Blank lines are read but it's not like they do anything to begin with

# Set your birthday. 
# Can be whatever but obviously won't work if you set it to something stupid.
# Example: 
# birthday = 31
# birthmonth = 07

birthday = 06
birthmonth = 09

# Set your name, won't appear if set to #.
# Example:
# name = John Doe
# OR
# name = #

name = #

# Show your name on each holiday, T or F, defaults to F.
# This is handled separately on custom modules.
name_birthday = T
name_newyear = F

# Set modules. these are the special events that appear on certain days.
# They are listed in priority, so if 2 events occur on the same day, the
# first one in the list will be used (RNG can also be set elsewhere)
# custom modules begin with "custom_" and then the filename. e.g. custom_anniversary
# Separate each module with a comma and space (", ")
# Example:
# modules = birthday, valentines
modules = birthday, newyear, halloween

# If 2 events occur on the same date, choose randomly, or highest
# priority to display (T/F), derfaults to F if not set
use_rng = F

# Choose the command(s) to run if nothing is happening that day
# Separate each module with a comma and space (", ")
# use a hash to disable
normal = #
"""

# Work out time and put it in actual useful format (might do this better with one string in the future)
full_date = datetime.datetime.now()
day = full_date.strftime("%d")
month = full_date.strftime("%m")

# config home detection
if "XDG_CONFIG_HOME" in os.environ:
    confighome = os.environ["XDG_CONFIG_HOME"]
else:
    confighome = os.path.join(os.environ["HOME"], ".config")
configpath = os.path.join(confighome, "shellcome")
# create path if not already present
if not os.path.exists(configpath):
    os.makedirs(configpath)

configfile = os.path.join(configpath, "config")
try:
    open(configfile, "r")
except:
    file = open(configfile, "w")
    file.write(DEFAULT_CONFIG)
    file.close()

with open(configfile, "r") as file:
    for line in file:
        # Search config file for stuff we want
        if not line.startswith("#"):   # ignore comments because i want to
            if line.startswith("birthday = "):
                birthday = str(line[11:-1].strip("\n"))

            elif line.startswith("birthmonth = "):
                birthmonth = str(line[13:-1].strip("\n"))

            elif line.startswith("name = "):
                username = line[7:-1].strip("\n")

            elif line.startswith("modules = "):
                modules = line[10:-1].strip("\n").split(", ")

            elif line.startswith("normal = "):
                normal = line[9:-1].strip("\n")

            elif line.startswith("name_"):
                if line[-2] == "T":
                    usenamefor.append(line[5:-5])

# print(modules)                       # DEBUG LINE
#print(birthday, birthmonth, username) # DEBUG LINE  

#day = "31"
#month = "10"
# username = "John Doe" # DEBUG LINE to test if name shows up correctly if set to a hash
# Remove username if it is a hash
if username == "#":
    username = "!"
# Add punctuatiom so i don't have to every time
else:
    username = ", " + username + "!"


for event in modules:
    if checkdate(event, day + month, birthday + birthmonth) == True:
        happening_today.append(event)
    else:
        # print("debug")  # DEBUG LINE (surprisingly)
        pass

if use_rng == "F":
    try:
        chosen_event = happening_today[1]
    except:
        do_normal = True
    else:
        chosen_event = happening_today[1]
elif not happening_today == []:
    list_length = len(happening_today) - 1
    chosen_event = happening_today[random.randint(0, list_length)]
else:
    do_normal = True

if do_normal == False:
    if not chosen_event in usenamefor:
        username = "!"
    show_ascii(chosen_event, username)
else:
    if normal == "#":
        pass
    else:
        os.system(normal)