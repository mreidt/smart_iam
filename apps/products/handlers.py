from rest_framework import exceptions

from apps.products.repositories import products_repository


class ProductsHandlers(object):
    def delete_product(self, product_id: int) -> None:
        product = products_repository.get_product_by_id(product_id)

        if product.is_active:
            raise exceptions.PermissionDenied("Cannot delete active product.")

        products_repository.delete(product)


products_handler = ProductsHandlers()
