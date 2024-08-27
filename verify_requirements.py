import re
from typing import List


def check_pattern(requirement):

    mixed_pattern = re.compile(
        r'^\s*\w+\s*:'
        r'\s*([\w.:]+|'
        r'\[\s*([\w.:]+\s*,\s*)*[\w.:]+\s*\])\s*$'
    )
    if not mixed_pattern.match(requirement):
        print("Requirement did not match mixed_pattern")
        print("Requirement: ", requirement)
        print("Pattern: ", mixed_pattern.pattern)

        # Detailed Debugging
        if not re.match(r'^\s*\w+\s*:', requirement):
            print("Failed at variable name and colon")
        else:
            print("Passed variable name and colon")

        if not re.search(r':\s*[\w.]+\s*$', requirement) and not re.search(r':\s*\[\s*([\w.]+\s*,\s*)*[\w.]+\s*\]\s*$',
                                                                        requirement):
            print("Failed at value or list of values")
        else:
            print("Passed value or list of values")
        return False
    return True


def check_requirement_validity(requirement_text):

    requirements = requirement_text.split(";")

    # remove empty strings in list.
    requirements = list(filter(lambda x: len(x) > 0, requirements))
    # print(f'Requirements: {requirements}')

    for requirement in requirements:
        requirement_text = requirement.strip()
        # print(f'Requirement: {requirement_text}')
        if not check_pattern(requirement_text):
            return False

    return True


def check_participant_requirements(participant) -> List:
    check_errors: List = []
    for requirement_source in [participant.events, participant.tasks, [participant]]:
        for item in requirement_source:
            requirements = item.get_requirements()
            for requirement in requirements:
                text_annotation = requirement.get_text_annotation()
                if not check_requirement_validity(text_annotation):
                    check_errors.append(text_annotation)
    return check_errors


def process_lane(lane):
    print(f'Lane: {lane.name}')
    check_participant_requirements(participant=lane)


def verify_requirements(pools) -> bool:

    for pool in pools.values():
        lanes = pool.lanes if pool.has_lanes() else [pool]
        for lane in lanes:
            sub_lanes = lane.lanes if lane.has_lanes() else [lane]
            for sub_lane in sub_lanes:
                error_messages = check_participant_requirements(sub_lane)
                if len(error_messages) > 0:
                    return False

    return True
