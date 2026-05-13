"""
API REST — Endpoints de utilidad
"""

from fastapi import FastAPI, Query

app = FastAPI(title="Devin Bugs Demo API")


@app.get("/discount")
def get_discount(
    price: float = Query(..., gt=0, description="Precio original del producto"),
    percent: float = Query(..., ge=0, le=100, description="Porcentaje de descuento a aplicar"),
):
    """Devuelve el precio con el descuento aplicado."""
    discount_amount = price * (percent / 100)
    final_price = round(price - discount_amount, 2)
    return {
        "original_price": price,
        "discount_percent": percent,
        "discount_amount": round(discount_amount, 2),
        "final_price": final_price,
    }
