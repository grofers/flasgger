import copy


class Path:
    """
    paths:
        /api/endpoint1: ...
        /api/endpoint2: ...
    """

class Api:
    """
    /api/endpoint:
        get: ...
        post: ...
    """


class Operation:
    """
    http_method:
        parameters: ...
        request_body: ...
        responses: ....
    """


class Parameter:
    """
    in: query
    name: parameter
    schema:
        type: integer
    required: true
    """
    class ParamType:
        path = "path"
        query = "query"
        header = "header"

    def __init__(self, mapping):
        self.param_type = mapping['in']
        self.name = mapping['name']
        self.schema_type = mapping['schema']['type']
        self.__mapping = mapping

    def to_schema(self):
        """
        :return: parameter in json schema form
        """
        mapping = self.__mapping
        required_param = [self.name] if mapping.get('required') else []
        schema = Schema(
            self.name, schema_type=self.schema_type, props_map=None, required=required_param
        )
        return schema


class Body:
    """
    request or response body

    description: ...
    content:
        media-type:
            schema:
                ...
    """


class Schema:
    """
    type: object, integer, number, string, boolean, array
    required:
    properties:
        property:
            Schema
    """
    class Type:
        Object = "object"
        Integer = "integer"
        Number = "number"
        String = "string"
        Boolean = "boolean"

    @staticmethod
    def schema_from_mapping(name, mapping):
        return Schema(
            name, mapping.get('type'), mapping.get('properties'), mapping.get('required', [])
        )

    def __init__(self, name, schema_type=None, props_map=None, required=None):
        self.name = name
        self.schema_type = schema_type if schema_type else 'object'
        self.properties = []
        self.required = []

        if self.schema_type == 'object':
            self.properties = self.get_props(props_map)
            self.required = required

    def get_props(self, mapping):
        return [Schema(prop, mapping[prop]) for prop in mapping]

    def serialised(self):
        return {
            "type": self.schema_type,
            "required": self.required,
            "properties": {prop.name : prop.serialised() for prop in self.properties},
        }
