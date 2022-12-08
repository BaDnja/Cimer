from humps.camel import case
from pydantic import BaseModel as PydanticBaseModel


class BaseModelSchema(PydanticBaseModel):

    class Config:
        alias_generator = case
        allow_population_by_field_name = True
