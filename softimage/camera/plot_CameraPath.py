from siutils import si		# Application
from siutils import siut	# XSIUtils
from siutils import log		# LogMessage
from siutils import C		# win32com.client.constants

class SubCurve:
    """
    class to hold subcurve points in
    """
    def __init__(self):
        self.points = []
        self.nbpoints = 0
    def AddPoint(self, x, y, z, w = 1.0):
		#self.points.append({'x': x, 'y':y, 'z':z, 'w':w})
		
        self.points.append( x )
        self.points.append( y )
        self.points.append( z )
        self.points.append( w )
        self.nbpoints += 1  
		
    def MakeKnots(self):
        self.knots = [0.0]*(self.nbpoints+2)
        knotVal = 1.0
        for i in range(3,len(self.knots)):
            self.knots[i] = knotVal
            if i < len(self.knots)-3:
                knotVal += 1.0
				
    def MakeLinearKnots(self):
        self.knots = [0.0]*self.nbpoints
        for i in range(len(knots)):
            self.knots[i] += float(i)
			
    def MakeValid(self):
        """
        make sure the sub curve is at least 4 points
        support 2 and 3 point curves by duplicating end points
        """

		#self.points = self.points[0]
		
        if self.nbpoints < 4:
            if self.nbpoints < 1:
                return False
            if self.nbpoints == 2:
                self.points = self.points[:4] + self.points
                self.nbpoints += 1
            if self.nbpoints == 3:
                self.points += self.points[-4:]
                self.nbpoints += 1
        return True

class CurveList:
    """
    basic curve list class
    """
    def __init__(self):
        self.name = "ASECurve_1"
        self.subCurves = []
        self.position = XSIMath.CreateVector3()
    def AddSubCurve(self, curve):
        self.subCurves.append( curve )

root = si.ActiveSceneRoot
oPicked = si.PickElement( C.siCameraFilter, 'Pick Camera', 'Pick Camera' )

if oPicked(0) != 0:
	si.LogMessage( "Picked element: " + str(oPicked(2)) )
	si.SelectObj( str(oPicked(2)), "", 1 )
	camera=str(oPicked(2))

	firstkey = Application.FirstKey(camera,"","")
	lastkey = Application.LastKey(camera,"","") 
	totalkeys =  (lastkey-firstkey)

	for item in si.Selection:
		subcurve=SubCurve()
		for i in range ( int(firstkey -1), int(lastkey +1)):
			i += 1
			kine=item.Kinematics.Global.GetTransform2(i)
			x=kine.PosX
			y=kine.PosY
			z=kine.PosZ
			subcurve.AddPoint(float(x), float(y), float(z))
			
		#print (subcurve.points)
		subcurve.MakeValid()
		
		knots = [0.0]*subcurve.nbpoints
		for i in range(len(knots)):
			knots[i] += float(i)
			
		siCurve = root.AddNurbsCurveList2()
		siCurve.ActivePrimitive.Geometry.AddCurve( subcurve.points, knots, False, 1, 18, C.siSINurbs )
		
		
else:
	print "User Aborted"
