# On_Deck
To do web application

## Technologies Used
* Flask
* SQLAlchemy
* Knockout JS

## Setup
1. After cloning this repo to your machine, cd into 'To_Dooli'.
2. Enter the command `vagrant up`. This command can take awhile to run. Ignore the error `default: stdin: is not a tty`.
3. Enter the command `vagrant ssh`.
4. Once vagrant is up and running cd into '/vagrant'.
5. The database should be setup already. Incase you want to start fresh, you can delete catalog.db and use the `python database_setup.py` command. Then use the `python populate_database.py` command to add the categories and some filler data. I make it clear in the file where unnecessary data is added so feel free to remove or comment out those lines if you wish.
6. At this point, all the data should be setup. You can launch the application using the `python application.py` command. Just open up a browser and navigate to 'localhost:5000'.

## Author
Geordy Williams
