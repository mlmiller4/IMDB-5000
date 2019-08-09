# IMDB-5000
Data analysis using Pandas performed on a 5000-record set of movie data from the IMDB. 

## Prerequisites

The following must be installed:
* Python 3.x
* [NumPy](https://www.numpy.org/)
* [Pandas](https://pandas.pydata.org/)
* [Flask](https://www.fullstackpython.com/flask.html)
* [Flask_RESTful](https://flask-restful.readthedocs.io/en/latest/)

'''
## Getting Started
Either clone this repository or download the code as a .zip file and extract to a folder.
You may do the following:

## Display the top ten most profitable genres, actors, directors, director/actor pairs as well as the highest ranked director/actor pairs on the IMDB:
$python IMDB.py

## Run unit tests on the functions in the IMDB.py file:
$python test_IMDB.py

## Start a REST endpoint that contains the actors name and number of facebook likes:
$python flask_app_IMDB.py
'''

### Using the REST endpoint:
To see an actor's full name and number of facebook likes, enter the following, along with the actor's last name.
curl http://127.0.0.1:5000/actor/<actor last name>

#### Example:
To see information for Harrison Ford, enter http://127.0.0.1:5000/actor/Ford

To add a new actor's information, use the following:
$curl -H "Content-Type:application/json" -X POST -d '{"last name":"<actor's last name>","full name":"<actor's full name>","facebook likes":<number of facebook likes>}' http://127.0.0.1:5000/actor/<actor's last name>
  
#### Example:
To enter Tom Hardy, who has 27,000 facebook likes, use the following:
$curl -H "Content-Type:application/json" -X POST -d '{"last name":"Hardy","full name":"Tom Hardy","facebook likes":27000}' http://127.0.0.1:5000/actor/Hardy

To update an existing actor's information use the following:
$curl -H "Content-Type:application/json" -X PUT -d '{"last name":"<actor's last name>","full name":"<actor's full name>","facebook likes":<number of facebook likes>}' http://127.0.0.1:5000/actor/<actor's last name>

#### Example:
To change Harrison Ford's number of facebook likes to 123456, use the following:
$curl -H "Content-Type:application/json" -X PUT -d '{"last name":"Ford","full name":"Harrison Ford","facebook likes":123456}' http://127.0.0.1:5000/actor/Ford

To delete and actor from the REST endpoint use the following:
$curl -X DELETE http://127.0.0.1:5000/actor/<actor's last name>

#### Example:
To delete Harrison Ford from the rest endpoint:
$curl -X DELETE http://127.0.0.1:5000/actor/Ford
You will receive a "Ford is deleted" message, and if you enter http://127.0.0.1:5000/actor/Ford you will get an "Actor not found" message.


