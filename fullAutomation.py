import os
import vtk


def matchBrainTags():
    matchedBrainTags = {}
    brainScans = os.listdir("./Priority2SaveDir")
    for filename in os.listdir("./Priority2NameTags"):
        for brain in brainScans:
            if(filename[:len(filename)-4] in brain):
                matchedBrainTags[filename] = brain
    
    return False


def createScene():
    return False


def main():
    matchedBrainTags = matchBrainTags()
    return False


main()
