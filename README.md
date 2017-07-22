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

    sample response: [
    {
        "station_code": "BOST",
        "station_name": "Boston South Station, MA"
    },
    {
        "station_code": "BBAY",
        "station_name": "Boston Back Bay, MA"
    },... ]

#### `Schedule` :
URL `\schedule`
*Methods*:
**GET**:
* data parameters:
    - start_station
    - end_station
    - trip_date
    - *time_of_day* (optional)

- sample query:
    
    `/schedule?start_station=MYST&end_station=WGTN&trip_date=2017-20-05`
- response:

    `[
    {
        "arrival": "08:45:00",
        "fare": 26,
        "time_out": "05:32:00",
        "train_num": 9
    },
    {
        "arrival": "11:45:00",
        "fare": 26,
        "time_out": "08:32:00",
        "train_num": 10
    }, ... ]`

#### `Passenger`:
URL: `\passengers\{passenger_id}`
*Methods*:
* GET:
    - data parameters:
        * token
- sample query: 

    `/passengers/5?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpheSIsImV4cCI6MTUwMDcyNzYxOH0.4-57_43Hx7y6Uk-oNWU_L6VulKSHOsqrLpodh176Pcs`

- response:

    `{ "address": "as", "email": "jay@jay", "first_name": "jay", "last_name": "jay" }`

* POST - returns the passenger_id on successful creation
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

