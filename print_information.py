def print_events_of_participant(participant):
    for event in participant.events:
        requirements = event.get_requirements()

        for requirement in requirements:
            text_annotation = requirement.get_text_annotation()
            print(f'Event id: {event.id}, Event Name: {text_annotation}')


def print_tasks_of_participant(participant):
    for task in participant.tasks:
        requirements = task.get_requirements()

        for requirement in requirements:
            text_annotation = requirement.get_text_annotation()
            print(f'Task: "{task.name}" Requirement: "{text_annotation}"')


def print_requirements_of_participant(participant):
    frs = ['FR1', "FR2", "FR3", "FR4", "FR5", "FR6", "FR7"]
    for requirement in participant.get_requirements():
        if requirement.name in frs:
            print(f'Lane Requirement: {requirement.get_text_annotation()}')
        else:
            print(f'Basic Information: {requirement.get_text_annotation()}')


def print_all_information(pools):
    for pool in pools.values():
        if pool.has_lanes():
            for lane in pool.lanes:
                if lane.has_lanes():
                    for sub_lane in lane.lanes:
                        print(f'Lane: {sub_lane.name}')
                        print_events_of_participant(participant=sub_lane)
                        print_tasks_of_participant(participant=sub_lane)
                        print_requirements_of_participant(participant=sub_lane)

                else:
                    print(f'Lane: {lane.name}')
                    print_events_of_participant(participant=lane)
                    print_tasks_of_participant(participant=lane)
                    print_requirements_of_participant(participant=lane)

        else:
            print(f'Lane: {pool.name}')
            print_events_of_participant(participant=pool)
            print_tasks_of_participant(participant=pool)
            print_requirements_of_participant(participant=pool)
