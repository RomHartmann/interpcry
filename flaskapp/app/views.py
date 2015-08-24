from flask import render_template, request, redirect, url_for
from app import app
import os


@app.route('/')
def home():
    return redirect(url_for('upload'))




@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    if request.method == 'POST':
        fFile = request.files['file']
        
        from datetime import datetime as dt
        sFilename = str(dt.now())+".wav"
        
        sPath = os.path.join(os.getcwd(), "app/uploads", sFilename)
        
        fFile.save(sPath)
        
        return redirect(url_for('returned_gui', sInput=sPath))
    else:
        return render_template('upload.html')
    
    


@app.route('/returned', methods=['GET', 'POST'])
def returned():
    "returns json format results, no markup"
    from interpcry import cry_pipeline
    sInput = request.args.get('sInput')
    dRet = cry_pipeline.interp_cry(sInput, iResample=None)
    os.remove(sInput)
    
    import json
    return json.dumps(dRet)



@app.route('/returned_gui', methods=['GET', 'POST'])
def returned_gui():
    """returns the results with some markup for the GUI"""
    from datetime import datetime as dt
    oBegin = dt.now()
    
    from interpcry import cry_pipeline
    sInput = request.args.get('sInput')
    dRet = cry_pipeline.interp_cry(sInput, iResample=None)
    os.remove(sInput)
    
    ldRet = [{'sCry':dRet['lsNames'][i], 'sConfidence': dRet['liValues'][i]} for i in range(len(dRet['lsNames']))]
    
    import json
    sTimeDelta = str(dt.now() - oBegin)
    
    
    return render_template('results.html',
                           sTime = sTimeDelta,
                           sUploadURL = "/upload",
                           ldRet = ldRet)










