from apps.account import models


class AccountRepository:
    model = models.IAMAccount

    def get_account_by_id(self, id):
        return self.model.objects.get(id=id)


class AccountProductsRepository:
    model = models.AccountProducts

    def get_account_products(self, account_id):
        account = account_repository.get_account_by_id(account_id)
        products = self.model.objects.filter(account=account, is_active=True, is_deleted=False)
        return products


account_repository = AccountRepository()
account_products_repository = AccountProductsRepository()
