import json
import urllib
import uuid
import logging

import requests


class NotionWebQuery2:
    def __init__(self, notion_web_filter=None, notion_web_aggregations=None, notion_web_sorts=None):
        self.query2 = {}
        self.filters = [] if notion_web_filter == None else notion_web_filter.generate()
        self.aggregations = [] if notion_web_aggregations == None else notion_web_aggregations.generate()
        self.sorts = [] if notion_web_sorts == None else notion_web_sorts.generate()
        if self.sorts != []:
            self.query2['sort'] = self.sorts
        if self.filters != []:
            self.query2['filter'] = self.filters
        if self.aggregations != []:
            self.query2['aggregations'] = self.aggregations

    def generate(self):
        return self.query2


class NotionWebQuery2Filter:
    def __init__(self, operator, *args):
        self.ffilters = {}
        self.filters = []
        for arg in args:
            self.filters.append(arg.generate())
        self.ffilters["filters"] = self.filters
        self.ffilters["operator"] = operator

    def generate(self):
        return self.ffilters


class NotionWebDbSimpleFilter:
    def __init__(self, type, value, operator, property):
        logging.debug("NotionWebDbSimpleFilter: type: %s, value: %s, operator: %s, property: %s" % (type, value, operator, property))
        self.type = type
        self.value = value
        self.operator = operator
        self.property = urllib.parse.unquote(property)

    def generate(self):
        ffilter = {}
        filter = {}
        filter["value"] = {}
        filter["value"]["type"] = self.type
        filter["value"]["value"] = self.value
        filter["operator"] = self.operator
        ffilter["filter"] = filter
        ffilter["property"] = self.property
        return ffilter


class NotionWebDbCompoundFilter:
    def __init__(self, operator, *args):
        self.ffilters = {}
        self.filters = []
        for arg in args:
            self.filters.append(arg.generate())
        self.ffilters["filters"] = self.filters
        self.ffilters["operator"] = operator

    def generate(self):
        return self.ffilters


class NotionWebDbAggregations:
    def __init__(self, *args):
        self.list_aggregations = []
        for arg in args:
            self.list_aggregations.append(arg.generate())

    def generate(self):
        return self.list_aggregations


class NotionWebDbAggregation:
    def __init__(self, property):
        self.aggregate = {}
        self.aggregate["property"] = urllib.parse.unquote(property)

    def sum(self):
        self.aggregate["aggregator"] = "sum"
        return self

    def count(self):
        self.aggregate["aggregator"] = "count"
        return self

    def generate(self):
        return self.aggregate


def split_page_id(page_id):
    print(page_id)
    m = [8, 4, 4, 4, 12]
    i = 0
    split_strings = []
    index = 0
    j = 0
    while index < len(page_id):
        # print(index, '->', m[j])
        split_strings.append(page_id[index: index + m[j]])
        index = index + m[j]
        j = j + 1

    # print(split_strings)
    return ("-".join(split_strings))


def generate_collection_view_filter_body(database_id, view_id, unix_tp, query2filter):
    body = json.dumps(
        {
            "requestId": str(uuid.uuid4()),  # random uuid?
            "transactions":
                [
                    {
                        "id": str(uuid.uuid4()),  # random uuid?
                        "operations":
                            [
                                {
                                    "pointer":
                                        {
                                            "table": "collection_view",
                                            "id": split_page_id(view_id),  # view -id
                                        },
                                    "path":
                                        [],
                                    "command": "update",
                                    "args": {
                                        "query2": query2filter
                                    }
                                },
                                {
                                    "pointer":
                                        {
                                            "table": "block",
                                            "id": split_page_id(database_id),  # database-id
                                        },
                                    "path":
                                        [],
                                    "command": "update",
                                    "args":
                                        {
                                            "last_edited_time": unix_tp  # unix-timestamp
                                        }
                                }
                            ]
                    }
                ]
        })
    return body


def send_collection_view_filter_request(url, payload, notion_client_version, x_notion_active_user_header, cookie):
    headers = {
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Content-Type': 'application/json',
        'notion-client-version': notion_client_version,
        'x-notion-active-user-header': x_notion_active_user_header,
        'sec-ch-ua-platform': '"macOS"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Cookie': cookie
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
