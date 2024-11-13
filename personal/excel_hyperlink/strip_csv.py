import os
import csv

path = "./csv"
filelist = os.listdir(path=path)

for file in filelist:
  infile = f"{path}/{file}"
  outfiile = f"{path}/stripped_{file}"
  print(infile)

  with open(infile, "r") as readfile:
    str = readfile.read()
    stripped = str.replace("\n", "")
    
    with open(outfiile, "w") as writefile:
      writefile.write(stripped)
