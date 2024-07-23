# VIRGO <img src="virgo/virgo.gif" width="100" height="100" />
## Visual Interface for Research using GEOS Output

## Background
Welcome esteemed scientist, heliophysist, astronomer, or otherwise cool person! We are glad to show you around virgo and how it might be useful in your groundbreaking research (or even just make your plots easier to create).

Virgo was developped in conjunction with NASA's Goddard Space Flight Center as a means of accelerating the extension of the [Goddard Earth Observing System](https://gmao.gsfc.nasa.gov/GEOS_systems/) (GEOS) into the upper atmosphere. Beyond this VIRGO has applications to researchers as a way to automate data manipulation and visualization through the use of visual scripting. Its core philosophy lies in its implementation of **Nodes** and **Edges** to make science code more reuasable and well-documented. Let's get after it!

## Installation

The easiest way to install VIRGO is through [Anaconda](https://www.anaconda.com/download/success) or [Miniconda](https://docs.anaconda.com/miniconda/). This installation will assume you have one of these installed on your machine.

1. Navigate to the directory where you want to install virgo using 
    ```
    cd dir
    ```
    REPLACING dir with the path of a folder you want to install virgo in
2. Clone the repository 
    ```
    git clone https://github.com/GeorgeHuber/virgo
    ```
    - If this command produces an error you may need to use a [personal access token](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/accessing-github-using-two-factor-authentication#authenticating-on-the-command-line-using-https) to authenticate your github account
    - Another alternative for less technically inclined folk may be to install [Github Desktop](https://desktop.github.com/download/), sign in, and clone the repository from there!

3. Navigate into the virgo folder using 
    ```
    cd virgo
    ```
4. To install the neccessary packages for virgo run 
    ```
    conda create --name virgo --file requirements.txt
    ```
This command creates a new conda environment with all the package versions specified in requirements.txt that can be reused the next time you run VIRGO.

## Get Started

Make sure you are inside the virgo folder in your terminal and then enter your conda environment with 
```
conda activate virgo
```
Finally run  
```
python3 -m virgo
```
and you should see the application pop up on your screen!

## Tutorial - In progress
- Use the top menu to open a file
- Click the buttons in the Nodes tab to add things to the canvas
- Double click to delete things from the canvas
- Click on an output to select it and then click on an input of another node to create a connection.
    - Click on the canvas to deselect a node
- Use the configurations tab to open a prebuilt graph setup
- Use the canvas top menu to save a canvas

## Nodes
VIRGO allows user to construct data flows using three main types of base nodes: Data source, functional, and graphical nodes.
### Adding Custom Functionality
### Data Sources
Data source nodes supply data to the rest of the flow, for each field of your file you want to visualize a different datasource node is needed. When a canvas is run, execution starts at a data source and propogates through the network
### Functional Nodes
### Graphical Nodes


## Technical Abstract
The Goddard Earth Observing System (GEOS) models dynamical, physical, chemical and biological features of the atmosphere within the Earth System Modeling Framework (ESMF) up to an altitude of ~75 kilometers. As part of ongoing efforts to study the coupling between the lower and upper atmosphere, GEOS’s upper boundary must be raised to successfully encompass the dynamics of the mesosphere and thermosphere resulting from vertical propagation of solar and lunar tides, gravity waves, and Kelvin waves. This must be accomplished through a time-consuming process of tweaking the model. We developed an open source Visual Interface for Research using GEOS Output (VIRGO) which streamlines the model development pipeline by integrating data transfer, manipulation, and visualization into a single application installed as a Python package. VIRGO allows users to create and save custom visualization configurations and then execute them in a single click, aiding researchers and promoting the reusability of science code. VIRGO contains 14 prebuilt configurations for looking at GEOS output files while also allowing users to easily create new plots through its use of modular nodes. The VIRGO application is open source and available through GitHub at https://github.com/GeorgeHuber/virgo. 


