import maya.cmds as cmds
import hanoi

global srcList 
scrList = []
global tempList
tempList = []
global destList
destList = []



def initialisePegList(listName):
	global srcList
	srcList = list(reversed(listName))


def moveSrcPeg(ring, start, end):
	
	timeInc = (end-start)/4
	end = start+timeInc
	hanoi.offPeg(ring, start, end)
	start = end
	end = start+(2*timeInc)
	hanoi.srcPeg(ring, start, end)
	start = end
	end = start + timeInc
	hanoi.onPeg(ring, start, end, srcList)
	global srcList
	srcList.append(ring)

def moveTempPeg(ring, start, end):
	
	timeInc = (end-start)/4
	end = start+timeInc
	hanoi.offPeg(ring, start, end)
	start = end
	end = start+(2*timeInc)
	hanoi.tempPeg(ring, start, end)
	start = end
	end = start + timeInc
	hanoi.onPeg(ring, start, end, tempList)
	global tempList
	tempList.append(ring)

def moveDestPeg(ring, start, end):

	timeInc = (end-start)/4
	end = start+timeInc
	hanoi.offPeg(ring, start, end)
	start = end
	end = start+(2*timeInc)
	hanoi.destPeg(ring, start, end)
	start = end
	end = start + timeInc
	hanoi.onPeg(ring, start, end, destList)
	global destList
	destList.append(ring)
	
def moveRing(ring, start, end, type):

	if type == 'src':
		moveSrcPeg(ring, start, end)
	elif type == 'temp':
		moveTempPeg(ring, start, end)
	elif type == 'dest':
		moveDestPeg(ring, start, end)

def hanoifunc(n, src, dst, tmp):
    if n <= 0:
        pass
    else:
        for h in hanoifunc(n-1, src, tmp, dst):
            yield h
        yield(src, dst)
        for h in hanoifunc(n-1, tmp, dst, src):
            yield h

def main(num, start, end):

	timeInc = end-start

	moves = [h for h in hanoifunc(num, 'src', 'dest', 'temp')]
	
	for i in range (0, len(moves)):
		
		frm = moves[i][0]
		to = moves[i][1]
		
		if frm == 'src':
			global srcList
			ring = srcList.pop()
		elif frm == 'temp':
			global tempList
			ring = tempList.pop()
		elif frm == 'dest':
			global destList
			ring = destList.pop()
		
		moveRing(ring, start, end, to)
		
		start = end
		end = end+timeInc
	cmds.playbackOptions(maxTime=end)
