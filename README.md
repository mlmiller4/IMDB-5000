# IMDB-5000
Data analysis using Pandas performed on a 5000-record set of movie data from the IMDB. 

## Prerequisites

The following must be installed:
* [Python 3.x](https://www.python.org/downloads/)
* [NumPy](https://www.numpy.org/)
* [Pandas](https://pandas.pydata.org/)
* [Flask](https://www.fullstackpython.com/flask.html)
* [Flask_RESTful](https://flask-restful.readthedocs.io/en/latest/)


## Getting Started
Either clone this repository or download the code as a .zip file and extract to a folder.
You may do the following:

### Display the top ten most profitable genres, actors, directors, director/actor pairs as well as the highest ranked director/actor pairs on the IMDB:
$python IMDB.py

### Run unit tests on the functions in the IMDB.py file:
$python test_IMDB.py

### Start a REST endpoint that contains the actors name and number of facebook likes:
$python flask_app_IMDB.py


### Using the REST endpoint:

### GET:
To see an actor's full name and number of facebook likes, enter the following, along with the actor's last name:

$curl -s http://<i></i>127.0.0.1:5000/actor/[actor's unspaced name]

#### Example:
To see information for Harrison Ford, enter http://<i></i>127.0.0.1:5000/actor/HarrisonFord

### POST
To add a new actor's information, use the following:

$curl -H "Content-Type:application/json" -X POST -d '{"name":"[actor's name]","facebook likes":[number of facebook likes],"unspacedName":"[actor's unspaced name]}' http://<i></i>127.0.0.1:5000/actor/[actor's unspaced name]
  
#### Example:
To enter Tom Hardy, who has 27,000 facebook likes, use the following:

$curl -H "Content-Type:application/json" -X POST -d '{"name":"Tom Hardy","facebook likes":27000,"unspacedName":"TomHardy"}' http://<i></i>127.0.0.1:5000/actor/TomHardy

Note: If you try to post an actor who's name is already present, you will get the message "Actor with the name [actor name] already exists."

### PUT
To update an existing actor's information use the following:

$curl -s -H "Content-Type:application/json" -X PUT -d '{"name":"[actor's name]","unspacedName":"[actor's unspaced name]","facebook likes":[number of facebook likes]}' http://<i></i>127.0.0.1:5000/actor/[actor's unspaced name]

#### Example:
To change Harrison Ford's number of facebook likes to 123456, use the following:

$curl -s -H "Content-Type:application/json" -X PUT -d '{"name":"Harrison Ford","unspacedName":"HarrisonFord","facebook likes":123456}' http://<i></i>127.0.0.1:5000/actor/HarrisonFord

### DELETE
To delete an actor from the REST endpoint use the following:

$curl -s -X DELETE http://<i></i>127.0.0.1:5000/actor/[actor's unspaced name]

#### Example:
To delete Harrison Ford from the rest endpoint:

$curl -s -X DELETE http://<i></i>127.0.0.1:5000/actor/HarrisonFord

You will receive a "HarrisonFord is deleted" message, and if you enter http://<i></i>127.0.0.1:5000/actor/HarrisonFord you will get an "Actor not found" message.


