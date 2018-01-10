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

@app.route('/id/<id>',  methods = ['GET','POST'])
def runScript(id):
    if request.method == 'POST':
	    auth = HydroShareAuthBasic(username=request.form['username'], password=request.form['password'])
	    hs = HydroShare(auth=auth)

	    os.chdir("/home/ubuntu/modflownwt/")
	    hs.getResource(id, destination='/home/ubuntu/modflownwt/', unzip=True)
	    subprocess.call("sudo cp /home/ubuntu/modflownwt/" + str(id) + '/' + str(id) +
			    '/data/contents/* /home/ubuntu/modflownwt/workspace/Data', shell=True)
	    subprocess.call("sudo rm -r /home/ubuntu/modflownwt/" +
			    str(id), shell=True)

	    subprocess.call(
		"sudo docker run -v /home/ubuntu/modflownwt/workspace:/app/workspace bakinam/modflownwt", shell=True)
	    #
	    hs.getResource("ace3231be6b64ee6a02ddd8e6dfa3d5d",
			   destination='/home/ubuntu/modflownwt/', unzip=True)
	    subprocess.call("sudo cp /home/ubuntu/modflownwt/ace3231be6b64ee6a02ddd8e6dfa3d5d/ace3231be6b64ee6a02ddd8e6dfa3d5d/data/contents/* /home/ubuntu/modflownwt/workspace/MODFLOW", shell=True)
	    subprocess.call(
		"sudo rm -r /home/ubuntu/modflownwt/ace3231be6b64ee6a02ddd8e6dfa3d5d", shell=True)

	    # Locate the file with the .nam extension
	    for file in os.listdir("/home/ubuntu/modflownwt/workspace/MODFLOW"):
		if file.endswith(".nam"):
		    filename = file

	    # # Run the model
	    os.chdir("/home/ubuntu/modflownwt/workspace/MODFLOW")
	    subprocess.call(
		"sudo chmod u+x /home/ubuntu/modflownwt/workspace/MODFLOW/mfnwt", shell=True)
	    subprocess.call(
		"sudo /home/ubuntu/modflownwt/workspace/MODFLOW/mfnwt " + filename, shell=True)

	    abstract = 'This resource contains the prepared input data for the MODFLOW-NWT and the output from running the MODFLOW-NWT engine using this prepared data as a model input'
	    title = 'MODFLOW_NWT_OUTPUT'
	    keywords = ('my keyword 1', 'my keyword 2')
	#    keywords = ('MODFLOW-NWT Input data','MODFLOW-NWT Output data', 'MODFLOW-NWT')
	    rtype = 'MODFLOWModelInstanceResource'
	    output_id = hs.createResource(rtype, title, abstract=abstract, keywords=keywords)

	    for file in os.listdir("/home/ubuntu/modflownwt/workspace/MODFLOW"):
		try:
		    hs.deleteResourceFile(resource_id,file)
		except:
		    pass

	    # Upload to hydroshare
	    for file in os.listdir("/home/ubuntu/modflownwt/workspace/MODFLOW"):
		if file != "mfnwt":
		    hs.addResourceFile(output_id, "/home/ubuntu/modflownwt/workspace/MODFLOW/" + file)

	    subprocess.call("sudo rm /home/ubuntu/modflownwt/workspace/MODFLOW/*.*", shell=True)
	    subprocess.call("sudo rm -r  /home/ubuntu/modflownwt/workspace/Scratch", shell=True)
	    subprocess.call("sudo rm -r  /home/ubuntu/modflownwt/workspace/Framework", shell=True)
	    subprocess.call("sudo rm  /home/ubuntu/modflownwt/workspace/Data/*", shell=True)

	    abstract = 'My abstract'
	    title = 'MODFLOW NWT Collection'
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
	    return json.dumps(hs.getScienceMetadata(resource_id))
    return render_template('login.html', id = str(id))
