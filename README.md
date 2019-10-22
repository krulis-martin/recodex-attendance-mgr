# Attendance Manager for ReCodEx

A GUI tool for easier management of student attendance within a single shadow assignment of [ReCodEx](https://github.com/ReCodEx) system.

The objective is to collect attendance records for students in labs. The records are encoded into a single shadow assignment in ReCodEx. The assigned points represent the sum of points for the whole attendance. Individual records are encoded into `note` property of the shadow assignment. Individual records are encoded as tokens separated by `;`. Tokens have the following meaning:

* `_` -- absence
* `1` -- regular attendance (i.e. +1 point)
* `0` -- present, but not responding (i.e., +1 point -1 penalty = 0 points)
* `2` -- present and bonus for activity (+1 point +1 bonus = 2 points total)


## Requirements
- Python 3.6+
- See `requirements.txt`

## Deployment
1. clone the repository
2. install dependencies using `pip install -r requirements.txt` in the root 
   directory of the repository

Note that `tkinter` Python package is required, but this should be part of your Python installation already.

## Usage

1. You need to log in via [ReCodEx-CLI](https://github.com/ReCodEx/cli).
2. Set up a configuration file. It is pretty simple, you need to write in a UUID of shadow assignment in ReCodEx that will collect the points and a list of dates where the lectures/seminars occurred.
3. Execute the app `python ./attendance_mgr.py ./your-config.yaml`

That's it!

The GUI will appear allow you to modify the attendance records. `Cancel` button will terminate the application, `OK` button will save the records and then terminate.
