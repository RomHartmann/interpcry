def classify_cry(dRec):
    """
    compare a cry to all pre-identified cries
    dictionary of form:
        dInput = {
            'iSampleRate': iSampleRate,
            'aTime': aTime,
            'aAudio': aAudio,
            'aCorr': aCorr
        }
    
    """
    import analyse
    import os
    
    iSelfCorrArea = analyse.analyse_cry(dRec, dRec)[1]
    
    lsCryNames = []
    liCryValues = []
    
    dCries = {}
    
    
    sCryDBDir = os.getcwd() + '/DB_cries'
    lsCryTypes = os.listdir(sCryDBDir)
    
    for sCryType in lsCryTypes:
        sCutDir = '{0}/{1}'.format(sCryDBDir, sCryType)
        
        for sCut in os.listdir(sCutDir):
            sDBDir = '{0}/{1}/{2}'.format(sCryDBDir, sCryType, sCut)
            
            iMisfit, iCorrArea = analyse.analyse_cry(dRec, sDBDir)
            
            iDeltaArea = abs(iCorrArea - iSelfCorrArea)
            iComparisonMetric = iMisfit * iDeltaArea    #TODO test accuracy of using one, the other, both as metrics
            
            lsCryNames.append(sCryType)
            liCryValues.append(iComparisonMetric)
            
            try:
                dCries[sCryType] += iComparisonMetric
            except KeyError:
                dCries[sCryType] = iComparisonMetric
    
    
    lsCryNamesSorted = [x for (y,x) in sorted(zip(liCryValues,lsCryNames))]
    liCryValuesSorted = [round(y,2) for (y,x) in sorted(zip(liCryValues,lsCryNames))]
    
    dAllSorted = {
        'lsNames': lsCryNamesSorted,
        'liValues': liCryValuesSorted
    }
    
    
    
    lsAllTopsSortedNames = [x for (y,x) in sorted(zip(dCries.values(), dCries.keys()))]
    liAllTopsSortedValues = [round(y,2) for (y,x) in sorted(zip(dCries.values(), dCries.keys()))]
    
    import common_fxns
    liConfidence = common_fxns.get_confidence(liAllTopsSortedValues)
    
    #aggregated and sorted results based on all comparisons, with normalized confidence results
    dSortedTypes = {
        'lsNames': lsAllTopsSortedNames,
        'liValues': liAllTopsSortedValues,
        'liConfidence': liConfidence
    }
    
    
    return dAllSorted, dSortedTypes















