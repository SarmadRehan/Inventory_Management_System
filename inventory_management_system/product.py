class Product:
    def __init__(self, product_id: int, name: str, category: str, price: float, stock_quantity: int, product_sku: str) -> None:
        self.name = name
        self.product_id = product_id
        self.product_sku = product_sku
        self.category = category
        self.price =  price
        self.stock_quantity = stock_quantity

    def __repr__(self) -> str:
        return f"Product(id={self.product_id}, sku='{self.product_sku}', name='{self.name}', price={self.price}, quantity={self.stock_quantity})"
    
    def __str__(self) -> str:
        return f"{self.name} - {self.category} | Price: ${self.price}, Stock: {self.stock_quantity}"
