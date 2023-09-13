from typing import List, Any, Dict

from ninja import Schema
from pydantic import conint


class SkiiResponse(Schema):
    data: Any | None


class SkiiListResponse(Schema):
    data: List[Any] = []
    count: conint(gt=0)


class MsgResponseContract(Schema):
    """A response with a text message

    Args:
        message (str): the text message

    Example:
        ::

        {
            "message": "The message"
        }
    """

    message: str


class FormInvalidResponseContract(Schema):
    """Form errors dict provided by Django from form validation

    Args:
        errors (Dict[str, List[Dict[str, Any]]]): a Django form errors dict

    Example:
        ::

        {
            "errors": {
                'password2': [
                    {
                        'message': 'The two password fields didn’t match.',
                        'code': 'password_mismatch'
                    }
                ]
            }
        }
    """

    errors: Dict[str, List[Dict[str, Any]]]