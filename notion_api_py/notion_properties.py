import json
import logging

class NotionProperties:
    def __init__(self, existing_properties=None, properties=[]):
        self.log = logging.getLogger(self.__class__.__name__)
        self.properties = {}
        self.existing_properties = existing_properties
        for property in properties:
            self.properties[property.get_property_name()]=property.get_property_value()

    def get_property(self, property_name):
        if self.existing_properties != None:
            if self.existing_properties.__contains__(property_name):
                if self.existing_properties[property_name]["type"] == "formula":
                    return self.existing_properties[property_name]["formula"][self.existing_properties[property_name]["formula"]["type"]]
                elif self.existing_properties[property_name]["type"] == "title" or self.existing_properties[property_name]["type"] == "rich_text":
                    return self.existing_properties[property_name][self.existing_properties[property_name]["type"]][0]["plain_text"]
                elif self.existing_properties[property_name]["type"] == "rollup":
                    return self.existing_properties[property_name]["rollup"][self.existing_properties[property_name]["rollup"]["type"]]
                else:
                    return self.existing_properties[property_name][self.existing_properties[property_name]["type"]]
            else:
                raise Exception("Key doesnt exist:" + property_name)
        else:
            raise Exception("There is no existing properties to look into")

    def get_properties_dict(self):
        return self.properties

    def get_json_string(self):
        return json.dumps(self.properties)

class NotionProperty:
    def __init__(self, property_name):
        # self.property = {}
        self.property_name = property_name
        self.property_value = None

    def get_property_name(self):
        return self.property_name

    def get_property_value(self):
        return self.property_value

    def number(self, value):
        if value != None:
            self.property_value = {
                "type": "number",
                "number": float(value)
            }
            return self
        return None

    def text(self, value):
        if value != None:
            self.property_value = {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": value,
                            "link": None
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": value,
                        "href": None
                    }
                ]
            }
            return self
        return None

    def title(self, value):
        if value != None:
            self.property_value = {
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": value,
                            "link": None
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": value,
                        "href": None
                    }
                ]
            }
            return self
        return None

    def relations(self, value):
        if value != None:
            self.property_value = {
                "type": "relation",
                "relation": json.loads(json.dumps(value))
            }
            return self
        return None

    def select(self, value):
        if value != None:
            self.property_value = {
                "type": "select",
                "select": {
                    "name": value,
                }
            }
            return self
        return None

    def multi_select(self, value):
        if value != None:
            self.property_value = {
                "type": "multi_select",
                "multi_select": value,
            }
            return self
        return None

    def checkbox(self, value):
        if value != None:
            self.property_value = {
                "type": "checkbox",
                "checkbox": value
            }
            return self
        return None

    def date(self, value):
        # startdate_yyyy_mm_dd, enddate_yyyy_mm_dd, starttime, endtime
        if value != None:
            self.property_value = {
                "type": "date",
                "date": {
                    "start": value["start"],
                    "end": value["end"],
                    "time_zone": value["time_zone"]
                }
            }
            return self
        return None