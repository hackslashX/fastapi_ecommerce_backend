from crud.schemas import Category, CategoryCreate


class CreateCategoryRequest(CategoryCreate):
    ...


class CreateCategoryResponse(Category):
    ...
