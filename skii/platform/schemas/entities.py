from ninja import ModelSchema

from skii.platform.entities import RecordIdentityHistory


class RecordIdentityHistotyContract(ModelSchema):
    class Config:
        model = RecordIdentityHistory
        model_fields = ["created", "last_modified"]
