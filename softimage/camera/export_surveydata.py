from siutils import si		# Application

root = si.ActiveSceneRoot

fileBrowser = XSIUIToolkit.FileBrowser
fileBrowser.Filter = "txt (*.txt)|*.txt||"
fileBrowser.ShowSave()
fileName = fileBrowser.filepathname
fso = XSIFactory.CreateObject('Scripting.FileSystemObject')
file = fso.CreateTextFile(fileName)

file.write("# Name       SurveyX       SurveyY       SurveyZ       Uncertainty \n")


# For survey data to work correctly in PFTrack the X and Z values must be swapped.
# WT SI scene 1 unit = 1 foot
#PFTrack survey data should be converted to meters.
for item in si.Selection:
	kine=item.Kinematics.Global.GetTransform2(1)
	x = kine.PosZ *.3048
	y = kine.PosY *.3048
	z = kine.PosX *.3048
	d = 0.0
	file.write( '"%s"\t%6f\t%6f\t%6f\t%6f\t\n'	%	(item.Name,si.XSIRound(x,6),si.XSIRound(y,6),si.XSIRound(z,6), d))
file.close()