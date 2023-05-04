"""Define utilities used in test."""


def compare_dict(dict1, dict2):
    """Compare two dictionaries.

    This function checks that two objects that contain similar keys
    have the same value

    """
    dict1_keys = set(dict1)
    dict2_keys = set(dict2)
    intersect = dict1_keys.intersection(dict2_keys)

    if not intersect:
        return False

    for key in intersect:
        if dict1[key] != dict2[key]:
            return False
    return True


def make_transitions(obj, transitions, note={}):
    """Change state of organisation."""
    for each in transitions:
        obj.workflow_state = each
        obj.transition(note)
    return obj
