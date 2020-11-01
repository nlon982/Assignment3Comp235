from CS235Flix.adapters.movie_file_csv_reader import MovieFileCSVReader
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.director import Director
from CS235Flix.domain.genre import Genre


def test_read_csv_file(movie_file_csv_reader):
    movie_file_csv_reader.read_csv_file()

    dataset_of_movies = movie_file_csv_reader.dataset_of_movies
    dataset_of_actors = movie_file_csv_reader.dataset_of_actors
    dataset_of_directors = movie_file_csv_reader.dataset_of_directors
    dataset_of_genres = movie_file_csv_reader.dataset_of_genres

    assert len(dataset_of_movies) == 100 # this is how much is in the test path
    assert len(set(dataset_of_actors)) == len(dataset_of_actors) # check unique items only
    assert len(set(dataset_of_directors)) == len(dataset_of_directors)  # ^ ditto
    assert len(set(dataset_of_genres)) == len(dataset_of_genres)  # ^ ditto


    temp_chris_pratt = Actor("Chris Pratt")
    chris_pratt = dataset_of_actors[dataset_of_actors.index(temp_chris_pratt)] # get chris pratt object that's in the database

    actor_colleagues = [Actor("Vin Diesel"), Actor("Bradley Cooper"), Actor("Zoe Saldana"), Actor("Ty Simpkins")] # actor colleagues of Chriss Pratt's from two different movies
    for a_actor in actor_colleagues:
        assert chris_pratt.check_if_this_actor_worked_with(a_actor)

    movie_object = dataset_of_movies[0]
    assert movie_object.title == "Guardians of the Galaxy"
    assert movie_object.release_year == 2014
    assert movie_object.runtime_minutes == 121
    assert movie_object.description == "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."
    assert movie_object.external_rating == 8.1
    assert movie_object.external_rating_votes == 757074
    assert movie_object.revenue == 333.13
    assert movie_object.metascore == 76
    assert isinstance(movie_object.director, Director)
    assert isinstance(movie_object.actors[0], Actor)
    assert isinstance(movie_object.genres[0], Genre)