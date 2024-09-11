# employee-entry-form-web-app
This is a web app built with Flask.

# Installation
First, you need to clone this repository:

    git clone https://github.com/zunairAbid/employee-entry-form-web-app.git

Then change into the employee-entry-form-web-app folder:
    
    cd  employee-entry-form-web-app

Now, we will need to create a virtual environment and install all the dependencies:

    python3 -m venv venv       # on Windows, use "python -m venv venv" instead

    source venv/bin/activate   # on Windows, use "venv\Scripts\activate" instead
    
    pip install -r requirements.txt

# Run Unit tests

python3 -m unittest discover -s tests

# Run Flask App

python3 app.py
