import json
import logging
import notion_endpoints
import requests


class NotionApi:
    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Notion-Version": version
        }
        self.logger = logging.getLogger(self.__class__.__name__)

    def retrieve_database(self, database_id):
        url = notion_endpoints.update_retrieve_database.replace(":id", database_id)
        return self.send_notion_request("GET", url)

    # def query_database(self, database_id, body):
    #     url = notion_endpoints.query_database.replace(":id", database_id)
    #     return self.send_notion_request("POST", url, body)

    # returns results list
    # def query_database(self, database_id, body):
    #     url = notion_endpoints.query_database.replace(":id", database_id)
    #     has_more = True
    #     all_results = []
    #     while has_more:
    #         response = self.send_notion_request("POST", url, body)
    #         if response.status_code != 200:
    #             logging.error(f'Response Status: {response.status_code}')
    #         else:
    #             all_results.extend([response.json()["results"][i]["id"] for i in range(0,len(response.json()["results"]))])
    #
    #         has_more = response.json()['has_more']
    #         if has_more:
    #             body=self.add_pagination_to_filter(response.json()['next_cursor'], body)
    #             # body = {
    #             #     "start_cursor": response.json()['next_cursor']
    #             # }
    #
    #     return (all_results)

    def query_database(self, database_id, body):
        url = notion_endpoints.query_database.replace(":id", database_id)
        has_more = True
        all_results = []
        while has_more:
            response = self.send_notion_request("POST", url, body)
            if response.status_code != 200:
                self.logger.error(f'Response Status: {response.status_code}')
            else:
                all_results.extend(response.json()["results"])

            has_more = response.json()['has_more']
            if has_more:
                body=self.add_pagination_to_filter(response.json()['next_cursor'], body)
                # body = {
                #     "start_cursor": response.json()['next_cursor']
                # }

        return (all_results)
    def add_pagination_to_filter(self, next_cursor, existing_filter):
        if existing_filter!=None:
          filter_with_pagination=json.loads(json.dumps(existing_filter))
          filter_with_pagination['start_cursor']=next_cursor
          return filter_with_pagination
        else:
            return {
                "start_cursor": next_cursor
            }
    def create_database(self, body):
        return self.send_notion_request("POST", notion_endpoints.create_database, body)

    def update_database(self, database_id, body):
        url = notion_endpoints.update_retrieve_database.replace(":id", database_id)
        return self.send_notion_request("PATCH", url, body)

    def create_page(self, body):
        return self.send_notion_request("POST", notion_endpoints.create_page, body)

    def retrieve_page_properties(self, page_id):
        url = notion_endpoints.update_retrieve_page_properties.replace(":id", page_id)
        return self.send_notion_request("GET", url)

    def update_page_properties(self, body, page_id):
        url = notion_endpoints.update_retrieve_page_properties.replace(":id", page_id)
        return self.send_notion_request("PATCH", url, body)

    def retrieve_block(self, block_id):
        url = notion_endpoints.update_retrieve_block.replace(":id", block_id)
        return self.send_notion_request("GET", url)

    def retrieve_block_children(self, block_id):
        url = notion_endpoints.retrieve_append_block_children.replace(":id", block_id)
        return self.send_notion_request("GET", url)

    def update_block(self, block_id, body):
        url = notion_endpoints.update_retrieve_block.replace(":id", block_id)
        return self.send_notion_request("PATCH", url, body)

    def append_block_children(self, block_id, body):
        url = notion_endpoints.retrieve_append_block_children.replace(":id", block_id)
        return self.send_notion_request("PATCH", url, body)

    def send_notion_request(self, request_type, endpoint, body=None):

        if (body != None):
            data = json.dumps(body)
            self.logger.debug("A Notion request with this request body will be sent: %s", data)
        else:
            data = None
        # print(str(uploadData))
        try:
            res = requests.request(request_type, endpoint, headers=self.headers, data=data)
            if (res.status_code == 200):
                self.logger.debug("Response code 200")
            else:
                raise Exception("Response code other than 200. Received response code:" + res.status_code)
        except Exception as e:
            raise Exception("Issue encountered while trying to send request for " + endpoint + ":", e)

        self.logger.debug(res.text)
        return res
