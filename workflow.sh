#!/bin/bash
file=/home/ubuntu/test/$1/$1/data/contents/*.nam
name=$(basename ${file[0]} .nam)
#echo $name

cp -a /home/ubuntu/test/$1/$1/data/contents/.  /home/ubuntu/test/Data/
(cd /home/ubuntu/test; python build_modflow.py)

(cd /home/ubuntu/test/MODFLOW;  ./mfnwt *.nam)


