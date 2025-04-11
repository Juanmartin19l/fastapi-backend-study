from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Producto no encontrado"}},
)


class Product(BaseModel):
    id: int
    name: str
    quantity: int


products_list = [
    Product(id=1, name="Laptop", quantity=10),
    Product(id=2, name="Mouse", quantity=50),
    Product(id=3, name="Keyboard", quantity=30),
    Product(id=4, name="Monitor", quantity=20),
    Product(id=5, name="Printer", quantity=15),
]


# GET ALL PRODUCTS
@router.get("/")
async def get_products():
    return products_list


# GET BY ID
@router.get("/{id}")
async def get_product(id: int):
    product = search_product(id)
    if product is None:
        raise HTTPException(
            status_code=404, detail=f"Producto con id {id} no encontrado"
        )
    return product


# POST
@router.post("/", status_code=201)
async def post_product(product: Product):
    if isinstance(search_product(product.id), Product):
        raise HTTPException(
            status_code=400,
            detail=f"El producto con id {product.id} ya existe en la lista",
        )

    # Verificar si ya existe un producto con el mismo nombre
    for existing_product in products_list:
        if existing_product.name == product.name:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un producto con el nombre '{product.name}'",
            )

    products_list.append(product)
    return product


# PUT
@router.put("/")
async def put_product(product: Product):
    found = False
    for index, saved_product in enumerate(products_list):
        if saved_product.id == product.id:
            products_list[index] = product
            found = True
            break

    if not found:
        raise HTTPException(
            status_code=404, detail=f"Producto con id {product.id} no encontrado"
        )

    return {"actualizado": product}


# DELETE
@router.delete("/{id}")
async def delete_product(id: int):
    found = False
    for index, saved_product in enumerate(products_list):
        if saved_product.id == id:
            del products_list[index]
            found = True
            break

    if not found:
        raise HTTPException(
            status_code=404, detail=f"Producto con id {id} no encontrado"
        )

    return {"message": f"Se ha borrado el producto con id: {id}"}


# Search Product
def search_product(id: int):
    products = filter(lambda product: product.id == id, products_list)
    try:
        return list(products)[0]
    except IndexError:
        return None
