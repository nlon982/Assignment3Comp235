# CS235Flix

## Description

This is Nathan Longhurst's submission for Assignment 3, Comp235.

A Web application that demonstrates use of Python's Flask framework. The application makes use of libraries such as the Jinja templating library and WTForms. Architectural design patterns and principles including Repository (both Memory and an SQL Database have been implemented), Dependency Inversion and Single Responsibility have been used to design the application. The application uses Flask Blueprints to maintain a separation of concerns between application functions. Testing includes unit and end-to-end testing using the pytest tool.

## Installation

**Installation via requirements.txt**

```shell
$ cd Assignment3Comp235
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:COMPSCI-235' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *Assignment3Comp235* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Testing

Testing requires that file *Assignment3Comp235/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *Assignment3Comp235/tests/data* directory. 

E.g. 

`TEST_DATA_PATH_MEMORY = os.path.join('C:', os.sep, 'Users', 'ian', 'Documents', 'Python dev', 'Assignment3Comp235', 'tests', 'data', 'memory')`

assigns TEST_DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

`C:\Users\ian\Documents\python-dev\Assignment3Comp235\tests\data`

Testing optionally requires that you tell it what database type to do e2e testing on (specifically the tests found in test_web_app.py). See *CS235Flix/tests/conftest.py*, and change the line in the client's fixture 'REPOSITORY' to the desired repository type

You can then run tests from within PyCharm.


## Configuration

The *Assignment3Comp235/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

Database relevant variables
* 'SQLALCHEMY_DATABASE_URI': this is Database URI (this as is)
* 'SQLALCHEMY_ECHO': set to 'TRUE' or 'FALSE' that turns printing of all SQL statements on/off
* 'REPOSITORY': set to 'memory' or 'database'
