from typing import List, Dict
from bpmn_elements import *

# Define the namespaces
namespaces = {
    'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
    'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
    'dc': 'http://www.omg.org/spec/DD/20100524/DC',
    'di': 'http://www.omg.org/spec/DD/20100524/DI',
    'bioc': 'http://bpmn.io/schema/bpmn/biocolor/1.0',
    'modeler': 'http://camunda.org/schema/modeler/1.0'
}


def find_all(xml_string,
             search_element):
    xml_return_string = xml_string.findall(search_element, namespaces)
    return xml_return_string


def find(xml_string,
         search_element):
    xml_return_string = xml_string.find(search_element, namespaces)
    return xml_return_string


def get_text(xml_string, search_element):
    return xml_string.find(search_element, namespaces).text


# Find all text annotations
def get_text_annotations(xml_string, search_elements) -> Dict[str, TextAnnotation]:
    text_annotations: Dict[str, TextAnnotation] = {}
    for search_element in search_elements:
        for text_annotation in find_all(xml_string=xml_string, search_element=search_element):
            text_annotation_text = get_text(xml_string=text_annotation, search_element='bpmn:text')
            current_text_annotation = TextAnnotation(text_annotation.get('id'), text_annotation_text)
            text_annotations[current_text_annotation.id] = current_text_annotation
    return text_annotations


# find all Fundamental Requirement Data Objects
def get_data_objects(xml_string, search_element) -> Dict[str, DataObject]:
    data_objects: Dict[str, DataObject] = {}
    frs = ["BI", "FR1", "FR2", "FR3", "FR4", "FR5", "FR6", "FR7"]
    for data_object_reference in find_all(xml_string, search_element):
        if data_object_reference.get('name') in frs:
            data_objects[data_object_reference.get('id')] = DataObject(data_object_reference.get('id'),
                                                                       data_object_reference.get('name'))
    return data_objects


# Connect data object with text annotations
def add_text_annotations_to_requirements(xml_string,
                                         search_elements,
                                         data_objects: Dict[str, DataObject],
                                         text_annotations: Dict[str, TextAnnotation]):

    for search_element in search_elements:
        for data_association in find_all(xml_string, search_element):
            source_ref = data_association.get('sourceRef')
            target_ref = data_association.get('targetRef')

            if source_ref in data_objects:
                data_objects[source_ref].add_text_annotation(text_annotations[target_ref].text)

            if target_ref in data_objects:
                data_objects[target_ref].add_text_annotation(text_annotations[source_ref].text)
    return data_objects


def get_events(process, data_objects):
    events: Dict[str, Event] = {}
    intermediate_throw_events = process.findall('bpmn:intermediateThrowEvent', namespaces)
    for intermediate_throw_event in intermediate_throw_events:

        event_id = intermediate_throw_event.get('id')
        events[event_id] = Event(id=event_id)

        data_input_associations = intermediate_throw_event.findall('bpmn:dataInputAssociation', namespaces)
        for data_input_association in data_input_associations:
            data_object_reference = get_text(xml_string=data_input_association, search_element='bpmn:sourceRef')
            current_data_object = data_objects[data_object_reference]
            events[event_id].add_requirement(current_data_object)
            del data_objects[data_object_reference]
    return events


def get_tasks(process, data_objects):
    possible_tasks = ['bpmn:task', 'bpmn:scriptTask', "bpmn:userTask"]
    tasks: Dict[str, Task] = {}
    for possible_task in possible_tasks:
        xml_current_tasks = process.findall(possible_task, namespaces)
        for xml_current_task in xml_current_tasks:
            task_id = xml_current_task.get('id')
            tasks[task_id] = Task(id=task_id, name=xml_current_task.get('name'))

            xml_data_input_associations = xml_current_task.findall('bpmn:dataInputAssociation', namespaces)
            for xml_data_input_association in xml_data_input_associations:
                data_object_reference = get_text(xml_data_input_association, 'bpmn:sourceRef')
                current_data_object = data_objects[data_object_reference]
                tasks[task_id].add_requirement(current_data_object)
                # TODO Check if this is working
                del data_objects[data_object_reference]
    return tasks


def add_events_to_lane(xml, lane, events):
    for flowNodeRef in xml.findall('bpmn:flowNodeRef', namespaces):
        if flowNodeRef.text in events:
            lane.add_element(events[flowNodeRef.text])


def add_tasks_to_lane(xml, lane, tasks):
    for flowNodeRef in xml.findall('bpmn:flowNodeRef', namespaces):
        if flowNodeRef.text in tasks:
            lane.add_element(tasks[flowNodeRef.text])


def get_pools(xml_string, search_element) -> Dict[str, Pool]:
    pools: Dict[str, Pool] = {}
    for participant in find_all(xml_string, search_element):
        current_pool = Pool(id=participant.attrib['id'],
                            name=participant.attrib.get('name', ''),
                            process_ref=participant.attrib['processRef'])
        pools[participant.attrib['processRef']] = current_pool

    return pools


def get_coordinates(bpmndi_element) -> Coordinate:
    bounds = find(xml_string=bpmndi_element, search_element='dc:Bounds')
    current_coordinate = Coordinate(
                x=bounds.get("x"),
                y=bounds.get("y"),
                width=bounds.get("width"),
                height=bounds.get("height"))
    return current_coordinate


def get_data_objects_with_coordinates(xml_string, search_element, data_objects):
    data_object_with_coordinates: Dict[str, Coordinate] = {}
    for data_object in data_objects:
        bpmndi_elements = find_all(xml_string=xml_string, search_element=search_element)
        for bpmndi_element in bpmndi_elements:
            if bpmndi_element.get("bpmnElement") == data_object:
                data_object_with_coordinates[bpmndi_element.get("bpmnElement")] = get_coordinates(bpmndi_element)
    return data_object_with_coordinates


def get_lane_coordinates(xml_string, search_element, lane_id):
    bpmndi_elements = find_all(xml_string=xml_string, search_element=search_element)
    for bpmndi_element in bpmndi_elements:
        if bpmndi_element.get("bpmnElement") == lane_id:
            current_coordinates = get_coordinates(bpmndi_element)
            return current_coordinates


def add_requirements_to_lane(xml_string, search_element, lane, data_object_with_coordinates, data_objects):
    lane_coordinates = get_lane_coordinates(xml_string, search_element,lane.id)
    for key, coord in data_object_with_coordinates.items():
        if (coord.x > lane_coordinates.x
                and coord.x_end < lane_coordinates.x_end
                and coord.y > lane_coordinates.y
                and coord.y_end < lane_coordinates.y_end):
            lane.add_requirement(data_objects[key])
            # print(f'Adding: {data_objects[key].name} to {lane.name}')