import os
import subprocess

def getpodnames():
    #cmd = ["kubectl", "get, "all"]
    results = []
    cmd = ["kubectl", "get", "pods", "-o", "jsonpath='{.items[*].metadata.name}'"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    for line in p.stdout:
        line = line.rstrip("\r\n")
        if line.startswith("#"):
            continue
        line = line[1:-1]
        pods = line.split(" ")
        results.extend(pods)
   
    return results

def makepodname(name="kuberun-"):
    names = getpodnames()
    i = 0
    leading_zeros = 4
    if name not in names:
        return name
    while True:
        num = str(i).zfill(leading_zeros)
        podname = name + num
        if podname not in names:
            return podname
        i += 1
    return None

def makefilename(filename, ext):
    # if filename does not exist, return filename
    # else keep adding _1, _2, _3, etc. until filename does not exist
    if not os.path.exists(filename + ext):
        return filename + ext
    i = 1
    leading_zeros = 4
    while True:
        num = str(i).zfill(leading_zeros)
        newfilename = filename + "_" + num + ext
        if not os.path.exists(newfilename):
            return newfilename
        i += 1
    return None