from ruamel import yaml
import sys
from students import load_students
import PySimpleGUI as sg


# Load configuration
def init(cfgFile):
    with open(cfgFile, "r") as fp:
        config = yaml.safe_load(fp)
    assignment_id = config["assignments"][0]  # In the future, there might be a select box displayed
    students = load_students(assignment_id, config["dates"])

    return (students, config["dates"])


# Create header layout (dates)
def create_header(dates):
    res = [sg.Text("", size=(20, 1))]
    for date in dates:
        res.append(sg.Text(date, size=(11, 1)))
    return res


# Create one row of the layout (students data)
def create_layout_student_row(student, dates):
    res = [sg.Text("{} {}".format(student.first_name, student.last_name), size=(20, 1))]
    for i in range(0, len(dates)):
        res.append(sg.Checkbox("",
                   key="|".join(["checkbox", student.user_id, str(i)]),
                   enable_events=True,
                   default=student.present(i),
                   size=(0, 0),
                   pad=(0, 0)))
        res.append(sg.OptionMenu(["", "-1", "+1"],
                   key="|".join(["select", student.user_id, str(i)]),
                   disabled=not student.present(i),
                   default_value=student.bonus(i),
                   size=(2, 1),
                   pad=((0, 20), (0, 0))))
    return res


# Create complete window layout
def create_layout(students, dates):
    return [create_header(dates)] +\
        list(map(lambda s: create_layout_student_row(s, dates), students)) +\
        [[sg.OK(), sg.Cancel()]]


# Save form data into the students objects and then trigger ReCodEx updates
def save(students, dates, values):
    for student in students:
        print("Saving student {} {} ...".format(student.first_name, student.last_name))
        for i in range(0, len(dates)):
            checkbox_key = "|".join(["checkbox", student.user_id, str(i)])
            select_key = "|".join(["select", student.user_id, str(i)])
            student.set_attendance(i, values[checkbox_key], values[select_key])

        student.save()


# Main Script

if len(sys.argv) != 2:
    print("One argument expected -- path to a Yaml config file.")
    sys.exit()

configFile = sys.argv[1]
(students, dates) = init(configFile)

# Create the Main Window
window = sg.Window("Update attendance by {}".format(configFile), create_layout(students, dates))

# Event Loop to process "events"
while True:
    event, values = window.Read()

    # Terminate without saving
    if event in (None, "Cancel"):
        break

    # Save and terminate
    if event == 'OK':
        save(students, dates, values)
        break

    # Toggle disabled menu options
    ev_type, user_id, idx = event.split("|")
    if ev_type == "checkbox":
        select_key = "|".join(["select", user_id, idx])
        window[select_key].Update(disabled=not values[event])

window.Close()
