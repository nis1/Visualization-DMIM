## DICOM 3D Medical Image Modeling (DMIM)

Nowadays, patients are sent to MRI, PET, and CT scans more than before. Each scan produces a large amount of information of a patient, normally as a set of 2D slices, that will be inspected by a doctor or a technician. The project aims to visualize any DICOM images by creating a 3D model in addition to the classic slice-by-slice inspection.

&nbsp;
## Installation

This tutorial uses Conda and PIP. Please make sure to install them before you  proceed the next steps.

1. Create virtual environment with the following instruction:

```
$ conda create -n DMIM python=3.5.4
```
“DMIM” is the name of the new environment. Please make sure to install    	Python 3.5.4, and not other version.

2.  Activate the new DMIM environment by typing:
```
$ conda activate DMIM
```
3. Clone the repository: 
```
$ git clone https://github.com/nis1/Visualization-DMIM.git
```
4.  Install MongoDB:
```
$ conda install mongodb
```
5. Enter the repository folder, and install the requirements:
```
$ pip install -r requirements.txt
```
6. Open new terminal window and start MongoDB:
```
$ mongod
```
7. Finally, run the website from the repository main folder:
```
$ FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run
```
8. The website should be available at http://localhost:5000/

A successful installation will result in the following index page: 

<kbd>![Home Page](https://github.com/nis1/Visualization-DMIM/blob/master/static/wiki/4.jpg)</kbd>
&nbsp;&nbsp;

## More images from the app

#### Store and analyze various cases
<kbd>![Store and analyze various cases](https://github.com/nis1/Visualization-DMIM/blob/master/static/wiki/5.jpg)</kbd>
&nbsp;

#### 3D Analysis
<kbd>![3D Analysis](https://github.com/nis1/Visualization-DMIM/blob/master/static/wiki/8.jpg)</kbd>
&nbsp;

#### Slice Analysis
<kbd>![Slice Analysis](https://github.com/nis1/Visualization-DMIM/blob/master/static/wiki/10.jpg)</kbd>
&nbsp;

#### Draw on slices
<kbd>![Draw on slices](https://github.com/nis1/Visualization-DMIM/blob/master/static/wiki/11.jpg)</kbd>
&nbsp;&nbsp;


## References

The X ToolKit:
https://github.com/xtk/X

AMI: 
https://github.com/FNNDSC/ami
