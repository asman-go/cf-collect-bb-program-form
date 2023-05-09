import pydantic
import typing


class Form(pydantic.BaseModel):
    program_name: typing.Optional[str]
    program_site: typing.Optional[str]
    platform: typing.Optional[str]
    in_scope: typing.Optional[str]
    mobile_scope: typing.Optional[str]
    not_paid_scope: typing.Optional[str]
    out_of_scope: typing.Optional[str]
    notes: typing.Optional[str]
