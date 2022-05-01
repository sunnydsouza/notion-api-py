import json
import logging

from notion_api_py.notion_api import NotionApi
from notion_api_py.notion_page import CreateNotionApiRequestBody
from notion_api_py.notion_properties import NotionProperties, NotionProperty

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

class NotionDatabase(NotionApi):
    def __init__(self, token=None, version=None, database_id=None, existing_pages=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        if token == None or version == None or database_id == None:
            self.logger.error("NotionDatabase: token, version or database_id is None")
            raise Exception("Either token or version or database_id is None and are required to connect to NotionApi")
        else:
            NotionApi.__init__(self,token, version)
            self.database_id = database_id
            self.database_properties = None
            self.existing_pages = existing_pages


    # def add(self, add_page):
    #     self.logger.debug("add_page json created ->" + json.dumps(add_page))
    #     # response = self.create_page(add_page)
    #     # if response.status_code != 200:
    #     #     print(f'Response Status: {response.status_code}')
    #     #     raise Exception(f'Response Status: {response.status_code}')
    #     # else:
    #     #     return response.json()["id"]

    # def update(self, page_id, update_page):
    #     self.logger.debug("update_page json created -> " + json.dumps(update_page))
    #     print("update_page json created ->" + json.dumps(update_page))
    #     response = self.update_page_properties(update_page, page_id)
    #     print(response.json())
    #     if response.status_code != 200:
    #         print(f'Response Status: {response.status_code}')
    #         raise Exception(f'Response Status: {response.status_code}')
    #     else:
    #         return response.json()['id']

    def add_page(self,  icon=None, external_icon_url=None
                    , cover_url=None, archived=False, properties=""):
       request_body = CreateNotionApiRequestBody(parent_database_id=self.database_id
                                       , icon=icon
                                       , external_icon_url=external_icon_url
                                       , cover_url=cover_url
                                       , archived=archived
                                       , properties=json.loads(self.build_properties(properties))
                                       ).generate()
       self.logger.info("add_page json created -> " + json.dumps(request_body))
       response = self.create_page(request_body)
       if response.status_code != 200:
           self.logger.debug(f'Response Status: {response.status_code}')
           raise Exception(f'Response Status: {response.status_code}')
       else:
           return response.json()["id"]

    def update_page(self, page_id=None, icon=None, external_icon_url=None
                    , cover_url=None, archived=False, properties=""):
       request_body = CreateNotionApiRequestBody(parent_database_id=self.database_id
                                       , icon=icon
                                       , external_icon_url=external_icon_url
                                       , cover_url=cover_url
                                       , archived=archived
                                       , properties=json.loads(self.build_properties(properties))
                                       ).generate()
       self.logger.debug("update_page json created -> " + json.dumps(request_body))
       response = self.update_page_properties(request_body, page_id)
       self.logger.debug("update_page response ->"+response.json())
       if response.status_code != 200:
           print(f'Response Status: {response.status_code}')
           raise Exception(f'Response Status: {response.status_code}')
       else:
           return response.json()['id']

    def delete_page(self, page_id=None):
        request_body = CreateNotionApiRequestBody(parent_database_id=self.database_id
                                                  , archived=True
                                                  ).generate()
        self.logger.debug("delete_page json created -> " + json.dumps(request_body))
        response = self.update_page_properties(request_body, page_id)
        self.logger.debug("delete_page response ->" + response.json())
        if response.status_code != 200:
            print(f'Response Status: {response.status_code}')
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
        return NotionProperties(properties=notion_properties).get_json_string()

    def filter(self, filter):
        self.logger.debug("filter json created -> %s", json.dumps(filter))
        all_filtered_results = self.query_database(self.database_id, filter)
        if len(all_filtered_results) > 0:
            # self.logger.debug("all the filtered results -> %s",str(all_filtered_results))
            return all_filtered_results

    # def filter_with_properties(self, filter):
    #     print(json.dumps(filter))
    #     all_filtered_results = self.query_database_with_properties(self.database_id, filter)
    #     if len(all_filtered_results) > 0:
    #         # print(all_filtered_results)
    #         return all_filtered_results


    def get_all_properties(self):
        if self.database_properties== None:
            self.logger.debug("self.database_properties is None. Hence retrieving from NotionApi")
            self.database_properties = self.retrieve_database(self.database_id).json()["properties"]
        return self.database_properties

    def get_property_type_map(self):
        self.property_type_map={}
        for key, value in self.get_all_properties().items():
            self.property_type_map[key] = value["type"]
        self.logger.info("Database property_type_map generated -> "+str(self.property_type_map))
        return self.property_type_map
