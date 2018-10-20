# Aspect-Sentiment-Analysis-on-Amazon-Reviews

Project Repository for CSE-6242 course.


It will be better for us to coordinate different packages using conda environment. Added is the requirements.txt file.

Use this -


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
