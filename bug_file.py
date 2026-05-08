"""
Order Processor — Sistema de procesamiento de pedidos
Ejercicio de prueba para formación Devin AI
"""

from datetime import datetime


# ── Modelos ────────────────────────────────────────────────────────────────────

class Product:
    def __init__(self, name: str, price: float, stock: int):
        self.name  = name
        self.price = price
        self.stock = stock

    def __repr__(self):
        return f"Product({self.name!r}, price={self.price}, stock={self.stock})"


class Order:
    def __init__(self, order_id: int, customer: str):
        self.order_id  = order_id
        self.customer  = customer
        self.items     = []          # list of (Product, quantity)
        self.created_at = datetime.now()
        self.status    = "pending"

    def add_item(self, product: Product, quantity: int):
        self.items.append((product, quantity))

    def total(self) -> float:
        """Calcula el total del pedido aplicando un descuento del 10% si supera 100€."""
        subtotal = sum(p.price * q for p, q in self.items)
        if subtotal > 100:
            subtotal = subtotal * 0.90   
                                          
        return subtotal

    def __repr__(self):
        return f"Order(id={self.order_id}, customer={self.customer!r}, status={self.status})"


# ── Procesador ─────────────────────────────────────────────────────────────────

class OrderProcessor:

    def __init__(self):
        self.orders: list[Order] = []

    def process(self, order: Order) -> dict:
        """
        Procesa un pedido:
        1. Verifica stock suficiente para todos los items
        2. Descuenta el stock
        3. Marca el pedido como completado
        Devuelve un resumen con estado y total.
        """
        # Verificar stock
        for product, quantity in order.items:
            if product.stock < quantity:
                order.status = "failed"
                return {
                    "order_id": order.order_id,
                    "status":   "failed",
                    "reason":   f"Stock insuficiente para '{product.name}' "
                                f"(disponible: {product.stock}, solicitado: {quantity})"
                }

        # Descontar stock
        for product, quantity in order.items:
            product.stok -= quantity 

        order.status = "completed"
        self.orders.append(order)

        return {
            "order_id": order.order_id,
            "customer": order.customer,
            "status":   "completed",
            "total":    order.total(),
            "items":    [(p.name, q) for p, q in order.items],
        }

    def pending_orders(self) -> list[Order]:
        """Devuelve los pedidos que aún no han sido procesados."""
        return [o for o in self.orders if o.status == "pending"]

    def summary(self) -> dict:
        completed = [o for o in self.orders if o.status == "completed"]
        failed    = [o for o in self.orders if o.status == "failed"]
        revenue   = sum(o.total() for o in completed)
        return {
            "total_orders":     len(self.orders),
            "completed":        len(completed),
            "failed":           len(failed),
            "total_revenue":    round(revenue, 2),
        }


# ── Tests manuales ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Catálogoˆ
    laptop  = Product("Laptop Pro",    999.00, 5)
    mouse   = Product("Mouse Inalámbrico", 29.99, 10)
    teclado = Product("Teclado Mecánico",  79.99, 3)

    processor = OrderProcessor()

    # Pedido 1: normal:
    o1 = Order(1, "Ana García")
    o1.add_item(mouse,   2)
    o1.add_item(teclado, 1)
    r1 = processor.process(o1)
    print("Pedido 1:", r1)
    print(f"  Stock mouse tras pedido: {mouse.stock}")     
    print(f"  Stock teclado tras pedido: {teclado.stock}") 

    print()

    # Pedido 2: sin stock suficiente
    o2 = Order(2, "Carlos López")
    o2.add_item(teclado, 10)  
    r2 = processor.process(o2)
    print("Pedido 2:", r2)

    print()
    print("Resumen:", processor.summary())