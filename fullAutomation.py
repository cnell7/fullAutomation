import os
import vtk
import itertools

def main():
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
    input = ['./Priority2SaveDir/stx_neo-0078-1-6year_mid_keyChain.stl',
    './Priority2SaveDir/stx_neo-0100-1-6year_mid_keyChain.stl',
    './Priority2SaveDir/stx_neo-0123-1-6year_mid_keyChain.stl',
    './Priority2SaveDir/stx_neo-0125-1-6year_mid_keyChain.stl',
    './Priority2SaveDir/stx_neo-0217-1-6year_mid_keyChain.stl',
    './Priority2SaveDir/stx_neo-0343-1-1-6year_mid_keyChain.stl']

    inputTags = ['./Priority2NameTags/0078-1.stl',
    './Priority2NameTags/0100-1.stl',
    './Priority2NameTags/0123-1.stl',
    './Priority2NameTags/0125-1.stl',
    './Priority2NameTags/0217-1.stl',
    './Priority2NameTags/0343-1-1.stl']

    switcherBrain = {1: [-50,60,0],
    2: [0,60,0],
    3: [50,60,0],
    4: [-50,0,0],
    5: [0,0,0],
    6: [50,0,0]}
    switcherNameTag = {1: [-90,60,10],
    2: [-40,60,10],
    3: [10,60,10],
    4: [-90,0,10],
    5: [-40,0,10],
    6: [10,0,10]}
    count = 1

    appendFilter = vtk.vtkAppendPolyData()

    for (i, iT) in zip(input, inputTags):
        # Append key chain
        reader = vtk.vtkSTLReader()
        reader.SetFileName(i)
        trans = vtk.vtkTransform()
        coordinates = switcherBrain[count]
        trans.Translate(coordinates[0], coordinates[1], coordinates[2])

        process = vtk.vtkTransformPolyDataFilter()
        process.SetTransform(trans)
        process.SetInputConnection(reader.GetOutputPort())
        process.Update()

        appendFilter.AddInputConnection(process.GetOutputPort())
        appendFilter.Update()

        # Append nane tag
        reader = vtk.vtkSTLReader()
        reader.SetFileName(iT)
        trans = vtk.vtkTransform()
        coordinates = switcherNameTag[count]
        trans.Translate(coordinates[0], coordinates[1], coordinates[2])

        process = vtk.vtkTransformPolyDataFilter()
        process.SetTransform(trans)
        process.SetInputConnection(reader.GetOutputPort())
        process.Update()

        appendFilter.AddInputConnection(process.GetOutputPort())
        appendFilter.Update()
        count += 1

    #appendFilter.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(appendFilter.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(actor)
    renderer.SetBackground(.3, .2, .1)

    renderWindow.Render()
    renderWindowInteractor.Start()

    #writer = vtk.vtkPolyDataWriter()
    #writer.SetFileName('./Priority2SaveDir/stx_neo-0078-1-6year_mid_keyChain(2).stl')
    #writer.SetInputConnection(appendFilter.GetOutputPort())
    #writer.Write()
    return True

main()
