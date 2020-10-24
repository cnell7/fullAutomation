import os
import vtk

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

    inputTags = ['0078-1.stl',
    '0100-1.stl',
    '0123-1.stl',
    '0125-1.stl',
    '0217-1.stl',
    '0343-1-1.stl']

    switcher = {1: [-50,50,0],
    2: [0,50,0],
    3: [50,50,0],
    4: [-50,0,0],
    5: [0,0,0],
    6: [50,0,0]}
    count = 1

    reader = vtk.vtkSTLReader()
    appendFilter = vtk.vtkAppendPolyData()

    for i in input:
        reader.SetFileName(i)
        trans = vtk.vtkTransform()
        coordinates = switcher[count]
        trans.Translate(coordinates[0], coordinates[1], coordinates[2])

        process = vtk.vtkTransformPolyDataFilter()
        process.SetTransform(trans)
        process.SetInputConnection(reader.GetOutputPort())
        process.Update()

        appendFilter.AddInputConnection(process.GetOutputPort())


        count += 1

    appendFilter.Update()

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
