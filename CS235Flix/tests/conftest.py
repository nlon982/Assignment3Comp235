import os
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from CS235Flix import create_app
from CS235Flix.adapters import memory_repository, database_repository
from CS235Flix.adapters.memory_repository import MemoryRepository
from CS235Flix.adapters.orm import metadata, map_model_to_tables

from CS235Flix.adapters.movie_file_csv_reader import MovieFileCSVReader


#TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'ianwo', 'OneDrive', 'Documents', 'PythonDev', 'repo 02.07.2020',
#                              'COVID-19', 'tests', 'data')
#TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'iwar006', 'Documents', 'Python dev', 'COVID-19', 'tests', 'data')

TEST_DATA_PATH_MEMORY = os.path.join("C:", os.sep, "Users", "Nathan Longhurst", "OneDrive - The University of Auckland", "b Comp235", "Assignment 3", "GitHub - Assignment 3", "Assignment3Comp235", "CS235Flix", "tests", "data", "memory")
TEST_DATA_PATH_DATABASE = os.path.join("C:", os.sep, "Users", "Nathan Longhurst", "OneDrive - The University of Auckland", "b Comp235", "Assignment 3", "GitHub - Assignment 3", "Assignment3Comp235", "CS235Flix", "tests", "data", "database")
# the above two folders actually contain the identical test .csv's. I have created two seperate paths for the sake of adaptability, if someone decides they want to have different test folders (that'll require changing the tests accordingly too).


TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///cs235flix-test.db'


@pytest.fixture
def database_engine():
    engine = create_engine(TEST_DATABASE_URI_FILE)
    clear_mappers()
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield engine
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def empty_session():
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def blank_session_factory(): # copy and past of session_factory fixture, just without populate
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    #database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory
    metadata.drop_all(engine)
    clear_mappers()


@pytest.fixture
def movie_file_csv_reader():
    movie_csv_path = os.path.join(TEST_DATA_PATH_MEMORY, 'Data1000Movies.csv')
    return MovieFileCSVReader(movie_csv_path)

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH_MEMORY, repo)
    return repo

@pytest.fixture
def blank_memory_repository():
    repo = MemoryRepository()
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'REPOSITORY': 'memory',                       # Set to 'memory' or 'database' depending on desired repository.
        'TEST_DATA_PATH': TEST_DATA_PATH_MEMORY,      # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='thorke', password='cLQ^C#oFXloS'):
        return self._client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
