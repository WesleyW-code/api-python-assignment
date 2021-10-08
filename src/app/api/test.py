import datetime

all_appointments = [
  {
    "appt_length": 40,
    "id": 1,
    "patient_id": 1,
    "appt_time": "2021-08-22 11:00:00"
  }

]

my_appointment = {
    "appt_length": 5,
    "id": 1,
    "patient_id": 1,
    "appt_time": "2021-08-22 11:30:00"
  }
my_time = datetime.datetime.strptime(my_appointment['appt_time'],'%Y-%m-%d %H:%M:%S')

check = True

print(my_appointment["appt_time"])


for appt in all_appointments:
    to_check = appt["appt_time"]
    their_time = datetime.datetime.strptime(to_check,'%Y-%m-%d %H:%M:%S')
    difference = my_time - their_time
    difference = difference.total_seconds()
    mins = difference/60
    print(mins)
    if mins < appt["appt_length"] and mins > 0:
        check=False
        print("first")
    if mins > -my_appointment["appt_length"] and mins < 0:
        check=False
        print("second")