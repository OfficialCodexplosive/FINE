[![Build Status](https://travis-ci.com/FZJ-IEK3-VSA/FINE.svg?branch=master)](https://travis-ci.com/FZJ-IEK3-VSA/FINE) [![Version](https://img.shields.io/pypi/v/FINE.svg)](https://pypi.python.org/pypi/FINE) [![Documentation Status](https://readthedocs.org/projects/vsa-fine/badge/?version=latest)](https://vsa-fine.readthedocs.io/en/latest/) [![PyPI - License](https://img.shields.io/pypi/l/FINE)]((https://github.com/FZJ-IEK3-VSA/FINE/blob/master/LICENSE.txt)) [![codecov](https://codecov.io/gh/FZJ-IEK3-VSA/FINE/branch/master/graph/badge.svg)](https://codecov.io/gh/FZJ-IEK3-VSA/FINE)


<a href="https://www.fz-juelich.de/iek/iek-3/DE/Home/home_node.html"><img src="http://www.fz-juelich.de/SharedDocs/Bilder/IBG/IBG-3/DE/Plant-soil-atmosphere%20exchange%20processes/INPLAMINT%20(BONARES)/Bild3.jpg?__blob=poster" alt="Forschungszentrum Juelich Logo" width="230px"></a> 

# FINE - Framework for Integrated Energy System Assessment

The FINE python package provides a framework for modeling, optimizing and assessing energy systems. With the provided framework, systems with multiple regions, commodities and time steps can be modeled. Target of the optimization is the minimization of the total annual cost while considering technical and enviromental constraints. Besides using the full temporal resolution, an interconnected typical period storage formulation can be applied, that reduces the complexity and computational time of the model.

If you want to use FINE in a published work, please [**kindly cite following publication**](https://www.sciencedirect.com/science/article/pii/S036054421830879X) which gives a description of the first stages of the framework. The python package which provides the time series aggregation module and its corresponding literatur can be found [**here**](https://github.com/FZJ-IEK3-VSA/tsam).

## Features
* representation of an energy system by multiple locations, commodities and time steps
* complexity reducing storage formulation based on typical periods


## Documentation

A "Read the Docs" documentation of FINE can be found [**here**](https://vsa-fine.readthedocs.io/en/latest/).

## Installation
### Prepare and install required software
1.  Install anaconda [by choosing your operating system here](https://docs.anaconda.com/anaconda/install/). If you are a Windows 10 user, remember to tick "Add Anaconda to my PATH environment variable" during installation under "Advanced installations options".
2. Install git from https://git-scm.com/downloads
### Prepare folder
1. Open a prompt e.g. "anaconda prompt" or "cmd" from the windows start menu
2. Make a folder where you want to work, for example C:\Users\<your username>\work with "mkdir C:\Users\<your username>\work"
3. Go to that directory with "cd C:\Users\<your username>\work" at the command line


### Get source code via GIT

Clone public repository or repository of your choice first
```
git clone https://github.com/FZJ-IEK3-VSA/FINE.git 
```
Move into the FINE folder with
```
cd fine
```

### Installation for users
It is recommended to create a clean environment with conda to use FINE because it requires many dependencies. 

```
conda env create -f requirements.yml
activate FINE
```
### Installation for developers
Create a development environment if you want to modify it.
Install the requirements in a clean conda environment:
```
conda env create -f requirements_dev.yml
activate FINE_dev
```

The development environent includes all packages to check if FINE is working.
```
pytest --cov=FINE test/
```
If all tests run through, you have successfully installed FINE. 
## Examples

A number of [**examples**](examples/) shows the capabilities of FINE.

## Using an Integrated Developer Environment (IDE)
In order to efficiently develop FINE further, install Visual Studio Code and open it. Make sure the Python Extension is installed by clicking this button and searching for Python. Then open the FINE folder with File > Open Folder and open it. VS-Code will automatically look for an environment but perhaps it is not the right one. In order to choose the correct environment, click Strg+Shift+P/Ctrl+Shift+P and type in the field Python: Select Interpreter and choose the correct interpreter (here: 'fine_dev',conda).Then, we can configure the tests as next step. Therefore, call again Strg+Shift+P/Ctrl+Shift+P and type Python: Configure tests and choose pytest and the root directory. If successful, following symbol should pop up on the left side with which you can navigate through the tests. In order to make the test run in Visual Studio Code an empty file with the title '__init__.py' needs to be added to the test folder (C:\Users\<your username>\work\FINE\test).
		

	


## License

MIT License

Copyright (C) 2016-2020 Lara Welder, Theresa Groß, Leander Kotzur, Robin Beer, Henrik Büsing, Dilara Caglayan, Thomas Grube, Heidi Heinrichs, Maximilian Hoffmann, Timo Kannengießer, Kevin Knosala, Felix Kullmann, Stefan Kraus, Jochen Linßen, Peter Markewitz, Lars Nolting, Jan Priesmann, Bismark Singh, Andreas Smolenko, Peter Stenzel, Chloi Syranidou, Johannes Thürauf, Michael Zier, Martin Robinius, Detlef Stolten

You should have received a copy of the MIT License along with this program.
If not, see https://opensource.org/licenses/MIT


## About Us 
<a href="https://www.fz-juelich.de/iek/iek-3/DE/Home/home_node.html"><img src="https://www.fz-juelich.de/SharedDocs/Bilder/IEK/IEK-3/Abteilungen2015/VSA_DepartmentPicture_2019-02-04_459x244_2480x1317.jpg?__blob=normal" alt="Institut TSA"></a> 

We are the [Institute of Energy and Climate Research - Techno-economic Systems Analysis (IEK-3)](https://www.fz-juelich.de/iek/iek-3/DE/Home/home_node.html) belonging to the [Forschungszentrum Jülich](www.fz-juelich.de/). Our interdisciplinary institute's research is focusing on energy-related process and systems analyses. Data searches and system simulations are used to determine energy and mass balances, as well as to evaluate performance, emissions and costs of energy systems. The results are used for performing comparative assessment studies between the various systems. Our current priorities include the development of energy strategies, in accordance with the German Federal Government’s greenhouse gas reduction targets, by designing new infrastructures for sustainable and secure energy supply chains and by conducting cost analysis studies for integrating new technologies into future energy market frameworks.

## Contributions and Users


Within the BMWi funded project [**METIS**](http://www.metis-platform.net/) we develop together with the RWTH-Aachen ([**Prof. Aaron Praktiknjo**](http://www.wiwi.rwth-aachen.de/cms/Wirtschaftswissenschaften/Die-Fakultaet/Institute-und-Lehrstuehle/Professoren/~jgfr/Praktiknjo-Aaron/?allou=1&lidx=1)), the EDOM Team at FAU ([**PD Bismark Singh**](https://www.math.fau.de/wirtschaftsmathematik/team/bismark-singh/)) and the [**Jülich Supercomputing Centre**](http://www.fz-juelich.de/ias/jsc/DE/Home/home_node.html) new methods and models within FINE.

<a href="http://www.metis-platform.net/"><img src="http://www.metis-platform.net/metis-platform/DE/_Documents/Pictures/projectTeamAtKickOffMeeting_640x338.jpg?__blob=normal" alt="METIS Team" width="400px" style="float:center"></a> 

Dr. Martin Robinius is teaching a [**course**](https://www.campus-elgouna.tu-berlin.de/energy/v_menu/msc_business_engineering_energy/modules_and_curricula/project_market_coupling/) at TU Berlin in which he is introducing FINE to students.

<p float="left">
<a href="https://www.rwth-aachen.de/go/id/a/"> <img src="https://jugit.fz-juelich.de/iek-3/shared-code/fine/uploads/633d3c56d4fde45de2691c0262f96697/RWTH_Logo.png" width="230" /> </a> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
<a href="https://www.fau.de/"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Friedrich-Alexander-Universit%C3%A4t_Erlangen-N%C3%BCrnberg_logo.svg/2000px-Friedrich-Alexander-Universit%C3%A4t_Erlangen-N%C3%BCrnberg_logo.svg.png" width="230" /> </a>
</p>

## Acknowledgement

This work was supported by the Helmholtz Association under the Joint Initiative ["Energy System 2050   A Contribution of the Research Field Energy"](https://www.helmholtz.de/en/research/energy/energy_system_2050/).

<a href="https://www.helmholtz.de/en/"><img src="https://www.helmholtz.de/fileadmin/user_upload/05_aktuelles/Marke_Design/logos/HG_LOGO_S_ENG_RGB.jpg" alt="Helmholtz Logo" width="200px" style="float:right"></a>
