from ..models import APITokenModel
from django.db import transaction

class GenerateApiKeyService:

    def __init__(self, user):
        self.user = user
        print(self.user)

    # def execute(self):
    #     token = self.get_existing_token()

    #     if token:
    #         pass

    #     else:
    #         pass


    def get_existing_token(self):
        return APITokenModel.objects.filter(user=self.user).first()

    @transaction.atomic()
    def execute(self):
        existing_token = (APITokenModel.objects
                        .select_for_update()
                        .filter(user=self.user)
                        .first())
        # existing_token = self.get_existing_token()
        if existing_token:
            # print(existing_token)
            existing_token.delete() 

        obj = APITokenModel(user=self.user)
        api_key = obj.generate_token()

        return api_key
