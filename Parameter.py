
# device parameter list
usrp_parameters = {
		'centerFrequency': 2.45e9,
		'gain': 30,
		'fftsize': 4096,
		'window' : 'none',
		'recordTime' : 1,
		'bandwidth':4000000,
		'position': [None,None],
		'step': [0.1,0.1]
		}
maxGain = 76
minCenterFrequency = 70e6
maxCenterFrequency = 7e9
minBandwidth = 200e3
maxBandwidth = 5e6
maxRecordTime = 10
maxStepSize = 10
singleStep = 0.01