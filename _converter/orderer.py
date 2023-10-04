import csv
import re

## main
def orderer(fname):
    to_write = [get_header(fname)] + order_lines(get_headerless_lines(fname))
    write_csv(to_write, fname)
 

########

# returns -1 if no tag found, or if tag is None
def get_value(tag, t, keys=["F", "S", "Q"]):
    if tag==None:
        return -1
    t = t.upper()
    if not t in keys:
        return 0
    full = re.findall("{}[0-9]*".format(t), tag)
    if len(full)==0:
        return -1
    if len(full)!=1:
        raise Exception("Tag ({}) formatted incorrectly".format(tag))
    return int(full[0][1:])


def get_tag(title):
    tag = re.findall("F[0-9]+(?:S[0-9]+)?Q[0-9]+", title)
    if len(tag)==0:
        # print("No tag found for:", title)
        return None
    if len(tag)!=1:
        if len(set(tag))==1: # all elements in tag the same
            # warning("Same tag appears multiple times in line: {}".format(title))
            return tag[0]
        else:
            raise Exception("Different tags appear in the same line: {}".format(title))
    return tag[0]

def remove_tag(s):
    tag = get_tag(s)
    if tag:
        return s.replace(tag, "")
    else:
        return s


def order_lines(lines):
    for k in ["Q", "S", "F"]:
        lines.sort(key=lambda l: get_value(get_tag(l[1]), k))
    return lines


def get_headerless_lines(fname):
    f = open(fname, "r")
    output = []
    first = True
    for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
        if first:
            first = False
            continue
        output.append(line)
    return output


def get_header(fname):
    f = open(fname, "r")
    for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
        output = line
        break
    f.close()
    return output


def write_csv(contents, fname):
    with open(fname, 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(contents)


