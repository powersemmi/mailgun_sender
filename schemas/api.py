"""
TODO: Add schedule for api senders
"""

from typing import List, Literal
from pydantic import BaseModel, Field
from pydantic.types import Json


class ApiArgs(BaseModel):
    to: str = Field(title="Client api url",
                    description="Client Email")
    request_type: Literal["POST", "GET", "DELITE", "UPDATE", "PUT"]
    request_headers: Json = Field(title="Request headers",
                                  description="Request headers")
    table: str = Field(title="Path to date in DB",
                       description="Path to date in DB\n"
                                   "Example: mydb.mytable")
    cols: List[str] = Field(title="List of cols",
                            description="List of cols")
    rownum: int = Field(title="Row count",
                        description="Row count\n"
                                    "Number of row to send to client")
