import json
import logging

from notion_api import NotionApi
from notion_properties import NotionProperties, NotionProperty

NotionPropertiesMap={
    'number': lambda k,v: NotionProperty(k).number(v),
    'text': lambda k,v: NotionProperty(k).text(v),
    'title': lambda k,v: NotionProperty(k).title(v),
    'date': lambda k,v: NotionProperty(k).date(v),
    'checkbox': lambda k,v: NotionProperty(k).checkbox(v),
    'select': lambda k,v: NotionProperty(k).select(v),
    'multi_select': lambda k,v: NotionProperty(k).multi_select(v),
    'relation': lambda k,v: NotionProperty(k).relations(v),
}

class NotionPage(NotionApi):
    def __init__(self, token=None, version=None, page_id=None, properties=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        if token == None or version == None:
            self.logger.error("NotionPage: token or version is None")
            raise Exception("Either token or version is None and are required to connect to NotionApi")
        else:
            NotionApi.__init__(self, token, version)
            self.existing_id = page_id
            # if properties == None:  # No existing properties, so fetch via api using the page id
            #     self.existing_page_properties = self.retrieve_page_properties(page_id).json()[
            #         "properties"] if page_id != None else None
            # else:  # Existing properties available, wohoooooo...no api request required
            self.existing_page_properties = properties
            # print("existing_page_properties",self.existing_page_properties)

    def get_property(self, property_name):
        return NotionProperties(self.get_all_properties()).get_property(property_name)


    def update_page(self, icon=None, external_icon_url=None
                    , cover_url=None, archived=False, properties=""):
        request_body = CreateNotionApiRequestBody(icon=icon
                                                  , external_icon_url=external_icon_url
                                                  , cover_url=cover_url
                                                  , archived=archived
                                                  , properties=json.loads(self.build_properties(properties))
                                                  ).generate()
        self.logger.debug("update_page json created -> %s", json.dumps(request_body))
        response = self.update_page_properties(request_body, self.existing_id)
        self.logger.debug("update_page response -> %s" , str(response.json()))
        if response.status_code != 200:
            self.logger.debug(f'Response Status: {response.status_code}')
            raise Exception(f'Response Status: {response.status_code}')
        else:
            return response.json()['id']

    def build_properties(self, properties):
        self.logger.log(logging.DEBUG, "Building properties body using build_properties -> %s", properties)
        notion_properties = []
        # This is field name -> field type map for the current database
        property_type_map=self.get_property_type_map()
        for key, value in properties.items():
            self.logger.debug("For property %s == %s" % (key, value))
            individual_property_dict=NotionPropertiesMap.get(property_type_map[key])(key, value)
            self.logger.debug("dict created -> %s" ,individual_property_dict)
            if individual_property_dict != None:
                notion_properties.append(individual_property_dict)
            else:
                self.logger.debug("Since value is None, it wont be appended to final notion properties")

        self.logger.debug("notion_properties: %s",str(notion_properties))
        return NotionProperties(properties=notion_properties).get_json_string()

    def get_all_properties(self):
        if self.existing_page_properties== None:
            self.logger.debug("self.database_properties is None. Hence retrieving from NotionApi")
            self.existing_page_properties = self.retrieve_page_properties(self.existing_id).json()["properties"]
        return self.existing_page_properties

    def get_property_type_map(self):
        self.property_type_map={}
        for key, value in self.get_all_properties().items():
            self.property_type_map[key] = value["type"]
        self.logger.info("Pages property_type_map generated -> "+str(self.property_type_map))
        return self.property_type_map

class CreateNotionApiRequestBody:
    def __init__(self, parent_database_id=None, icon=None, external_icon_url=None, cover_url=None, archived=False,
                 properties=""):
        self.request_body = {}
        if parent_database_id != None:
            self.request_body["parent"] = {
                "database_id": parent_database_id
            }
        if icon != None:
            self.request_body["icon"] = self.build_icon(icon)

        if external_icon_url != None:
            self.request_body["icon"] = self.build_external_icon(external_icon_url)

        if cover_url != None:
            self.request_body["cover"] = self.build_cover(cover_url)
        self.request_body["archived"] = archived
        self.request_body["properties"] = properties

    def build_icon(self, emoji):
        return {
            "type": "emoji",
            "emoji": emoji
        }

    def build_external_icon(self, icon_url):
        return {
            "type": "external",
            "external": {
                "url": icon_url
            }
        }

    def build_cover(self, cover_url):
        return {
            "type": "external",
            "external": {
                "url": cover_url
            }
        }

    def generate(self):
        return self.request_body

