from apps.products import models


class ProductsRepository:
    model = models.Products

    def get_product_by_id(self, id):
        return self.model.objects.get(id=id)


products_repository = ProductsRepository()
