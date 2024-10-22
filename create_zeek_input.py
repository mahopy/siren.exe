

ips = {"Heating oven":"192.168.10.12", "Process control system":"192.168.1.10"}

# communications
# fields id sender_ip sender_port receiver_ip receiver_port attribute1 attribute2
communications = {}
def save_comms(participant, name):
    for event in participant.events:
        event_id = event.id
        requirements = []
        requirements_list = event.get_requirements()
        print(requirements_list)
        frs = ['FR1', "FR2", "FR3", "FR4", "FR5", "FR6", "FR7"]
        for category in participant.get_requirements():
            if category.name in frs:
                print(f'Lane Requirement: {category.get_text_annotation()}')
            else:
                print(f'Basic Information: {category.get_text_annotation()}')
        for requirement in requirements_list:
            text_annotation = requirement.get_text_annotation()
            requirements.append(text_annotation)
        communications[event_id] = {"sender_ip": " ", "sender_port": " ", "receiver_ip": " ", "receiver_port": " ",
                                    "requirements": requirements}
        print(communications)

def extract_communications(pools):
    for pool in pools.values():
        if pool.has_lanes():
            for lane in pool.lanes:
             #   print(lane)
                if lane.has_lanes():
                    for sub_lane in lane.lanes:
                        save_comms(participant=sub_lane, name=sub_lane.name)

                else:
                  #  print(f'Lane: {lane.name}')
                    save_comms(participant=lane, name=lane.name)

        else:
            #print(f'Lane: {pool.name}')
            save_comms(participant=pool, name=pool.name)
                #
                        # sub:lane = name
