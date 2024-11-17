# import xml.etree.ElementTree as ET
# from typing import List, Dict
# import pprint
# from bpmn_elements import *
# import tkinter as tk
# from tkinter import filedialog
# from gather_information import (get_text_annotations,
#                                 get_data_objects,
#                                 add_text_annotations_to_requirements,
#                                 get_pools,
#                                 find_all,
#                                 get_events,
#                                 get_tasks,
#                                 add_events_to_lane,
#                                 add_tasks_to_lane,
#                                 get_data_objects_with_coordinates,
#                                 add_requirements_to_lane)
# from verify_requirements import verify_requirements
# from print_information import print_all_information
#
#
# def init_requirement_finder():
#     file_path = open_file_dialog()
#     root = get_xml(file_path)
#     return root
#
# def open_file_dialog():
#     # Open a file dialog and allow the user to select an XML file
#     file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml;*.bpmn")])
#
#     return file_path
#
#
# def get_xml(file_path):
#     # Parse the XML file
#     tree = ET.parse(file_path)
#     root = tree.getroot()
#     return root
#
#
# def add_requirements_to_events_and_tasks(root):
#     for process in find_all(xml_string=root, search_element='bpmn:process'):
#         pool_id = process.get('id')
#         current_pool = pools[pool_id]
#
#         events: Dict[str, Event] = get_events(process, data_objects=data_objects)
#         tasks: Dict[str, Task] = get_tasks(process, data_objects=data_objects)
#
#         lane_sets = find_all(xml_string=process, search_element='bpmn:laneSet')
#         if lane_sets:
#             for lane_set in lane_sets:
#                 lanes = find_all(xml_string=lane_set, search_element='bpmn:lane')
#
#                 for lane in lanes:
#                     current_lane = Lane(id=lane.get('id'), name=lane.get('name'))
#                     current_pool.add_lane(current_lane)
#
#                     child_lanes_sets = find_all(xml_string=lane, search_element='bpmn:childLaneSet')
#                     if child_lanes_sets:  # Lane with child lane
#                         for child_lane_set in child_lanes_sets:
#                             child_lanes = find_all(child_lane_set, 'bpmn:lane')
#                             for child_lane in child_lanes:
#                                 current_child_lane = Lane(id=child_lane.get('id'), name=child_lane.get('name'))
#                                 current_lane.add_lane(current_child_lane)
#
#                                 add_events_to_lane(xml=child_lane, lane=current_child_lane, events=events)
#                                 add_tasks_to_lane(xml=child_lane, lane=current_child_lane, tasks=tasks)
#
#                     else:  # Lane without child lane
#                         add_events_to_lane(xml=lane, lane=current_lane, events=events)
#                         add_tasks_to_lane(xml=lane, lane=current_lane, tasks=tasks)
#
#         else:  # Plain pool without lanes
#             for key, event in events.items():
#                 current_pool.add_element(event)
#
#             for key, task in tasks.items():
#                 current_pool.add_element(task)
#
#
# def add_requirements_to_lanes(root):
#     for pool in pools.values():
#         if pool.has_lanes():
#             for lane in pool.lanes:
#                 if lane.has_lanes():
#                     for sub_lane in lane.lanes:
#                         add_requirements_to_lane(xml_string=root,
#                                                  search_element="bpmndi:BPMNDiagram/bpmndi:BPMNPlane/bpmndi:BPMNShape",
#                                                  lane=sub_lane,
#                                                  data_object_with_coordinates=data_object_with_coordinates,
#                                                  data_objects=data_objects)
#                 else:
#                     add_requirements_to_lane(xml_string=root,
#                                              search_element="bpmndi:BPMNDiagram/bpmndi:BPMNPlane/bpmndi:BPMNShape",
#                                              lane=lane,
#                                              data_object_with_coordinates=data_object_with_coordinates,
#                                              data_objects=data_objects)
#         else:
#             add_requirements_to_lane(xml_string=root,
#                                      search_element="bpmndi:BPMNDiagram/bpmndi:BPMNPlane/bpmndi:BPMNShape",
#                                      lane=pool,
#                                      data_object_with_coordinates=data_object_with_coordinates,
#                                      data_objects=data_objects)
#
#
#
# def find_annotations(root):
#     text_annotation_elements = ['bpmn:collaboration/bpmn:textAnnotation', 'bpmn:process/bpmn:textAnnotation']
#     annotations = get_text_annotations(xml_string=root, search_elements=text_annotation_elements)
#
#     return annotations
#
#
# def find_data_objects(root):
#     data_objects = get_data_objects(xml_string=root,
#                                     search_element="bpmn:process/bpmn:dataObjectReference")
#     return data_objects
#
#
# def add_annotations_to_data_objects(root, data_objects, annotations):
#     search_elements = ["bpmn:collaboration/bpmn:association", "bpmn:process/bpmn:association"]
#     data_objects = add_text_annotations_to_requirements(xml_string=root,
#                                                         search_elements=search_elements,
#                                                         data_objects=data_objects,
#                                                         text_annotations=annotations)
#
#     return data_objects
#
#
# def find_pools(root):
#     pools: Dict[str, Pool] = get_pools(xml_string=root,
#                                        search_element='bpmn:collaboration/bpmn:participant')
#     return pools
#
#
# file_path = open_file_dialog()
#
# root = get_xml(file_path)
#
# text_annotations = find_annotations(root)
#
# data_objects = find_data_objects(root)
#
# pools = find_pools(root)
#
# data_objects = add_annotations_to_data_objects(root=root, data_objects=data_objects, annotations=text_annotations)
#
#
# # # in the first step, we connect requirements of tasks and events, because they have a modelled connection,
# # # which can be found in the XML
# add_requirements_to_events_and_tasks(root=root)
#
# # # after all requirements that are connected with a task or an event are processed, in the list of data_objects
# # # only the requirements remain, that are not connected with a task or event, which means they are requirements of
# # # lanes. These are now connected with their lanes by their coordinates.
# data_object_with_coordinates: Dict[str, Coordinate] = (
#     get_data_objects_with_coordinates(xml_string=root,
#                                       search_element="bpmndi:BPMNDiagram/bpmndi:BPMNPlane/bpmndi:BPMNShape",
#                                       data_objects=data_objects))
#
# add_requirements_to_lanes(root)
#
# valid_requirements = verify_requirements(pools)
#
# if valid_requirements:
#     print_all_information(pools)
import xml.etree.ElementTree as ET
from typing import List, Dict
import pprint
import tkinter as tk
from tkinter import filedialog

