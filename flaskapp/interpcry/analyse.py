def analyse_cry(dRec, xDB):
    """
    dRec must be dictionary of form:
    dInput = {
            'iSampleRate': iSampleRate,
            'aTime': aTime,
            'aAudio': aAudio,
            'aCorr': aCorr
        }
    xDB can be string for filename, or dictionary of above form
    
    Correlation and least squares comparison between audio files
    classifications based on classifications by Pricilla Dunstan
    """
    import numpy as np
    
    def normalize(aArray):
        iMax = np.max(aArray)
        return [i/iMax for i in aArray]
    
    
    def calc_misfit(a1, a2):
        """
        calculates the misfit between the 2 arrays and returns a scalar
        shortest array length is taken
        """
        iLen = len(a1) if len(a1)<len(a2) else len(a2)
        
        iMisfit = 0
        for i in range(iLen):
            iMisfit += (a1[i] - a2[i])**2
        return iMisfit
    
    
    def round_sci(iNum, iSigs):
        """
        round number to significant figures
        """
        return float(format(iNum, '.{0}g'.format(iSigs)))
    
    
    iRecSampleRate = dRec['iSampleRate']
    aRecTime_NoShift = dRec['aTime']
    aRecAudio = dRec['aAudio']
    aRecCorr_NoShift = dRec['aCorr']
    
    
    if type(xDB) == str:
        import common_fxns
        sDBDir = xDB
        (iDBSampleRate, 
            aDBTime_NoShift, 
            aDBAudio, 
            aDBCorr_NoShift) = common_fxns.process_dir(sDBDir)[0:4]
        
    elif type(xDB) == dict:
        iDBSampleRate = xDB['iSampleRate']
        aDBTime_NoShift = xDB['aTime']
        aDBAudio = xDB['aAudio']
        aDBCorr_NoShift = xDB['aCorr']
        
    else:
        raise ValueError('Please enter a string or dict of the correct format')
    
    
    
    aRecCorr_NoShift = normalize(aRecCorr_NoShift)
    aDBCorr_NoShift = normalize(aDBCorr_NoShift)
    
    
    
    #shifted guassian correlations such that misfit has more meaning
    #shifted such that maxima line up
    iIndexMax = np.argmax(aRecCorr_NoShift)
    iDBIndexMax = np.argmax(aDBCorr_NoShift)
    
    #always shifting right: therefore shift where argmax is less
    #for y values, prepend 0, for tive values, prepend time increments
    if iDBIndexMax > iIndexMax:
        #shift signal 1 to the right
        iShift = iDBIndexMax - iIndexMax
        aRec = np.zeros(len(aRecCorr_NoShift) + iShift)
        aRec[iShift:] = aRecCorr_NoShift
        
        aRecTime = np.zeros(len(aRecTime_NoShift) + iShift)
        aRecTime[:iShift] = np.array([i/iRecSampleRate for i in range(iShift)])
        aRecTime[iShift:] = aRecTime_NoShift + iShift/iRecSampleRate
        
        aDB = aDBCorr_NoShift
        aDBTime = aDBTime_NoShift
    else:
        #shift signal 2 to the right
        iShift = iIndexMax - iDBIndexMax
        aDB = np.zeros(len(aDBCorr_NoShift) + iShift)
        aDB[iShift:] = aDBCorr_NoShift
        
        aDBTime = np.zeros(len(aDBTime_NoShift) + iShift)
        aDBTime[:iShift] = np.array([i/iDBSampleRate for i in range(iShift)])
        aDBTime[iShift:] = aDBTime_NoShift + iShift/iDBSampleRate
        
        aRec = aRecCorr_NoShift
        aRecTime = aRecTime_NoShift
    
    #correlation between 2 signals
    #order matters for the calculations to get iCorrArea
    bRecLonger = len(aRecTime) > len(aDBTime)
    
    #the fftconvolve needs the longer array to be placed first, time needs to be the longer one
    aCorrTime = aRecTime if bRecLonger else aDBTime
    
    aLonger = aRec if bRecLonger else aDB
    aShorter = aDB if bRecLonger else aRec
    
    #np.correlate(aRec, aDB, 'same') takes too long, fftconvolve is faster with near identical results
    from scipy import signal
    aCorr = signal.fftconvolve(aLonger, aShorter, mode='same') 
    
    
    #least squares comparison to get misfit
    iMisfit = calc_misfit(aRec, aDB)
    iCorrArea = np.trapz(aCorr, aCorrTime)
    
    #round to 3 significant figures
    iMisfit = round_sci(iMisfit, 3)
    iCorrArea = round_sci(iCorrArea, 3)
    
    
    
    
    return iMisfit, iCorrArea


















