from base import *
import os
from tqdm import tqdm

wd = os.getcwd()
od = wd + "\\output"

partID = ''
partIDs = []
while partID != 'e':
    partID = input("Enter a part ID; or, enter 'e' to end: ")
    partIDs.append(partID)
partIDs = partIDs[:-1]

if not os.path.exists(od):
    os.mkdir(od)

for partID in tqdm(partIDs):
    os.mkdir(od + "\\s" + str(partID))
    recurrsionModule([partID], od + "\\s" + str(partID), [])