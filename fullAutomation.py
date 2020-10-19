import os
import vtk


def matchBrainTags():
    brainDir = "./Priority2SaveDir"
    keyChainDir = "./Priority2NameTags"
    testFile = "/mnt/c/Users/Christian/Code/research/niral/fullautomation/Priority2SaveDir/stx_neo-0078-1-6year_mid_keyChain.stl"
    matchedBrainTags = {}
    brainScans = os.listdir(brainDir)
    # Matches the two if the brain filename contains the tag filename
    for filename in os.listdir(keyChainDir):
        for brain in brainScans:
            if(filename[:len(filename)-4] in brain):
                matchedBrainTags[filename[:len(filename)-4]] = brain

    transform = vtk.vtkTransform()
    polyData = loadSTL(testFile)
    return False


def createScene():
    return False


def loadSTL(name):
    # Load the given STL file, and return a vtkPolyData object for it
    reader = vtk.vtkSTLReader()
    reader.SetFileName(name)
    reader.Update()
    polydata = reader.GetOutput()
    return polydata


def main():
    # Match brain images with their respective name tags
    matchedBrainTags = matchBrainTags()
    return False


main()
