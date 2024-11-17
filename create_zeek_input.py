import csv

ips = {"Heating oven":"192.168.10.12", "Process control system":"192.168.1.10"}

# communications
# fields id sender_ip sender_port receiver_ip receiver_port attribute1 attribute2
communications = {}

def getBI(participant):
    name = participant.name
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

def save_comms(participant, name, pool):
    # Extract Basic Information
    base_information = getBI(participant)
    print(base_information)
    pool = pool
    sender = base_information["IP"]

    for event in participant.events:
        event_id = event.id
        receiver_name = event.receiver_name
    #    print("RECEIVER NAME")
   #     print(receiver_name)
        receiver_bi = ""
       # event.add_event_infos(sender,receiver)
        for parti in pool:
          #  print('Other Participants')
          #  print(parti.name)
            if parti.name == receiver_name:
                receiver_bi = getBI(parti)
                print("RECEIVER BI:")
                print(receiver_bi)
        receiver = receiver_bi["IP"]
        #receiver = ""
        requirements = []
        requirements_list = event.get_requirements()
        receiver_BI = getBI(participant)
       # print("Event Data")
        #print(event_id)
        port = ""
        for requirement in requirements_list:
            text_annotation = requirement.get_text_annotation()
            splitted = text_annotation.splitlines()
            print(splitted)
            if len(splitted) >= 1:
                for req in splitted:
                    if "port" in req:
                        print("POOOOORT")

                        port = req.split(" ")[1]
                    else:
                        requirements.append(req)


        communications[event_id] = {"sender_ip": sender, "sender_port": port, "receiver_ip": receiver, "receiver_port": port,
                                    "requirements": requirements}
        print(communications)

def save_into_file():
    data = [['sender','sender_p','receiver', 'receiver_p', 'protocol','requirements']]
    for com in communications:
        row = []
        row.append(communications[com]["sender_ip"])
        row.append(communications[com]["sender_port"])
        row.append(communications[com]["receiver_ip"])
        row.append(communications[com]["receiver_port"])
        for req in communications[com]['requirements']:
            if "protocol" in req.split(" ")[0]:
                print(req.split(" ")[1][:-1])
                row.append(req.split(" ")[1][:-1])

        row.append(communications[com]["requirements"])
        data.append(row)
    with open("zeek_input.tsv", 'w', newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(data)

def extract_communications(pools):
    for pool in pools.values():
        if pool.has_lanes():
            for lane in pool.lanes:
             #   print(lane)
                if lane.has_lanes():
                    for sub_lane in lane.lanes:
                        save_comms(participant=sub_lane, name=sub_lane.name ,pool=lane.lanes)
                else:
                  #  print(f'Lane: {lane.name}')
                    save_comms(participant=lane, name=lane.name, pool = pool.lanes)

        else:
            #print(f'Lane: {pool.name}')
            save_comms(participant=pool, name=pool.name, pool=pools.values())
                #
    save_into_file()              # sub:lane = name
