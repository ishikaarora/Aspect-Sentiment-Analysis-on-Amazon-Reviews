# Aspect-and-Opinion-Extraction-on-Amazon-Reviews

Project Repository for CSE-6242 course.


The folder structure of the package is mentioned below -
/data - Contains all the required data files
/src - Contains all the code files
/UI - Contains the required files for seeing the Visualisation



`conda create --name <env> --file requirements.txt`



And everytime you commit, run this command in the project folder to update the new set of requirements, if you have installed new libraries for the project -


`conda list -e > requirements.txt`


Ask me(Achyut), if you want to know more about conda environments!


## Using fetch_data file

Created a script to download files. Use this in your command line -


`fetch_data.py <local>`

here <local> is an argument
1 = Downloads only two files
0 = Downloads all 46 data files
