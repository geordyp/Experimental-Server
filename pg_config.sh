apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-sqlalchemy
apt-get -qqy install python-pip
pip install werkzeug==0.8.3
pip install flask==0.9
pip install Flask-Login==0.1.3
pip install requests
pip install httplib2
pip install -U flask-cors
pip install flask-httpauth

sudo -u postgres psql -c "CREATE USER me WITH PASSWORD 'password';"
sudo -u postgres psql -c "CREATE DATABASE tasks;"
