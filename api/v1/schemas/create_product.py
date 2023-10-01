from crud.schemas import Product, ProductCreate


class CreateProductRequest(ProductCreate):
    ...


class CreateProductResponse(Product):
    ...
