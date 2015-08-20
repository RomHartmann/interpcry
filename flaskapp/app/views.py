from flask import render_template, request, redirect, url_for
from app import app
import os



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    if request.method == 'POST':
        fFile = request.files['file']
        
        from datetime import datetime as dt
        sFilename = str(dt.now())
        
        sPath = os.path.join(os.getcwd(), "app/uploads", sFilename)
        
        fFile.save(sPath)
        
        return redirect(url_for('returned', sInput=sPath))
    else:
        return render_template('upload.html')
    
    



@app.route('/returned', methods=['GET', 'POST'])
def returned():
    sInput = request.args.get('sInput')
    
    from datetime import datetime as dt
    oBegin = dt.now()
    
    from interpcry import cry_pipeline
    
    dRet = cry_pipeline.interp_cry(sInput, iResample=None)
    
    sRet = "{0}: {1}".format(dRet['lsNames'], dRet['liValues'])
    
    #just shows time taken.  remove when no longer wanted
    sRet += "<br/> {0}".format(dt.now()-oBegin)
    
    
    return sRet

