# Commands to be executed to setup and run the app.
# Commands provided are strictly to be used in windows to setup on other OS, refer internet.

# Open the project folder
cd demosite
# use tree command tree should look like this
tree
├───demoapp
│   ├───migrations
│   └───templates
└───demosite

# Create a virtual environment for the app outside the DEMOSTITE APP
py -m venv ../demoproject-env

# Activate virtual environment
..\demoproject-env\Scripts\activate

# Install the requirements/packages
py -m pip install -r requirements.txt

# Migrate the app
py manage.py migrate

# Run the app
py manage.py runserver

# Test on browser - localhost:8000

# Create a superuser/admin
py manage.py createsuperuser

# Access admin site - localhost:8000/admin
