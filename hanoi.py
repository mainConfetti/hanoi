import maya.cmds as cmds

global srcList 
scrList = []
global tempList
tempList = []
global destList
destList = []

def createMaterial(name, colour):
	'''Creates a new, crysal-like, phong material
		
		name: The name of the material
		colour: The RGB 0-1 values of the colour of the material
	'''

	cmds.sets(renderable = True, noSurfaceShader=True, empty = True, name="%sSG"%name)
	cmds.shadingNode("lambert", asShader = True, name = name)
	cmds.setAttr("%s.color"%name, colour[0], colour[1], colour[2], type ="double3")
	cmds.connectAttr("%s.outColor"%name, "%sSG.surfaceShader"%name)

def assignMaterial(name, object):
	'''Assigns a material to an object
		name: The name of the material
		object: The name of the object
	'''
	cmds.sets(object, edit=True, forceElement= "%sSG"%name)
	
def assignNewMaterial(name, colour, object):
	'''Calls 2 procedures assignMaterial and createMaterial to create a new material and assign it to
		an object
		
		name: The name of the material
		colour: The RGB 0-1 values of the colour of the material
		object: The name of the object 
	'''
	createMaterial(name, colour)
	assignMaterial(name, object)
	
def newScene():

	cmds.polyPlane(n="floor", h=30, w=30, sx=1, sy=1)
	cmds.polyCylinder(n="src", h=5, r=0.2)
	cmds.move(0,2.5,0, 'src', a = True)
	cmds.duplicate("src", n="temp")
	cmds.duplicate("src", n="dest")
	cmds.move(-8,0,0, "src", r=True)
	cmds.move(8,0,0, "dest", r=True)
	assignNewMaterial('floorMaterial', [0.3, 0.2, 0], 'floor')
	assignNewMaterial('pegMaterial', [0,0,0], 'src')
	assignMaterial('pegMaterial', 'temp')
	assignMaterial('pegMaterial', 'dest')
    

def makeRingList(num):    
    rings=[]
    cmds.polyCylinder(n="ring", h=0.2, r=0.5)
    cmds.move(-8,0.1,0, 'ring', a=True)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    for i in range(0,num):
        v = cmds.duplicate("ring")
        rings.append(v[0])
       
    cmds.delete('ring')
    return rings
        
def scaleRings(listName):
    scl=1
    for i in range(0, len(listName)):
        cmds.scale(scl,1,scl, listName[i], a=True)
        scl=scl+(5/float(len(listName)))
        
def placeRings(listName):
    for i in range (0, len(listName)):
        movey= (0.2*len(listName))-(0.2*i)-0.2
        cmds.move(0, movey, 0, listName[i], a=True)

def colourRings(listName):
	colourInc = 1.0/len(listName)
	for i in range(0, len(listName)):
		assignNewMaterial('ringMaterial'+str(i), [1-((colourInc/2)*i), 1-(colourInc*i), 1], listName[i])
		

def offPeg(ring, start, end):
	cmds.currentTime(start)
	cmds.select(ring)
	cmds.setKeyframe()
	cmds.setKeyframe(ring, at='translateY', v=5, t=end)

def onPeg(ring, start, end, pegList):
	moveY = 0 + (0.2*len(pegList))
	cmds.currentTime(start)
	cmds.select(ring)
	cmds.setKeyframe()
	cmds.setKeyframe(ring, at='translateY', v=moveY, t=end)
	
def srcPeg(ring,start,end):
	cmds.currentTime(start)
	cmds.select(ring)
	cmds.setKeyframe(t=[start, end])
	cmds.setKeyframe(ring, at='translateX', v=0, t=end)
	cmds.setKeyframe(ring, at='rotateZ', v=0, t=end)
	cmds.setKeyframe(ring, at='translateY', v=8.5, t=(start+end)/2)

def tempPeg(ring,start,end):
	cmds.currentTime(start)
	cmds.select(ring)
	cmds.setKeyframe(t=[start, end])
	cmds.setKeyframe(ring, at='translateX', v=8, t=end)
	cmds.setKeyframe(ring, at='rotateZ', v=180, t=end)
	cmds.setKeyframe(ring, at='translateY', v=8.5, t=(start+end)/2)
	
def destPeg(ring,start,end):
	cmds.currentTime(start)
	cmds.select(ring)
	cmds.setKeyframe(t=[start, end])
	cmds.setKeyframe(ring, at='translateX', v=16, t=end)
	cmds.setKeyframe(ring, at='rotateZ', v=360, t=end)
	cmds.setKeyframe(ring, at='translateY', v=8.5, t=(start+end)/2)