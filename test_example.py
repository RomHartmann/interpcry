#--------------------------Black box example-------------------------
#paths
sInput = '/home/roman/Critical_ID/interpcry/example_cry.wav'


#interp
iResample=8000

import cry_pipeline
dRet = cry_pipeline.interp_cry(sInput, iResample=iResample)


print "Returned:    ", dRet['lsNames'], dRet['liValues']

















