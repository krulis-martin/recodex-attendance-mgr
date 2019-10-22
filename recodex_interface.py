from ruamel import yaml
import sys
import subprocess


# Low level functions for calling ReCodEx CLI process

def _recodex_call(args):
    res = subprocess.run(['recodex'] + args, capture_output=True)
    if res.returncode == 0:
        return res.stdout
    else:
        sys.stderr.write("Error calling recodex CLI:\n")
        sys.stderr.buffer.write(res.stderr)
        return None


# Get all students of given group
def get_students(group_id):
    payload = _recodex_call(['groups', 'students', group_id, '--yaml'])
    if payload is None:
        raise Exception("Error reading students of group.")
    return yaml.safe_load(payload)


# Get details and points of given shadow assignment
def get_shadow_assignment(assignment_id):
    payload = _recodex_call(['shadow_assignments', 'get', assignment_id, '--yaml'])
    if payload is None:
        raise Exception("Error reading shadow assignment.")
    return yaml.safe_load(payload)


def create_shadow_assignment_points(assignment_id, user_id, points, note):
    res = _recodex_call(['shadow_assignments', 'create-points', assignment_id, user_id, points, note])
    return False if res is None else True


def update_shadow_assignment_points(points_id, points, note):
    res = _recodex_call(['shadow_assignments', 'update-points', points_id, points, note])
    return False if res is None else True


def delete_shadow_assignment_points(points_id):
    res = _recodex_call(['shadow_assignments', 'delete-points', points_id])
    return False if res is None else True
