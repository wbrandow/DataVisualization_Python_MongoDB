# DataVisualization_Python_MongoDB
Data visualization example using Python and MongoDB

# Purpose
This code was developed as part of a CS-340 class focused on client/server development using Python and MongoDB.  The ficticious client for this software trains rescue dogs and needs a dashboard to visualize a database shared with them from local animal shelters.  The program creates a table and map and provides a dropdown for the user to select which type of rescue animal they are searching for.  The dashboard updates based on the specifications provided by the client for each rescue type.  The animal_shelter.py file is responsible for connecting to the database and handling basic CRUD (create, read, update, delete) operations.  The main.py file creates the interactive dashboard and passes queries to the database through an instance of the animalShelter class.

<img width="1781" alt="animal_shelter_Dashboard" src="https://user-images.githubusercontent.com/31283921/218006443-30d7d9cf-ffbc-4e4b-94de-aec774e729bc.png">

# Additional Libraries
Several Python libraries are imported by this project including:
  - PyMongo
  - Pandas
  - Matplotlib
  - Dash
  - Dash_leaflet
  - Numpy
  - Plotly
  - Jupyter_plotly_dash
  
All of these libraries can be installed using pip install <library>.

This project also utilizes MongoDB.  Most of the development was done using the server version of MongoDB in a virtual environment.  However, this software also runs successfully on the cloud utilizing MongoDB Atlas simply by modifying the MongoClient connection url in animal_shelter.py and passing the appropriate authentication.

# Lessons Learned
I am learning a ton of valuable information through this project.  I now have the experience to write queries, create indexes, manage users, import data, and more in MongoDB.  These skills should be easy to learn for other noSQL and relational databases.  This was my first experience using Dash to create an interactive data visualization dashboard.  I can imagine Dash being a powerful tool for future projects to quickly create client-side dashboards.

# Future Development
This is very much an active project at the time of this writing.  I will first focus on enabling geolocation on the map component.  I will also add a pie chart widget to display the breeds of the animals in each table produced by the dashboard.  I would also like to prompt the user for their username and password.  
