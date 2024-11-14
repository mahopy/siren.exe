

ips = {"Heating oven":"192.168.10.12", "Process control system":"192.168.1.10"}

# communications
# fields id sender_ip sender_port receiver_ip receiver_port attribute1 attribute2
communications = {}

def getBI(participant):
    information = participant.get_requirements()
    base_information = {}
    for req in information:
        if req.name == 'BI':
            print("Found BI")
            string_value_base = req

            string_value_base = string_value_base.get_text_annotation()
            base_information_list = string_value_base.split(";\n")
            for element in base_information_list:
                key, sep, value = element.partition(":")
                base_information[key] = value
    # print(base_information)
    return base_information

def save_comms(participant, name):
    # Extract Basic Information
    base_information = getBI(participant)
    print(base_information)
    sender = base_information["IP"]
    receiver = base_information[]
    for event in participant.events:
        event_id = event.id
        requirements = []
        requirements_list = event.get_requirements()

        print("Event Data")
        for requirement in requirements_list:
            text_annotation = requirement.get_text_annotation()
            requirements.append(text_annotation)
        communications[event_id] = {"sender_ip": "", "sender_port": "", "receiver_ip": " ", "receiver_port": " ",
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
