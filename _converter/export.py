from os import listdir, remove
from shutil import rmtree
from time import sleep

for fname in ["node_modules", "__pycache__", "output", "final_output", "tmp"]:
    try:
        rmtree("{}/".format(fname))
    except:
        pass

try:
    in_folder = "input/"
    for f in listdir(in_folder):
        remove("{}{}".format(in_folder, f))
    f = open(in_folder+"placeholder", 'w')
    f.write("placeholder")
    f.close()
except:
    pass

print("Done")
sleep(1)