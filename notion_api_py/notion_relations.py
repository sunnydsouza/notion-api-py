import logging

# Usage
# Relations().create("a-new-awesome-relation").append_to_existing(existing_relation)
# Relations().create("a-new-awesome-relation").append_to_existing([])
class Relations:

    def __init__(self):
        self.new_relation = {}
        self.log = logging.getLogger(self.__class__.__name__)

    def append_to_existing(self, existing_relations):
        relations=existing_relations
        if not self.does_relation_exist(self.new_relation, relations):
            relations.append(self.new_relation)
        self.log.debug("Final relation created ->" + str(relations))
        return relations

    def create(self, relation_id):
        self.new_relation['id'] = relation_id
        self.log.debug("Trying to create a new relation ->" + str(self.new_relation))
        return self

    def overwrite(self):
        return self.append_to_existing([])

    def does_relation_exist(self, new_relation, existing_relation_list):
        self.log.debug("Checking if relation exists ->"+ str(new_relation))
        if not bool(existing_relation_list):
            self.log.debug("There is no existing relations for this property")
            return False

        else:
            for each_relation in existing_relation_list:
                if each_relation['id'] == new_relation["id"] :
                    self.log.debug("This relation ->" + new_relation["id"]  + " -> already exists for this property")
                    return True
                else:
                    self.log.debug("This relation ->" + new_relation["id"]  + " -> doesnt exist. Hence will be appended")
                    return False

        return False  # default
