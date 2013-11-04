from siutils import si
si = si()					# win32com.client.Dispatch('XSI.Application')
from siutils import log		# LogMessage
from siutils import disp	# win32com.client.Dispatch
from siutils import C		# win32com.client.constants


#logs a collection of looped edge rings
log(si.Selection(0).SubComponent.ComponentCollection.IndexArray)

#Application.SelectGeometryComponents(item.FullName+".edge"+str(x2))
