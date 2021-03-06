def interp_cry(sInput, iResample=8000):
    """
    do entire process for one audio file
    TODO real life test algorithm in classify.classify_cry
    """
    
    #edge detection on the recording, isolate the cry(s)
    import isolate
    iSampleRate, laAudios, laCorrs = isolate.isolate_cries(sInput, iResample=iResample)
    
    dAggregatedCries = {}
    
    #run returned samples against database
    import classify
    
    for i in range(len(laAudios)):
        
        import numpy as np
        aAudio = laAudios[i]
        aCorr = laCorrs[i]
        aTime = np.array( [float(i)/iSampleRate for i in range(len(aAudio))] )
        
        dInput = {
            'iSampleRate': iSampleRate,
            'aTime': aTime,
            'aAudio': aAudio,
            'aCorr': aCorr
        }
        
        dAllSorted, dSortedTypes = classify.classify_cry(dInput)
        
        for i in range(len(dSortedTypes['lsNames'])):
            sCryType = dSortedTypes['lsNames'][i]
            sCryVal = dSortedTypes['liConfidence'][i]
            
            try:
                dAggregatedCries[sCryType] += sCryVal
            except KeyError:
                dAggregatedCries[sCryType] = sCryVal
        
    
    
    lAggregatedNames = [x for (y,x) in sorted(zip(dAggregatedCries.values() ,dAggregatedCries.keys()), reverse=True)]
    lAggregatedValues = [round(y,2) for (y,x) in sorted(zip(dAggregatedCries.values() ,dAggregatedCries.keys()), reverse=True)]
    
    dRet = {
        'lsNames': lAggregatedNames,
        'liValues': lAggregatedValues
    }
    
    return dRet
    


























