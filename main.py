import csv
from os import listdir, mkdir, rename, remove
from shutil import rmtree
from os.path import exists, join
from subprocess import call
from time import sleep
from _converter.orderer import orderer, get_tag

def exception(msg):
    print("ERROR")
    print(msg)
    sleep(3)
    raise Exception()

# installs node modules if required, creates output path. 
def init(out_path, user_path):
    if not exists("_converter/node_modules"):
        call("_converter\init.bat")
    try:
        mkdir(out_path)
    except:
        pass
    try:
        remove(user_path+"placeholder")
    except:
        pass
    try:
        rmtree(tmp)
    except:
        pass

# generate formatted string from q details
def parse_q(q, correct_raw, ans):
    if ans!=[]:
        mcq = True
        correct = []
        if correct_raw=="":
            correct_raw = "N/A"
        elif correct_raw=="0":
            correct_raw="ERROR"
        else:
            correct = correct_raw.split(",")
            try:
                correct = [int(q_i) for q_i in correct]
            except:
                exception("Correct column format is not valid: {}".format(correct_raw))
    else:
        mcq=False
        ans = [correct_raw]
        correct=[0]
    
    q = q.replace("```", "\n```").replace("\n\n```", "\n```")
    output = "\n"+q
    if mcq:
        for i, a in enumerate(ans):
            bold = "  "
            if i+1 in correct:
                bold = "**"
            output += "\n{}. {}{}{}".format(i+1, bold, a, bold)
        output+="\n"
        
    output += "\nCorrect: {}".format(correct_raw)

    return output

# joins all csvs in dirname to one file at the path/name outname 
def join(dirname, outname):
    # join csvs
    fnames = listdir(dirname)
    if len(fnames)==0:
        exception("No input files provided.")
    output = []
    first_file = True
    for fname in fnames:
        first_line = True
        f = open(dirname+fname, "r")
        for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
            if first_line and (not first_file):
                first_line = False
                continue
            output.append(line)
        if first_file:
            first_file = False
        
    with open(outname, 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(output)

def go(user_path, out_path, in_path):
    user_files = listdir(user_path)
    if len(user_files)!=1:
        exception("Something's gone wrong. Why are there {} input files?.".format(len(user_files)))
    user_fname = user_files[0]

    # create input csv for program
    joined_fname = out_path+"[joined] "+ user_fname
    call("_converter\convert.bat")
    join(in_path, joined_fname)

    orderer(joined_fname) # can be commented out

    # make data
    f = open(joined_fname, "r")
    first = True
    i = 0
    output = "## Questions from {}".format(user_fname)
    for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
        if first:
            first=False
            continue

        tag = get_tag(line[1])
        if tag==None:
            i+=1
            tag="Untagged Question {}".format(i)
        else:
            line[1] = line[1].replace(tag, "")

        i+=1
        output += "\n### {}".format(pretty_tag(tag))
        output += parse_q(line[1], line[2], line[3:])
        output += "\n"
    output = output.replace('\u2713', '') # remove rogue trailing character, strip() doesn't work
    f.close()

    f = open(out_path+"[parsed] " + user_fname.replace(".csv", ".md"), "w")
    f.write(output)
    f.close()


def pretty_tag(tag):
    return tag.replace("F", "Folder ").replace("S", " Subfolder ").replace("Q", " Question ")


# constants
base = "_converter/"
tmp = base+"tmp/"
user_path = base+"input/" # user input
in_path = base+"output/" # program input
out_path = base+"final_output/" # program output

# main 

init(out_path, user_path)
rename(user_path, tmp)
mkdir(user_path)
for fname in listdir(tmp):
    rename(tmp+fname, user_path+fname)
    go(user_path, out_path, in_path)
    rename(user_path+fname, tmp+fname)

# tidying up
assert len(listdir(user_path))==0
rmtree(user_path)
rename(tmp, user_path)

sleep(1)