import recodex_interface as rex
import unicodedata
from functools import reduce


# Convert UTF-8 string to plain ascii trying to map characters to their neares approximates
def _asciiize_string(str):
    return unicodedata.normalize('NFKD', str).encode('ascii', 'ignore').decode('utf-8')


# Parse token from note and return internal representation of points (None, 0, 1, or 2)
def _parse_points(token):
    try:
        i = int(token)
        if i >= 0 and i <= 2:
            return i
        return None
    except ValueError:
        return None


# One student of adjacent group and his/her points for selected shadow assignment
class Student:
    def __init__(self, student, assignment, dates):
        self.user_id = student["id"]
        self.first_name = student["name"]["firstName"]
        self.last_name = student["name"]["lastName"]
        self.assignment_id = assignment["id"]

        # Gather points and parse the note
        points = list(filter(lambda p: p["awardeeId"] == self.user_id, assignment["points"]))
        if len(points) > 0:
            points = points[0]
            self.points = list(map(_parse_points, points["note"].split(";")))
            self.points_id = points["id"]
            if (self.total_points() != int(points["points"])):
                raise Exception("Total points sum does not match detailed record in note fo user {} {}.".format(self.first_name, self.last_name))
        else:
            self.points = []
            self.points_id = None

        # Make sure the list has at least as many values as there are dates
        while (len(self.points) < len(dates)):
            self.points.append(None)

    # Compute the points total from attendance records
    def total_points(self):
        return reduce(lambda x, y: x + y, filter(lambda x: x, self.points))

    # Internal function that re-assembles note for saving
    def _assemble_note(self):
        return ";".join(map(lambda p: '_' if p is None else str(p), self.points))

    # Bool value whether the student was present at given lecture
    def present(self, lectureIdx):
        return self.points[lectureIdx] is not None

    # Return the bonus value for given lecture as a string
    def bonus(self, lectureIdx):
        if (self.present(lectureIdx)):
            return ['-1', '', '+1'][self.points[lectureIdx]]
        else:
            return ''

    # Set attendance values (presence and bonus) for particular lecture
    def set_attendance(self, idx, present, bonus):
        if present is False:
            self.points[idx] = None
        else:
            if bonus == '':
                self.points[idx] = 1
            else:
                self.points[idx] = 1 + int(bonus)

    # Save the user data using low-level ReCodEx-CLI calls
    def save(self):
        has_any = len(list(filter(lambda x: x is not None, self.points))) > 0
        if self.points_id is None:
            if has_any:
                rex.create_shadow_assignment_points(self.assignment_id, self.user_id, str(self.total_points()), self._assemble_note())
        else:
            if has_any:
                rex.update_shadow_assignment_points(self.points_id, str(self.total_points()), self._assemble_note())
            else:
                rex.delete_shadow_assignment_points(self.points_id)


# Load given assignment, get its group_id, and load students of that group
# Students are returned as a list of Student objects sorted by name
def load_students(assignment_id, dates):
    print("Loading shadow assignment {} ...".format(assignment_id))
    assignment = rex.get_shadow_assignment(assignment_id)

    group_id = assignment['groupId']
    print("Loading students of group {} ...".format(group_id))
    students = [Student(s, assignment, dates) for s in rex.get_students(group_id)]

    return sorted(students, key=lambda s: (_asciiize_string(s.last_name), _asciiize_string(s.first_name)))
