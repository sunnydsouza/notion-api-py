class NotionFilter:

    def __init__(self, filter_conditions):
        self.filter = {}
        self.filter["filter"] = filter_conditions

    def build(self):
        return self.filter


class NotionFilterAnd:

    def __init__(self, *args):
        self.and_condition = {}
        arg_list = []
        for arg in args:
            if arg != None:
                arg_list.append(arg)
        self.and_condition["and"] = arg_list
        # print(self.and_condition)

    def build(self):
        return self.and_condition


class NotionFilterOr:
    def __init__(self, *args):
        self.or_condition = {}
        arg_list = []
        for arg in args:
            if arg != None:
                arg_list.append(arg)
        self.or_condition["or"] = arg_list
        # print(self.or_condition)

    def build(self):
        return self.or_condition


class NotionRelationFilter:
    def __init__(self, property):
        self.property = property

    def contains(self, value):
        return generate_condition("relation", self.property, "contains", value)

    def does_not_contain(self, value):
        return generate_condition("relation", self.property, "does_not_contain", value)

    def is_empty(self, value):
        return generate_condition("relation", self.property, "is_empty", value)

    def is_not_empty(self, value):
        return generate_condition("relation", self.property, "is_not_empty", value)


class NotionCheckboxFilter:

    def __init__(self, property):
        self.property = property

    def does_not_equal(self, value):
        return generate_condition("checkbox", self.property, "does_not_equal", value)

    def equals(self, value):
        return generate_condition("checkbox", self.property, "equals", value)


class NotionTextFilter:

    def __init__(self, property):
        self.property = property

    def equals(self, value):
        return generate_condition("text", self.property, "equals", value)

    def does_not_equal(self, value):
        return generate_condition("text", self.property, "does_not_equal", value)

    def contains(self, value):
        return generate_condition("text", self.property, "contains", value)

    def does_not_contain(self, value):
        return generate_condition("text", self.property, "does_not_contain", value)

    def does_not_equal(self, value):
        return generate_condition("text", self.property, "does_not_equal", value)

    def starts_with(self, value):
        return generate_condition("text", self.property, "starts_with", value)

    def ends_with(self, value):
        return generate_condition("text", self.property, "ends_with", value)

    def is_empty(self, value):
        return generate_condition("text", self.property, "is_empty", value)

    def is_not_empty(self, value):
        return generate_condition("text", self.property, "is_not_empty", value)


class NotionFormulaFilter:
    def __init__(self, property):
        self.property = property

    def text(self, value):
        return generate_condition("formula", self.property, "text", value)

    def checkbox(self, value):
        return generate_condition("formula", self.property, "checkbox", value)

    def number(self, value):
        return generate_condition("formula", self.property, "number", value)

    def date(self, value):
        return generate_condition("formula", self.property, "date", value)


class NotionFormulaNumberFilter:
    @staticmethod
    def equals(value):
        return generate_condition_formula("number", "equals", value)

    @staticmethod
    def does_not_equal(value):
        return generate_condition_formula("number", "does_not_equal", value)

    @staticmethod
    def greater_than(value):
        return generate_condition_formula("number", "greater_than", value)

    @staticmethod
    def less_than(value):
        return generate_condition_formula("number", "less_than", value)

    @staticmethod
    def greater_than_or_equal_to(value):
        return generate_condition_formula("number", "greater_than_or_equal_to", value)

    @staticmethod
    def less_than_or_equal_to(value):
        return generate_condition_formula("number", "less_than_or_equal_to", value)

    @staticmethod
    def is_empty(value):
        return generate_condition_formula("number", "is_empty", value)

    @staticmethod
    def is_not_empty(value):
        return generate_condition_formula("number", "is_not_empty", value)


class NotionFormulaTextFilter:
    # Reserved only when used in conjuction with formula filter
    @staticmethod
    def equals(value):
        return generate_condition_formula("text", "equals", value)

    @staticmethod
    def does_not_equal(value):
        return generate_condition_formula("text", "does_not_equal", value)

    @staticmethod
    def contains(value):
        return generate_condition_formula("text", "contains", value)

    @staticmethod
    def does_not_contain(value):
        return generate_condition_formula("text", "does_not_contain", value)

    @staticmethod
    def does_not_equal(value):
        return generate_condition_formula("text", "does_not_equal", value)

    @staticmethod
    def starts_with(value):
        return generate_condition_formula("text", "starts_with", value)

    @staticmethod
    def ends_with(value):
        return generate_condition_formula("text", "ends_with", value)

    @staticmethod
    def is_empty(value):
        return generate_condition_formula("text", "is_empty", value)

    @staticmethod
    def is_not_empty(value):
        return generate_condition_formula("text", "is_not_empty", value)


