from apps.products import models


class ProductsRepository:
    model = models.Products

    def get_product_by_id(self, id: int) -> models.Products:
        return self.model.objects.get(id=id)

    def delete(self, product: models.Products) -> None:
        product.delete()


products_repository = ProductsRepository()
