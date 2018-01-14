# Python Script
from flask import Flask
from flask import request, redirect, render_template

import subprocess
import shutil
import os
import glob
from hs_restclient import HydroShare, HydroShareAuthBasic
import json
import os
import subprocess
import sys
app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/sciunit/<id>', methods=['GET', 'POST'])
def runSCI(id):
    if request.method == 'POST':
        auth = HydroShareAuthBasic(
            username=request.form['username'], password=request.form['password'])

        hs = HydroShare(auth=auth)

        hs.getResource('e987ddcf73a94376a4a70e5db0fb7646',
                       destination='/home/ubuntu/hydroshareLink/', unzip=True)
        subprocess.Popen('sciunit open /home/ubuntu/hydroshareLink/e987ddcf73a94376a4a70e5db0fb7646/e987ddcf73a94376a4a70e5db0fb7646/data/contents/modflow.zip',
                         stdout=subprocess.PIPE, shell=True)

    	os.chdir("/home/ubuntu/test/")
    	hs.getResource(id, destination='/home/ubuntu/test/', unzip=True)
        proc = subprocess.Popen('sciunit repeat e2 ' +
                                str(id), stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read()
    	abstract = ''
    	title = 'MODFLOW_NWT_SCIUNIT_OUTPUT'
    	keywords = ('my keyword 1', 'my keyword 2')
    	rtype = 'MODFLOWModelInstanceResource'
    	output_id = hs.createResource(
    	    rtype, title, abstract=abstract, keywords=keywords)
    	for file in os.listdir("/home/ubuntu/test/MODFLOW/"):
            if file != "mfnwt":
                hs.addResourceFile(output_id, "/home/ubuntu/test/MODFLOW/" + file)
    	title = 'ModflowNwtCollection'
    	keywords = ('MODFLOW-NWT Input data','MODFLOW-NWT Output data', 'MODFLOW-NWT')
    	rtype = 'CollectionResource'
    	resource_id = hs.createResource(rtype, title, abstract=abstract, keywords=keywords)

    	metaData = {'relations' : []}
    	newObject = {}
    	newObject['type'] = 'hasPart'
    	newObject['value'] = 'http://www.hydroshare.org/resource/' + str(id) + '/'
    	metaData['relations'].append(newObject)
    	newObject = {}
    	newObject['type'] = 'hasPart'
    	newObject['value'] = 'http://www.hydroshare.org/resource/' + str(output_id) + '/'
    	metaData['relations'].append(newObject)
    	hs.updateScienceMetadata(resource_id, metadata = metaData)

    	return output
    return render_template('login.html', id = str(id))
