from typing import List, Any, Dict, Optional

from ninja import Schema
from pydantic import UUID4


class SkiiRecordContract(Schema):
    data: Any


class SkiiListContract(Schema):
    data: List[Any] = []


class SkiiMsgContract(Schema):
    message: str


class IdentifierContract(Schema):
    pk: Optional[UUID4]
    class Config:
        fields = {}


class SkiiIdentifierContract(Schema):
    data: IdentifierContract


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