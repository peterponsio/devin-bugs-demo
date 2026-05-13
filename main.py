from fastapi import FastAPI, Query, HTTPException

app = FastAPI(title="Shop API")


@app.get("/discount")
def get_discount(
    price: float = Query(..., gt=0, description="Original price"),
    percent: int = Query(..., ge=0, description="Discount percentage (0-100)"),
):
    if percent > 100:
        raise HTTPException(status_code=400, detail="percent must not exceed 100")

    discount = round(price * percent / 100, 2)
    final = round(price - discount, 2)

    return {"original": price, "discount": discount, "final": final}
