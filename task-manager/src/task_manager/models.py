from pydantic import Field
from typing_extensions import Annotated

# PrimaryKey to limit the range of valid primary keys

PrimaryKey = Annotated[int, Field(gt=0, lt=2147483647)]
