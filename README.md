# notion-api-py
A wrapper around **Notion Api** allowing you to create objects for your databases/pages and easily perform add/update/delete/filter operations in a more readable way

There are many libraries, **official/unofficial** out there. However the motivation behind creating this is to have a more simplistic approach to the most basic operations to perform over a `Notion database` and `Notion pages`. Also, allowing for `filtering`, handling pagination amoung query results and **Applying filters on a database view on Notion UI via code (Yes, the coolest unofficial thing so far 🥳) Refer section [Collection view filter](#collection-view-filter) for more details. 

### Prerequiste: Generate Notion Api token and integration

Before using this Api, you will need a API token from Notion

Please follow the below guide to know how to generate a api token for your Notion account, as well as how to share `databases` and `pages` with your created integration

[https://www.codingwithmiszu.com/2021/12/28/how-to-generate-a-notion-api-token-easily/](https://www.codingwithmiszu.com/2021/12/28/how-to-generate-a-notion-api-token-easily/)

[https://daily-dev-tips.com/posts/getting-started-with-the-notion-api/](https://daily-dev-tips.com/posts/getting-started-with-the-notion-api/)

To know more about NotionApi from the official sources

[https://www.notion.so/help/create-integrations-with-the-notion-api](https://www.notion.so/help/create-integrations-with-the-notion-api)

[https://developers.notion.com/docs/authorization](https://developers.notion.com/docs/authorization)

### Usage

Via the ‘Releases’ section of this repository to get the latest and greatest version of the library

Via `pip`

```python
python3 -m pip install notion-api-py
```

### RECOMMENDED - Setting up the `secrets_file.py`
Its recommened that all sensitive data be added to a `secrets_file.py` file, including the token, version, database ids and cookie related informationand not committed to the repository(add to `.gitignore`)

```python
# secrets_file.py
token = "secret_XXXXXXXXX"
version = "2021-08-16"

database1_id = "AAAAAAAAAAAAAAAAAAAAA"
database2_id = "BBBBBBBBBBBBBBBBBBBB"

# used for notion Collection view filter filers - NOT OFFICIAL API
notion_client_version = ''
x_notion_active_user_header = ''
cookie = '__cookie_string__'
```


### Notion Database

A wrapper class containing basic operations like `add_page` , `update_page` , `delete_page`  and  `filter`around a basic Notion database. 

Example usage: 

To create an object of `Tasks` database (example), all you need to do is relay the database_id as `database_id='XXXXXXX-XXXX-XXXX-XXXXXXXXX'` OR  `database_id=secrets_file.master_task_database_id` to the extended `NotionDatabase`class. The other `add`, `update`, `delete` can simply be relayed to parent `NotionDatabase` class and it will take care of it.

```python
class Tasks(NotionDatabase):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        NotionDatabase.__init__(self, token=secrets_file.token, version=secrets_file.version,
                                database_id=secrets_file.master_task_database_id)

    def add(self,icon=None,properties=None):
        self.log.info("--------- Preparing to Add tasks ---------")
        return self.add_page(icon=icon, properties=properties)

    def update(self, task_id=None, icon=None, properties=None):
        self.log.info("--------- Preparing to Update tasks ---------")
        return self.update_page(page_id=task_id, icon=icon, properties=properties)

    def delete(self, task_id):
        return self.delete_page(page_id=task_id)

    def filter(self, filter):
        return super().filter(filter)
```

### Notion Filters

The `NotionFilters` class provides a range of filters you can apply to the databases. 

Example usage

```python
incomplete_task_filter = NotionFilter(
        NotionFilterAnd(NotionRelationFilter("Release").contains("My Custom Release")
                        , NotionTextFilter("Name").contains("Test Name")
                        , NotionCheckboxFilter("✅ ?").does_not_equal(True)).build()).build()

filtered_incomplete_tasks = Tasks().filter(incomplete_feature_filter)
```

`NotionFilter`

This is wrapper/base that encapsulates all Notion filters. You can either give it a simple single filter (any one of the Single Filter,listed below) or a compund filter 

**Compund filters**

`NotionFilterAnd`

`NotionFilterOr`

These filter encapsulates the Single Filters listed below

**Single Filters**

`NotionRelationFilter` - apply filter on `Relations` fields

`NotionCheckboxFilter` - apply filter on `Checkbox` fields

`NotionTextFilter`- apply filter on `Text` fields

`NotionDateFilter` - apply filter on `Date` fields

`NotionSelectFilter` - apply filter on `Select` fields

`NotionMultiSelecFilter` - apply filter on `MultiSelect` fields

`NotionNumberFilter` apply filter on `Number` fields

`NotionFormulaFilter`- apply filter on `Formula` fields. While dealing with `Number, Text, Date, Checkbox` within `NotionFormulaFilter` use the `NotionFormulaNumberFilter` `NotionFormulaTextFilter` `NotionFormulaDateFilter` `NotionFormulaCheckboxFilter`

`NotionFilesFilter` - apply filter on `Files` fields

`NotionPeopleFilter` - apply filter on `People` fields

### Notion Page

A wrapper class containing basic operations like `add_page` , `update_page` , `build_properties`  around a basic `Notion page`. 

Example Usage:

To represent a `Tasks` page in the above `Tasks` database, we can create a `TasksPage` object extending the libraries `NotionPage` class. By virtue, the `TasksPage` class now inherits all basic operations - `add_page` , `update_page` , `build_properties` from `NotionPage` reducing the code. 

```python
class TasksPage(NotionPage):
    def __init__(self, page_id=None, existing_properties=None):
        NotionPage.__init__(self, token=secrets_file.token, version=secrets_file.version
                            ,page_id=page_id, properties=existing_properties)
```

By default, `page_id` and `existing_properties` are None. However, we need either the `page_id` or `existing_properties`.  When we are performing a filtering operation, the Notions filter results have all the information including the properties of the pages that come in the filtered result. In this case, we can simply pass the properties from the filtered results into the object while instantiating

This **helps reduce the number of api calls** to Notion to fetch properties details later

```python
# Example
incomplete_task_filter = NotionFilter(
        NotionFilterAnd(NotionRelationFilter("Release").contains("My Custom Release")
                        , NotionTextFilter("Name").contains("Test Name")
                        , NotionCheckboxFilter("✅ ?").does_not_equal(True)).build()).build()

filtered_incomplete_tasks = Tasks().filter(incomplete_feature_filter)
for each_task in filtered_incomplete_tasks:
    # print("each_task", each_task)
    each_incomplete_task = TasksPage(existing_properties=each_task)

		#The properties of each_incomplete_task can then be retrieved by below
    logging.debug("Incomplete task -> %s with status %s", each_incomplete_task.get_property("Name")
                                                    ,each_incomplete_task.get_property("Status"))
```

However, if we dont have properties, then `page_id` is mandatory as a api request would be made to fetch the page properties

```python
existing_task = TasksPage(page_id="87ec7b33-7932-bg35-d7fa7580cc63")
```

### Dynamic Notion Request builder

The build_properties function is unique automatic dynamic request builder which auto creates the json required for update page

```python
existing_task = TasksPage(page_id="87ec7b33-7932-bg35-d7fa7580cc63")

planned_days_relation = Relations().create("e9ec7b33-7932-bg35-d7fa7580cc63").append_to_existing(existing_task.get_property("Planned Day"))
planned_week_relation = Relations().create("303d3e79-9000-3000-b942-34ffd349af75").append_to_existing(existing_task.get_property("Planned Week"))
planned_month_relation = Relations().create("7896ty6r-344e-4763-819a-b7c7c405e4f0").append_to_existing(existing_task.get_property("Planned Month"))

# The 'Tasks' page might have several properties, but we are interesting only in updating the "Planned Day","Planned Week","Planned Month"
existing_task.update_page(icon="🔺",
                                 properties={
                                     "Planned Day": planned_days_relation,
                                     "Planned Week": planned_week_relation,
                                     "Planned Month": planned_month_relation
                                 })
```

would translate to a `RequestBody` in `json`something like

```python
{
    "icon":
    {
        "type": "emoji",
        "emoji": "🔺"
    },
    "archived": false,
    "properties":
    {
        "Planned Day":
        {
            "type": "relation",
            "relation":
            [
                {
                    "id": "e9ec7b33-7932-bg35-d7fa7580cc63"
                }
            ]
        },
        "Planned Week":
        {
            "type": "relation",
            "relation":
            [
                {
                    "id": "303d3e79-9000-3000-b942-34ffd349af75"
                }
            ]
        },
        "Planned Month":
        {
            "type": "relation",
            "relation":
            [
                {
                    "id": "7896ty6r-344e-4763-819a-b7c7c405e4f0"
                }
            ]
        }
    }
}
```

Another example with `date` fields (which is slightly different)

```python
Tasks().add(icon="✅",
            properties = {"Name": task_title,
                          "Task": task_relation,
                          "Hours spent": distributed_hours,
                          "Journal Date": Relations().create(journal_date_id).overwrite(),
                          "Time (Date)": {"start": "2021-12-31"
                                          ,"end": None
                                          ,"time_zone":None}
                          })
```

### Notion Properties

This class is responsible for interpreting the `properties` object for any `page` or `database` from the results of Notion requests.

Its used implicitly within the `NotionDatabase` and `NotionPage` classes

Its basically used to either read a specific property value from a json result or marshall a set of properties into a json request body

### Notion relations

This class is responsible for handling `relations` in databases, which is the basis of creating relation (much like foreign key) between different databases.

```python
#overwrites an existing relation with the new_relation
Relations().create(new_relation).overwrite()

#appends the new_relation to an existing list of relations
Relations().create(new_relation).append_to_existing(existing_relation)
```

Practical usage example

Say, extending the example above, if we use `overwrite()`

```python
#Before
{
    "icon":
    {
        "type": "emoji",
        "emoji": "🔺"
    },
    "archived": false,
    "properties":
    {
        "Planned Day":
        {
            "type": "relation",
            "relation":
            [
                {
                    "id": "e9ec7b33-7932-bg35-d7fa7580cc63"
                }
            ]
        },
        
    }
}

# Updating the Planned day relation with overwrite
existing_task = TasksPage(page_id="87ec7b33-7932-bg35-d7fa7580cc63")

planned_days_relation = Relations().create("5555555-7932-bg35-d7fa7580cc63").overwrite()
existing_task.update_page(icon="🔺",
                                 properties={
                                     "Planned Day": planned_days_relation,                                  
                                 })

#After update
{
    "icon":
    {
        "type": "emoji",
        "emoji": "🔺"
    },
    "archived": false,
    "properties":
    {
        "Planned Day":
        {
            "type": "relation",
            "relation":
            [
                {
                    "id": "5555555-7932-bg35-d7fa7580cc63"
                }
            ]
        },
        
    }
}
```

With the `append_to_existing` option, it would add to existing relation, if already present

```python
#Before
{
    "icon":
    {
        "type": "emoji",
        "emoji": "🔺"
    },
    "archived": false,
    "properties":
    {
        "Planned Day":
        {
            "type": "relation",
            "relation":
            [
                {
                    "id": "e9ec7b33-7932-bg35-d7fa7580cc63"
                }
            ]
        },
        
    }
}

# Updating the Planned day relation with overwrite
existing_task = TasksPage(page_id="87ec7b33-7932-bg35-d7fa7580cc63")

planned_days_relation = Relations().create("5555555-7932-bg35-d7fa7580cc63").append_to_existing(existing_task.get_property("Planned Day"))
existing_task.update_page(icon="🔺",
                                 properties={
                                     "Planned Day": planned_days_relation,                                  
                                 })

#After update
{
    "icon":
    {
        "type": "emoji",
        "emoji": "🔺"
    },
    "archived": false,
    "properties":
    {
        "Planned Day":
        {
            "type": "relation",
            "relation":
            [
                {
                    "id": "e9ec7b33-7932-bg35-d7fa7580cc63"
                },
               {
                    "id": "5555555-7932-bg35-d7fa7580cc63"
                }
            ]
        },
        
    }
}
```

More examples, can anyways seen in the code example of previous sections.

### Notion sorts

Not available at the moment. This is on the wishlist

### Collection view filter

This is an exciting option, which allows you auto set filters on particular `view` in Notion Databases

To know more about Notion database view, refer [https://www.notion.so/help/guides/using-database-views](https://www.notion.so/help/guides/using-database-views)

![Untitled](Detailed%20d%2016435/Untitled.png)

While the official Notion Api provides an option to `query` databases - [https://developers.notion.com/reference/post-database-query](https://developers.notion.com/reference/post-database-query)

it doesnt provide an ability to actually **“set”** the filters on the UI.

Example use cases 

**Use case 1:** where I needed this. I have `Planned Days`, `Planned Months` and `Planned Weeks` as relation pages and I want that every morning, the filter automatically changes to reflect the correct date/week/month so I can plan my tasks accordingly

**Use case 2:** I use Notion for project management where I create Project → Features → Tasks. I have templates for each of these. So whenever I create a new feature using the template, it brings in the linked task database with the `Related Features` filter applied. However, I would also like “auto” apply the `Tags`, `Projects` and `Release` relations, as I know them based on the Feature page we are on. As of this writing, Notion provides no way of doing this.

![Untitled](Detailed%20d%2016435/Untitled%201.png)

I reverse engineered the api calls from Notion to thier server to see what they are doing when  we apply filter operations to a view

Based on my experiments, I designed wrapper classes around it

***Please note this is unofficial api call, hence you will need a logged in session cookie to make this to work***

There are ‘n’ number of tutorials/chrome extensions on the net, how to get the stored cookies for a site.Currenly this is not covered here.

Once, you have the cookie details, we could use something like the below

```python

#Applying filters on UI for Use case 1
query2filter = NotionWebQuery2(
        notion_web_filter=NotionWebQuery2Filter("and"
                                                , NotionWebDbSimpleFilter("exact", day_page_id,
                                                                          "relation_contains",
                                                                          task_property_id_map.get("Planned Day"))
                                                , NotionWebDbSimpleFilter("exact", week_page_id,
                                                                          "relation_contains",
                                                                          task_property_id_map.get("Planned Week"))
                                                , NotionWebDbSimpleFilter("exact", month_page_id,
                                                                          "relation_contains",
                                                                          task_property_id_map.get("Planned Month"))
                                                )
        #Optional, only if you require to provide aggregate operations on columns
        # In my use case, wanted to provide aggregate on time spent for tasks as well as number of tasks
         , notion_web_aggregations=NotionWebDbAggregations(
            NotionWebDbAggregation(task_property_id_map.get("Actual time spent")).sum()
            , NotionWebDbAggregation(task_property_id_map.get("Name")).count()
        )
    ).generate()
```

Above, will generate the `json` RequestBody for the request to be sent

Further, you pass this filter to `generate_collection_view_filter_body` followed by `send_collection_view_filter_request`

```python

# the collection_id and collection_view_id can be fetched from url of the view
# if you right click on a database view and use the "Copy link" you should get a url as
# https://www.notion.so/XXXXXXXXXXX?v=YYYYYYYYY
# Here the collection_id=XXXXXXXXXXX and collection_view_id="YYYYYYYYY"
payload=generate_collection_view_filter_body(collection_id, collection_view_id,
                                               int(datetime.now().timestamp()), query2filter)

# notion_client_version, x_notion_active_user_header, cookie
# These details can be fetched by inspecting the Chrome devtools(Network) and the cookie
send_collection_view_filter_request("https://www.notion.so/api/v3/saveTransactions"
                                    ,payload
                                    ,secrets_file.notion_client_version
                                    ,secrets_file.x_notion_active_user_header
                                    ,secrets_file.cookie)
```
