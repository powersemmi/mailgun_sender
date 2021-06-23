from typing import List, Literal
from pydantic import BaseModel, Field


class MailArgs(BaseModel):
    host: Literal['send.reffection.com', 'post.alphastream.ru'] = (
        Field(title="Host",
              description="Host")
        )
    to: List[str] = Field(title="Subjects Emails",
                          description="Subjects Emails")
    subject: str = Field(title="Email subject",
                         description="Email subject")
    body: str = Field(title="Body of Email",
                      description="Subjects Email")
    concat_type: Literal['inline', 'attach'] = Field(
        default='attach',
        title="How to concat data to Email",
        description="How to concat data to Email\n"
                    "Maybe: inline|attach")
    table: Literal['mailgun_send', 'test'] = Field(
                                        title="Name of table",
                                        description="Name of table\n"
                                                    "Example: mailgun_send")
    fields: List[str] = Field(title="List of fields",
                              description="List of fields")
    limit: int = Field(title="Row count",
                       description="Row count\n"
                                   "Number of row to send to client")
