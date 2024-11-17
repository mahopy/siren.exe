from typing import List


class TextAnnotation:
    def __init__(self, id: str, text: str):
        self.id = id
        self.text = text


# class DataObject:
#     def __init__(self, id: str, name: str):
#         self.id = id
#         self.name = name
#         self.text_annotation =
#
#     def add_text_annotation(self, annotation: TextAnnotation):
#         self.text_annotation = annotation
#
#     def get_text_annotations(self):
#         return self.text_annotation

class DataObject:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.text_annotation = ""

    def add_text_annotation(self, annotation: str):
        self.text_annotation = annotation

    def get_text_annotation(self):
        return self.text_annotation


class Element:
    def __init__(self, id: str):
        self.id = id
        self.data_objects: List[DataObject] = []

    def add_requirement(self, data_object: DataObject):
        self.data_objects.append(data_object)

    def get_requirements(self):
        return self.data_objects


class Task(Element):
    def __init__(self, id: str, name: str):
        super().__init__(id)
        self.name = name


class Event(Element):
    def __init__(self, id: str):
        super().__init__(id)
        self.sender = ""
        self.receiver = ""
        self.receiver_name = ""
        self.receiver_id = ""
    def add_event_infos(self, sender, receiver):
        print(f"Added INFO: {receiver}")
        self.sender = sender
        self.receiver = receiver

class Pool(Element):
    def __init__(self, id: str, name: str, process_ref: str = None):
        super().__init__(id)
        self.name = name
        self.events = []
        self.tasks = []
        self.lanes = []
        self.requirements = []
        self.process_ref = process_ref

    def add_element(self, element):
        if isinstance(element, (Task, Event)):
            if not self.has_lanes():
                if isinstance(element, Task):
                    self.tasks.append(element)
                elif isinstance(element, Event):
                    self.events.append(element)
            else:
                raise TypeError("Cannot add elements directly to a pool that contains lanes")
        else:
            raise TypeError("Only Task or Event objects can be added to Pool")

    def add_requirement(self, element):
        self.requirements.append(element)

    def get_requirements(self):
        return self.requirements
    def add_lane(self, lane):
        if isinstance(lane, Lane):
            if not self.has_elements():
                self.lanes.append(lane)
            else:
                raise TypeError("Cannot add lanes to a pool that already contains elements")
        else:
            raise TypeError("Only Lane objects can be added to Pool")

    def get_events(self):
        return self.events

    def get_tasks(self):
        return self.tasks

    def has_elements(self):
        if self.tasks or self.events:
            return True
        else:
            return False

    def has_lanes(self):
        return self.lanes


class Lane(Pool):
    def __init__(self, id: str, name: str):
        super().__init__(id, name)
        self.lanes = []

    def add_lane(self, lane):
        if isinstance(lane, Lane):
            if not self.has_elements():
                self.lanes.append(lane)
            else:
                raise TypeError("Cannot add lanes to a lane that already contains elements")
        else:
            raise TypeError("Only Lane objects can be added to Lane")

    def get_lanes(self):
        return self.lanes


class Coordinate:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.x_end = self.calculate_x_end()
        self.y_end = self.calculate_y_end()

    def calculate_x_end(self) -> int:
        return self.x + self.width

    def calculate_y_end(self) -> int:
        return self.y + self.height