"""
Discounts API — Endpoint para consultar descuentos disponibles
"""

from datetime import date
from enum import Enum

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(
    title="Descuentos API",
    description="API para consultar los descuentos disponibles",
    version="1.0.0",
)


# -- Modelos ------------------------------------------------------------------

class DiscountType(str, Enum):
    percentage = "percentage"
    fixed = "fixed"


class Discount(BaseModel):
    id: int
    code: str
    description: str
    discount_type: DiscountType
    value: float
    min_order_amount: float | None = None
    start_date: date
    end_date: date
    active: bool


# -- Datos de ejemplo ---------------------------------------------------------

DISCOUNTS: list[Discount] = [
    Discount(
        id=1,
        code="WELCOME10",
        description="10% de descuento en tu primera compra",
        discount_type=DiscountType.percentage,
        value=10.0,
        min_order_amount=None,
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        active=True,
    ),
    Discount(
        id=2,
        code="SUMMER25",
        description="25% de descuento en productos de verano",
        discount_type=DiscountType.percentage,
        value=25.0,
        min_order_amount=50.0,
        start_date=date(2025, 6, 1),
        end_date=date(2025, 8, 31),
        active=True,
    ),
    Discount(
        id=3,
        code="FLAT5",
        description="5 EUR de descuento en pedidos superiores a 30 EUR",
        discount_type=DiscountType.fixed,
        value=5.0,
        min_order_amount=30.0,
        start_date=date(2025, 3, 1),
        end_date=date(2025, 12, 31),
        active=True,
    ),
    Discount(
        id=4,
        code="BLACKFRIDAY",
        description="30% de descuento por Black Friday",
        discount_type=DiscountType.percentage,
        value=30.0,
        min_order_amount=100.0,
        start_date=date(2025, 11, 28),
        end_date=date(2025, 11, 30),
        active=False,
    ),
]


# -- Endpoints ----------------------------------------------------------------

@app.get("/discounts", response_model=list[Discount])
def list_discounts(
    active: bool | None = Query(None, description="Filtrar por estado activo/inactivo"),
    discount_type: DiscountType | None = Query(None, description="Filtrar por tipo de descuento"),
) -> list[Discount]:
    """Devuelve la lista de descuentos disponibles con filtros opcionales."""
    results = DISCOUNTS

    if active is not None:
        results = [d for d in results if d.active == active]

    if discount_type is not None:
        results = [d for d in results if d.discount_type == discount_type]

    return results


@app.get("/discounts/{discount_id}", response_model=Discount)
def get_discount(discount_id: int) -> Discount:
    """Devuelve un descuento por su ID."""
    for discount in DISCOUNTS:
        if discount.id == discount_id:
            return discount

    raise HTTPException(status_code=404, detail="Descuento no encontrado")
