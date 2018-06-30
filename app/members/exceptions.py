__all__ = (
    'BaseRelationException',
    'RelationNotExist',
    'DuplicateRelationException',
)


class BaseRelationException(Exception):

    def __init__(self, from_user, to_user, relation_type):
        self.from_user = from_user,
        self.to_user = to_user,
        self.relation_type = relation_type


class RelationNotExist(BaseRelationException):

    def __str__(self):
        return 'Relation (From: {} To: {} relation_type: {}'.format(
            self.from_user,
            self.to_user,
            self.relation_type
        )


class DuplicateRelationException(BaseRelationException):

    def __str__(self):
        return 'Relation (From: {} To: {} relation_type: {}'.format(
            self.from_user,
            self.to_user,
            self.relation_type
        )
