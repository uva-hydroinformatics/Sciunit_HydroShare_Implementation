# Sciunit_HydroShare_Implementation
This repository has the implementation for the sciunit and Hydroshare. It contains a python script to download and SCIUNIT and input data from hydroshare, run the model contained within the sciunit, and post the output back to hydroshare.
The sciunit folder contains some of the files in the sciunit. Build_modflow.py is the pre-processing data file. Workflow.sh is the script to run the the model with input data inside of the sciunit.

The templates folder contains the HTML template for the login page. Server.py is the flask script.
The code uses Python Flask to trigger the processing of input files from Hydroshare. 
By sending an HTTP GET request with the Hydroshare ID of the input files it will download them and run the engine.   

To setup this Python Flask webserver on an Ubuntu System follow the steps below:

First obtain the scripts from this repository:  

```shell
git clone https://github.com/uva-hydroinformatics-lab/Sciunit_HydroShare_Implementation.git
```    

On a fresh ubuntu instance install nginx, python, and gunicorn:  
```shell
sudo apt-get install -y python python-pip nginx gunicorn
``` 

Install the required python packages:  
```shell
pip install flask hs_restclient numpy fiona rasterio flopy
```  

Setup Nginx:  
```shell
sudo /etc/init.d/nginx start
sudo rm /etc/nginx/sites-enabled/default
sudo touch /etc/nginx/sites-available/flask_project
sudo ln -s /etc/nginx/sites-available/flask_project /etc/nginx/sites-enabled/flask_project 
```   

Then edit the config file
```shell
sudo vim /etc/nginx/sites-enabled/flask_project
```  

```nginx
server {
  location / {
      proxy_pass http://localhost:8000;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
  }
}
```   

Restart Nginx:
```shell
sudo /etc/init.d/nginx restart
```  

Start the scrript using gunicorn:
```shell
cd Sciunit_HydroShare_Implementation
gunicorn app:app -b localhost:8000
```  
