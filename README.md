# Database, webapp and API for fictional NE Railway system
This is more or less a proof of concept/use case of a datasbase for a train system - originally a school project,
along with the web app and API endpoints (which I added to make things more interesting)

Everything is in Python (2.7)
The web server is implemented with Flask (`pip install flask`)
And the API endpoint is with FLask RESTful (`pip install flask_restful`)
Running is simple: `python run.py`

An accompanying Android App that takes advantage of the API is in the works.

***
## For the REST API, these are the resources and corresponding methods currently implemented:

#### `Station` :
URL: `\stations`
*Methods*: 
*GET*: 
    - data parameters: none

#### `Schedule` :
URL `\schedule`
*Methods*:
**GET**:
* data parameters:
    - start_station
    - end_station
    - trip_date
    - *time_of_day* (optional)

#### `Passenger`:
URL: `\passengers\{passenger_id}`
*Methods*:
* GET:
    - data parameters: none

#### `Ticket`:
URL: `\tickets`
*Methods*:
**GET**: <`\tickets\{ticket_numer}`>
    - data parameters: none
**POST** : <`\tickets`>
    * data parameters:
        - passenger_id
        - start_station
        - end_station
        - train_number
        - trip_date_time: e.g. `'2017-07-08 04:05:06'`
        - fare
        - *return_date_time*
        - *return_train*