from bpmn_elements import *
from gather_information import (
    get_text_annotations,
    get_data_objects,
    add_text_annotations_to_requirements,
    get_pools,
    find_all,
    get_events,
    get_tasks,
    add_events_to_lane,
    add_tasks_to_lane,
    get_data_objects_with_coordinates,
    add_requirements_to_lane,
)
from verify_requirements import verify_requirements
from print_information import print_all_information
from create_zeek_input import extract_communications

file_string = ""

def open_file_dialog() -> str:
    """Open a file dialog and allow the user to select an XML file."""
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml;*.bpmn")])
    return file_path


def get_xml(file_path: str) -> ET.Element:
    """Parse the XML file and return the root element."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root


def find_annotations(root: ET.Element) -> List[Dict]:
    """Find text annotations in the BPMN XML."""
    text_annotation_elements = ['bpmn:collaboration/bpmn:textAnnotation', 'bpmn:process/bpmn:textAnnotation']
    annotations = get_text_annotations(xml_string=root, search_elements=text_annotation_elements)
    return annotations


def find_data_objects(root: ET.Element) -> Dict[str, Dict]:
    """Find data objects in the BPMN XML."""
    data_objects = get_data_objects(xml_string=root, search_element="bpmn:process/bpmn:dataObjectReference")
    return data_objects


def find_pools(root: ET.Element) -> Dict[str, Pool]:
    """Find pools in the BPMN XML."""
    pools = get_pools(xml_string=root, search_element='bpmn:collaboration/bpmn:participant')
    return pools


def add_annotations_to_data_objects(root: ET.Element, data_objects: Dict, annotations: List[Dict]) -> Dict:
    """Add text annotations to data objects."""
    search_elements = ["bpmn:collaboration/bpmn:association", "bpmn:process/bpmn:association"]
    updated_data_objects = add_text_annotations_to_requirements(
        xml_string=root,
        search_elements=search_elements,
        data_objects=data_objects,
        text_annotations=annotations
    )
    return updated_data_objects


def add_requirements_to_events_and_tasks(root: ET.Element, pools: Dict[str, Pool], data_objects: Dict):
    """Add requirements (data_objects) to events and tasks."""
    for process in find_all(xml_string=root, search_element='bpmn:process'):
        pool_id = process.get('id')
        current_pool = pools[pool_id]

        events: Dict[str, Event] = get_events(process,root, data_objects=data_objects)
        tasks: Dict[str, Task] = get_tasks(process, data_objects=data_objects)

        lane_sets = find_all(xml_string=process, search_element='bpmn:laneSet')
        if lane_sets:
            for lane_set in lane_sets:
                lanes = find_all(xml_string=lane_set, search_element='bpmn:lane')
                for lane in lanes:
                    current_lane = Lane(id=lane.get('id'), name=lane.get('name'))
                    current_pool.add_lane(current_lane)

                    child_lane_sets = find_all(xml_string=lane, search_element='bpmn:childLaneSet')
                    if child_lane_sets:  # Lane with child lanes
                        for child_lane_set in child_lane_sets:
                            child_lanes = find_all(child_lane_set, 'bpmn:lane')
                            for child_lane in child_lanes:
                                current_child_lane = Lane(id=child_lane.get('id'), name=child_lane.get('name'))
                                current_lane.add_lane(current_child_lane)

                                add_events_to_lane(xml=child_lane, lane=current_child_lane, events=events)
                                add_tasks_to_lane(xml=child_lane, lane=current_child_lane, tasks=tasks)
                    else:  # Lane without child lanes
                        add_events_to_lane(xml=lane, lane=current_lane, events=events)
                        add_tasks_to_lane(xml=lane, lane=current_lane, tasks=tasks)
        else:  # Plain pool without lanes
            for event in events.values():
                current_pool.add_element(event)
            for task in tasks.values():
                current_pool.add_element(task)


def add_requirements_to_resources(root: ET.Element, pools: Dict[str, Pool], data_object_with_coordinates: Dict[str, Coordinate], data_objects: Dict):
    """Add requirements (data_objects) to resources (Pools, lanes, sublanes, childlanes."""
    for pool in pools.values():
        if pool.has_lanes():
            for lane in pool.lanes:
                if lane.has_lanes():
                    for sub_lane in lane.lanes:
                        add_requirements_to_lane(
                            xml_string=root,
                            search_element="bpmndi:BPMNDiagram/bpmndi:BPMNPlane/bpmndi:BPMNShape",
                            lane=sub_lane,
                            data_object_with_coordinates=data_object_with_coordinates,
                            data_objects=data_objects
                        )
                else:
                    add_requirements_to_lane(
                        xml_string=root,
                        search_element="bpmndi:BPMNDiagram/bpmndi:BPMNPlane/bpmndi:BPMNShape",
                        lane=lane,
                        data_object_with_coordinates=data_object_with_coordinates,
                        data_objects=data_objects
                    )
        else:
            add_requirements_to_lane(
                xml_string=root,
                search_element="bpmndi:BPMNDiagram/bpmndi:BPMNPlane/bpmndi:BPMNShape",
                lane=pool,
                data_object_with_coordinates=data_object_with_coordinates,
                data_objects=data_objects
            )


def main():
    file_path = open_file_dialog()
    root = get_xml(file_path)
    file_string = root
    text_annotations = find_annotations(root)
    data_objects = find_data_objects(root)
    pools = find_pools(root)
    data_objects = add_annotations_to_data_objects(root, data_objects, text_annotations)

    # Add requirements to tasks and events
    add_requirements_to_events_and_tasks(root, pools, data_objects)

    # Get data objects with coordinates
    data_object_with_coordinates = get_data_objects_with_coordinates(
        xml_string=root,
        search_element="bpmndi:BPMNDiagram/bpmndi:BPMNPlane/bpmndi:BPMNShape",
        data_objects=data_objects
    )

    # Add requirements to lanes
    add_requirements_to_resources(root, pools, data_object_with_coordinates, data_objects)

    # Verify and print valid requirements
    valid_requirements = verify_requirements(pools)
    if valid_requirements:
        #print_all_information(pools)
        extract_communications(pools)


if __name__ == "__main__":
    main()