class NotionFormulaDateFilter:

    @staticmethod
    def equals(value):
        return generate_condition_formula("date", "equals", value)

    @staticmethod
    def before(value):
        return generate_condition_formula("date", "before", value)

    @staticmethod
    def after(value):
        return generate_condition_formula("date", "after", value)

    @staticmethod
    def on_or_before(value):
        return generate_condition_formula("date", "on_or_before", value)

    @staticmethod
    def is_empty(value):
        return generate_condition_formula("date", "is_empty", value)

    @staticmethod
    def is_not_empty(value):
        return generate_condition_formula("date", "is_not_empty", value)

    @staticmethod
    def on_or_after(value):
        return generate_condition_formula("date", "on_or_after", value)

    @staticmethod
    def past_week(value):
        return generate_condition_formula("date", "past_week", value)

    @staticmethod
    def past_month(value):
        return generate_condition_formula("date", "past_month", value)

    @staticmethod
    def past_year(value):
        return generate_condition_formula("date", "past_year", value)

    @staticmethod
    def next_week(value):
        return generate_condition_formula("date", "next_week", value)

    @staticmethod
    def next_month(value):
        return generate_condition_formula("date", "next_month", value)

    @staticmethod
    def next_year(value):
        return generate_condition_formula("date", "next_year", value)


class NotionFormulaCheckboxFilter:

    @staticmethod
    def does_not_equal(value):
        return generate_condition_formula("checkbox" "does_not_equal", value)

    @staticmethod
    def equals(value):
        return generate_condition_formula("checkbox", "equals", value)


class NotionFilesFiler:
    def __init__(self, property):
        self.property = property

    def is_empty(self, value):
        return generate_condition("files", self.property, "is_empty", value)

    def is_not_empty(self, value):
        return generate_condition("files", self.property, "is_not_empty", value)


class NotionPeopleFilter:
    def __init__(self, property):
        self.property = property

    def contains(self, value):
        return generate_condition("people", self.property, "contains", value)

    def does_not_contain(self, value):
        return generate_condition("people", self.property, "does_not_contain", value)

    def is_empty(self, value):
        return generate_condition("people", self.property, "is_empty", value)

    def is_not_empty(self, value):
        return generate_condition("people", self.property, "is_not_empty", value)


class NotionDateFilter:
    def __init__(self, property):
        self.property = property

    def equals(self, value):
        return generate_condition("date", self.property, "equals", value)

    def before(self, value):
        return generate_condition("date", self.property, "before", value)

    def after(self, value):
        return generate_condition("date", self.property, "after", value)

    def on_or_before(self, value):
        return generate_condition("date", self.property, "on_or_before", value)

    def is_empty(self, value):
        return generate_condition("date", self.property, "is_empty", value)

    def is_not_empty(self, value):
        return generate_condition("date", self.property, "is_not_empty", value)

    def on_or_after(self, value):
        return generate_condition("date", self.property, "on_or_after", value)

    def past_week(self, value):
        return generate_condition("date", self.property, "past_week", value)

    def past_month(self, value):
        return generate_condition("date", self.property, "past_month", value)

    def past_year(self, value):
        return generate_condition("date", self.property, "past_year", value)

    def next_week(self, value):
        return generate_condition("date", self.property, "next_week", value)

    def next_month(self, value):
        return generate_condition("date", self.property, "next_month", value)

    def next_year(self, value):
        return generate_condition("date", self.property, "next_year", value)


class NotionSelectFilter:
    def __init__(self, property):
        self.property = property

    def equals(self, value):
        return generate_condition("select", self.property, "equals", value)

    def does_not_equal(self, value):
        return generate_condition("select", self.property, "does_not_equal", value)

    def is_empty(self, value):
        return generate_condition("select", self.property, "is_empty", value)

    def is_not_empty(self, value):
        return generate_condition("select", self.property, "is_not_empty", value)


class NotionMultiSelectFilter:
    def __init__(self, property):
        self.property = property

    def contains(self, value):
        return generate_condition("multi_select", self.property, "contains", value)

    def does_not_contain(self, value):
        return generate_condition("multi_select", self.property, "does_not_contain", value)

    def is_empty(self, value):
        return generate_condition("multi_select", self.property, "is_empty", value)

    def is_not_empty(self, value):
        return generate_condition("multi_select", self.property, "is_not_empty", value)


class NotionNumberFilter:
    def __init__(self, property):
        self.property = property

    def equals(self, value):
        return generate_condition("number", self.property, "equals", value)

    def does_not_equal(self, value):
        return generate_condition("number", self.property, "does_not_equal", value)

    def greater_than(self, value):
        return generate_condition("number", self.property, "greater_than", value)

    def less_than(self, value):
        return generate_condition("number", self.property, "less_than", value)

    def greater_than_or_equal_to(self, value):
        return generate_condition("number", self.property, "greater_than_or_equal_to", value)

    def less_than_or_equal_to(self, value):
        return generate_condition("number", self.property, "less_than_or_equal_to", value)

    def is_empty(self, value):
        return generate_condition("number", self.property, "is_empty", value)

    def is_not_empty(self, value):
        return generate_condition("number", self.property, "is_not_empty", value)


def generate_condition(filter_object, property_name, condition, value):
    if value != None:
        relation_filter = {}
        relation_filter["property"] = property_name
        relation_filter[filter_object] = {
            condition: value
        }
        # print(relation_filter)
        return relation_filter
    return None


def generate_condition_formula(filter_object, condition, value):
    if value != None:
        # relation_filter = {}
        # relation_filter[filter_object] = {
        #     condition: value
        # }
        # print(relation_filter)
        return {
            condition: value
        }
    return None
