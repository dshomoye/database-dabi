## Database, webapp and API for fictional NE Railway system
This is more or less a proof of concept/use case of a datasbase for a train system - originally a school project,
along with the web app and API endpoints (which I added to make things more interesting) 
>  this was a database focused class, being able to write correct SQL for managing the entire database was important hence the lack of use of an ORM. 

Everything is in Python (2.7)
The web server is implemented with Flask (`pip install flask`)
And the API endpoint is with FLask RESTful (`pip install flask_restful`)
Running is simple: `python run.py`

An accompanying Android App that takes advantage of the API is in the works.

***
### For the REST API, these are the resources and corresponding methods currently implemented:

For making changes to Tickets and viewing passenger info, the cliet must be logged in at /login
* POST with data:
```
{
    username: {username},
    password: {password}
}
```
a token will be issued if password is right. subsequent requests should include this token.

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
    - data parameters:
        * token
* POST
    - data parameters:
        * username
        * password
        * first_name
        * last_name
        * email
        * *address* (optional)

#### `Ticket`:
URL: `\tickets`
*Methods*:

**GET**: <`\tickets\{ticket_numer}`>
- data parameters: 
    * token (user must be owner of {ticket_number})
**POST** : <`\tickets`>
    * data parameters:
        - token
        - passenger_id
        - start_station
        - end_station
        - train_number
        - trip_date_time: e.g. `'2017-07-08 04:05:06'`
        - fare
        - *return_date_time*
        - *return_train*

