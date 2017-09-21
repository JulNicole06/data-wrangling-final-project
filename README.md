# Data Wrangling Final Project - Wrangle OpenStreetMap Data


## Project Details

This project is connected to the Data Wrangling course and I have chosen to use SQL for the database.

#### Project Rubric can be found here: https://review.udacity.com/#!/rubrics/25/view

### Files included in this submission:

##### 1. audit.py
Code used to audit OSM XML file before 

##### 2. street_suffix.py
Code used to scrape 'https://pe.usps.com/text/pub28/28apc_002.htm' to obtain a mapping of street suffix abbreviations to full street suffix names

##### 3. update.py
Code used to programatically "clean" values investigated in audit.py

##### 4. schema.py
Code provided by Udacity to validate that the transformed data is in the correct format

##### 5. prepare_for_database.py
Initial code provided by Udacity to clean and shape XML elements into provided schema for conversion to .csv files in preparation for upload to SQL database.  I updated the shape_element() fuction and created the get_tags() function to complete this task.  
	
##### 6. create_database.py
Code used to import .csv files into SQL tables

##### 7. sample.osm
sample OSM XML file of Roswell, GA

##### 8. final_submission.py
Code used to run files 1-6 created in this project for the final submission

##### 9. submission_document.pdf
Project Summary and write-up