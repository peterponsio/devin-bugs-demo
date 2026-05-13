"""Shop API — Discount endpoint."""

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Shop API")


@app.get("/discount")
def get_discount(
    price: float = Query(..., gt=0, description="Original price"),
    percent: int = Query(..., ge=0, description="Discount percentage (0-100)"),
):
    if percent > 100:
        raise HTTPException(status_code=400, detail="percent must be <= 100")

    discount_amount = round(price * percent / 100, 2)

    commission = 0.0
    if price > 500 and percent >= 30:
        commission = round(discount_amount * 0.02, 2)

    final_price = round(price - discount_amount + commission, 2)

    return {
        "original": price,
        "discount": discount_amount,
        "commission": commission,
        "final": final_price,
    }
