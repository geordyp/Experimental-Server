# Experimental_Server
This is server code for a RESTful web service created with Python and the Flask microframework. This web service will support my smaller projects.

## Currently supported REST clients
* [To Dooli](http://www.geordywilliams.com/projects/ToDooli/): A to do list application. [View Code](http://www.github.com/geordyp/To-Dooli)

## Technologies Used
* Flask
* SQLAlchemy

## Setup
1. After cloning this repo to your machine, cd into 'Experimental_Server'.
2. Enter the command `vagrant up`. This command can take awhile to run. Ignore the error `default: stdin: is not a tty`.
3. Enter the command `vagrant ssh`.
4. Once vagrant is up and running cd into '/vagrant'.
5. Create the data tables using the `python database_setup.py` command.
6. (Optional) Then use the `python populate_database.py` command to add some filler data.
7. At this point, all the data should be setup. You can launch the application using the `python __init__.py` command. Just open up a browser and navigate to 'localhost:5000'.

## Helpful Resources
* https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
* https://www.digitalocean.com/community/tutorials/how-to-create-your-first-digitalocean-droplet-virtual-server
* https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps

## Author
Geordy Williams
