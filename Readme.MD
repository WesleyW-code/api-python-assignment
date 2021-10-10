# Patient API

> CRUD API to schedule and manage appointments

We are building an API with [FastAPI](https://fastapi.tiangolo.com/)

## Outline
The below will outline the backend for my appointment service, that allows various operations involving patients and their appointments. 

> Functionality

- [ ] Create a patient
- [ ] Read all patients
- [ ] Read a patient
- [ ] Delete a patient
- [ ] Create a appointment
- [ ] Read all appointments
- [ ] Read an appointment for a patient
- [ ] Delete an appointment for a patient
- [ ] Update a patient
- [ ] Update an appointment 

## Important locations
>>> src/app/main.py contains the code that runs the actual API, using FastAPI
>>> src/app/api/crud.py creates the worker functions that are used in the API to create, view, update and delete data entries

## To get started
Install [Docker](https://www.docker.com/)
Navigate to the location of the folder 
```bash
cd folder\location\api-python-assignment
```
Create a directory for DB data
```bash
mkdir db_data
```

Get the Docker container up and running
```bash
docker-compose up -d --build
```

To set up the tables:
```bash
docker-compose run api alembic upgrade head
```

## Detail
I performed all testing of these functions in the [docs](http://localhost:8080/docs) for this api. I confirmed that the tables were added correctly by checking in `localhost:16543/` (login: `username: admin@admin.com` & `password: test123!`). Note: a new server will be required. The hostname for this server is "db" and the DB username and password is both `postgres`

### The methods available in the API are as follows: 
Note: to test that this function is working, because a front end is not currently available, inputs will need to be tested at the documentation location: [docs](http://localhost:8080/docs).

#### [To create a patient](http://localhost:8080/patient/):
Input:
- patients name 
- patients contact number 
eg: in the request body add: 
```bash
{
  "name": "Tom",
  "contact_number": "0826541287"
}
```

Output:
- patient name
- patient contact number
- patient id
- detail of appointments assoicated, if any.
eg:
```bash
{
  "name": "Tom",
  "contact_number": "0826541287",
  "id": 1,
  "appointments": []
}
```

#### [To view all patients](http://localhost:8080/patients/):
Input:
- skip (default value 0)
- limit (default value 100)
    Note: this will return the first 100 patients if the default values are used.
Output:
- List of all patients in the system, in the same format as the output from creating a patient

#### [To view a specific patient](http://localhost:8080/patient/1):
Input:
- The patient ID of the patient you want to view (this can be accessed by putting their ID at http://localhost:8080/patient/{id} )

Output:
- Information of the specific patient that you requested

### [To create an appointment](http://localhost:8080/appointment/):
Input:
- patient ID
- lenght of appointment in minutes
- Date of the appointments (YYYY/MM/DD) 
- Time (HH:MM)
    Note: appointments cannot overlap.
eg: in the request body add: 
```bash
{
  "appt_length": 30,
  "yyyy_mm_dd": "2021/05/21",
  "time": "12:00"
}
```

Output:
- Appointment length
- Appointment ID
- patient id
- Appointment date and time.
eg:
```bash
{
  "appt_length": 30,
  "id": 3,
  "patient_id": 1,
  "appt_time": "2021-05-21 12:00:00"
}
```

### [To view all appointments](http://localhost:8080/patients/):
Input:
- skip (default value 0)
- limit (default value 100)

Output:
- List of all appointments in the system


### [To view all appointments for a specific patient](http://localhost:8080/patients/1/appointments):
Input:
- Patient ID (can be obtained from read all patients)
    Note: this can be accessed by putting their ID in {id} at http://localhost:8080/patient/{id}/appointments

Output:
- List of all appointments for a patient in the systems


#### [To delete a specific patient](http://localhost:8080/patient/1):
Input:
- The patient ID of the patient you want to delete (this can be accessed by putting their ID at http://localhost:8080/patient/{id} )

Output:
- Confirmation message that the patient has been deleted

#### [To delete a specific appointment](http://localhost:8080/appointment/1):
Input:
- The appointment ID of the appointent you want to delete (this can be accessed by putting their ID at http://localhost:8080/patient/{id} )

Output:
- Confirmation message that the appointment has been deleted

#### [To delete all appointments for a specific patient](http://localhost:8080/patient/1/delete):
Input:
- The patient ID of the patient whose appointments you want to delete (this can be accessed by putting their ID at {id} in http://localhost:8080/patient/{id}/delete )

Output:
- Confirmation message that their appointment have been deleted

#### [To update a patients information](http://localhost:8080/patient/1/update):
Note: any details you don't wish to change should just be input as they currently exist.

Input:
- patients ID (this can be accessed by putting their ID at {id} in http://localhost:8080/patient/{id}/update
- patients name  
- patients contact number 

Output:
- updated patient name
- updated patient contact number
- patient id
- detail of appointments assoicated, if any.

#### [To update an appointment's details](http://localhost:8080/appointment/1/update):
Note: any details you don't wish to change should just be input as they currently exist.

Input:
- appointment ID (this can be accessed by putting the appointment ID at {id} in http://localhost:8080/appointment/{id}/delete 
- patients ID 
- appointment lenght
- date of appointment
- time of appointment

Output:
- updated appointment length
- appointment ID
- updated patient id
- updated appointment date and time 


