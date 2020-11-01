import os
import vtk
import itertools

def main():
    # Match keychains and nametags (will be used later when rest of script is working)
    brainDir = "./Priority2SaveDir"
    keyChainDir = "./Priority2NameTags"
    matchedBrainTags = {}
    brainScans = os.listdir(brainDir)
    # Matches the two if the brain filename contains the tag filename
    for filename in os.listdir(keyChainDir):
        for brain in brainScans:
            if(filename[:len(filename)-4] in brain):
                matchedBrainTags[filename[:len(filename)-4]] = brain

    # Test keychain input
    input = ['./Priority2SaveDir/stx_neo-0078-1-6year_mid_keyChain.stl',
    './Priority2SaveDir/stx_neo-0100-1-6year_mid_keyChain.stl',
    './Priority2SaveDir/stx_neo-0123-1-6year_mid_keyChain.stl',
    './Priority2SaveDir/stx_neo-0125-1-6year_mid_keyChain.stl',
    './Priority2SaveDir/stx_neo-0217-1-6year_mid_keyChain.stl',
    './Priority2SaveDir/stx_neo-0343-1-1-6year_mid_keyChain.stl']

    # Test nametag input
    inputTags = ['./Priority2NameTags/0078-1.stl',
    './Priority2NameTags/0100-1.stl',
    './Priority2NameTags/0123-1.stl',
    './Priority2NameTags/0125-1.stl',
    './Priority2NameTags/0217-1.stl',
    './Priority2NameTags/0343-1-1.stl']

    # Hard cooded translation for keychains
    switcherBrain = {1: [-50,60,0],
    2: [0,60,0],
    3: [50,60,0],
    4: [-50,0,0],
    5: [0,0,0],
    6: [50,0,0]}
    # Hard cooded translation for nametags
    switcherNameTag = {1: [-90,60,0],
    2: [-40,60,0],
    3: [10,60,0],
    4: [-90,0,0],
    5: [-40,0,0],
    6: [10,0,0]}

    keychainBounds = []
    keychainZMax = 0

    # Find max z height so that it can be used to raise other surfaces to that level (make level scene)
    for keychain in input:
        reader = vtk.vtkSTLReader()  
        reader.SetFileName(keychain)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        mapper.Update()
        bounds = mapper.GetBounds()
        if(bounds[4] > keychainZMax):
            keychainZMax = bounds[4]

    print(keychainZMax)
    coordinateCount = 1 # Used to keep track of which translation needs to be done for what part of the scene the loop is on.
    appendFilter = vtk.vtkAppendPolyData()

    for (i, iT) in zip(input, inputTags):
        # Append key chain
        reader = vtk.vtkSTLReader()  # Read keychain
        reader.SetFileName(i)

        # Use mapper to get keychain bounds to correctly place in scene
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        mapper.Update()
        bounds = mapper.GetBounds() #Return bounding box (array of six doubles) of data expressed as (xmin,xmax, ymin,ymax, zmin,zmax).

        trans = vtk.vtkTransform()   # Set translation
        coordinates = switcherBrain[coordinateCount]
        trans.Translate(coordinates[0], coordinates[1], (coordinates[2] + (keychainZMax - bounds[4])))  # Add z offset to final translation

        process = vtk.vtkTransformPolyDataFilter()  # Process translate
        process.SetTransform(trans)
        process.SetInputConnection(reader.GetOutputPort())
        process.Update()

        appendFilter.AddInputConnection(process.GetOutputPort())    # Append to scene
        appendFilter.Update()

        # Append name tag
        reader = vtk.vtkSTLReader() # Read nametag
        reader.SetFileName(iT)

        trans = vtk.vtkTransform()  # Set transltion
        coordinates = switcherNameTag[coordinateCount]
        trans.Translate(coordinates[0], coordinates[1], coordinates[2] + keychainZMax)

        process = vtk.vtkTransformPolyDataFilter()  # Process translate
        process.SetTransform(trans)
        process.SetInputConnection(reader.GetOutputPort())
        process.Update()

        appendFilter.AddInputConnection(process.GetOutputPort())    # Append to scene
        appendFilter.Update()
        coordinateCount += 1

    '''
    # Create test visual of what the scene looks like
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
    '''
    # Write print scene
    writer = vtk.vtkSTLWriter()
    writer.SetFileName('./Priority2SaveDir/stx_neo-0078-1-6year_mid_keyChain_2.stl')
    writer.SetInputConnection(appendFilter.GetOutputPort())
    writer.Write()
    return True


main()
