import os
import vtk


def matchBrainTags():
    brainDir = "./Priority2SaveDir"
    keyChainDir = "./Priority2NameTags"
    matchedBrainTags = {}
    brainScans = os.listdir(brainDir)
    # Matches the two if the brain filename contains the tag filename
    for filename in os.listdir(keyChainDir):
        for brain in brainScans:
            if(filename[:len(filename)-4] in brain):
                matchedBrainTags[filename[:len(filename)-4]] = brain

    # transform = vtk.vtkTransformPolyDataFilter()    # vtkTransformPolyDataFilter takes vtkAbstractTransform as a parameter
    reader = vtk.vtkSTLReader()
    reader.SetFileName('./Priority2SaveDir/stx_neo-0078-1-6year_mid_keyChain.stl')

    trans = vtk.vtkTransform()
    trans.Translate(1, 1, 1)

    process = vtk.vtkTransformPolyDataFilter()
    process.SetTransform(trans)
    process.SetInputConnection(reader.GetOutputPort())
    process.Update()

    process.GetOutputPort()
    # VTK append polydata
    # Need a writer to save images after translate
    return False


def createScene():
    return False

def main():
    # Match brain images with their respective name tags
    matchedBrainTags = matchBrainTags()
    return False


main()
