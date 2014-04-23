
import maya.cmds as cmds
import functools
import hanoi
import HanoiMain as hm


global rings
global time
global srcList 
scrList = []
global tempList
tempList = []
global destList
destList = []


def createUI(windowTitle):
    
    windowID = 'myWindowID'
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
        
    mainLayout=cmds.window(windowID, title=windowTitle, sizeable=False, resizeToFitChildren=True)
    tab1 = cmds.frameLayout(label='General', collapsable=False, mh=5, parent=mainLayout)
    cmds.rowColumnLayout(nc=2, columnOffset=[(1, 'left', 10)], parent = tab1)
    cmds.text(label='Number of Rings: ')
    global rings   
    rings = cmds.intField( 'ringNo', v=3, min = 1)
    cmds.separator(height=5, style='none')
    cmds.separator(height=5, style='none')
    cmds.text(label='Move rate (frames): ') 
    global time 
    time = cmds.intField( 'time', v=20)
    cmds.separator(height=20, style='none')
    cmds.separator(height=20, style='none')
    cmds.button('newScene', label='New Scene', c=functools.partial(createNewScene, rings))
    cmds.button('generate', label='Generate Animation', enable=False, c=functools.partial(generateCallback))
    
    cmds.showWindow(windowID)
    
def createWarning():
       
    if cmds.window('warning', exists=True):
        cmds.deleteUI('warning')
    
    mainLayout=cmds.window('warning', title='WARNING', sizeable=False, resizeToFitChildren=True)
    tab1 = cmds.frameLayout(label='General', collapsable=False, mh=5, parent=mainLayout)
    cmds.rowColumnLayout(nc=2, columnOffset=[(1, 'left', 10)], parent = tab1)
    cmds.text(label='WARNING! You are trying to generate an animation sequence for more')
    cmds.separator(style='none')
    cmds.text(label='than 10 rings, this may take longer than the age of the universe!')
    cmds.separator(style='none')
    cmds.text(label='Are you sure you wish to proceed?')
    cmds.separator(style='none')
    cmds.separator(height=20, style='none')
    cmds.separator(height=20, style='none')
    cmds.button('cancel', label='Cancel', w=150, c='cmds.deleteUI("warning")')
    cmds.button('proceed', label='Proceed', w=150, c=functools.partial(proceedCallback))
    
    cmds.showWindow('warning')

    
def createNewScene(*args):
	cmds.select(all=True)
	cmds.delete()
	global rings
	rings=cmds.intField('ringNo', query=True, value=True)
	hanoi.newScene()
	ringList=hanoi.makeRingList(rings)
	hanoi.scaleRings(ringList)
	hanoi.placeRings(ringList)
	hanoi.colourRings(ringList)
	hm.initialisePegList(ringList)
	cmds.button('generate', e=True, enable=True)
	print 'New scene created with '+str(rings)+' rings'

def generateCallback(*args):
	if rings <= 10:  
		global time
		time =cmds.intField('time', query = True, value = True)
		hm.main(rings, 1, time)
		global destlist
		destlist = []
	else:
		createWarning()
	cmds.button('generate', e=True, enable=False)

def proceedCallback(*args):
    time =cmds.intField('time', query = True, value = True)
    hm.main(rings, 1, time)
    cmds.deleteUI(warningID)
        

createUI('Hanoi')

#createWarning()