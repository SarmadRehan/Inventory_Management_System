from typing import List, Optional
import constant as const
from product import Product
from user import User

class ProductCRUD:
    def __init__(self, user: User, shared_products: List[Product], low_stock_threshold=const.LOW_STOCK_THRESHOLD) -> None:
        self.products: List[Product] = shared_products
        self.low_stock_threshold: int = low_stock_threshold
        self.user = user

    def add_product(self, name: str, category: str, price: float, stock_quantity: int, product_sku: str) -> Optional[Product]:
        if self.user.role != const.Role.ADMIN:
            print("Error: Only admins can add products.")
            return None

        product_id = max((product.product_id for product in self.products), default=0) + 1
        product_exists = any(product.product_sku == product_sku for product in self.products)

        if product_exists:
            print(f"Error: The SKU '{product_sku}' is already in use.")
            return None

        new_product = Product(product_id, name, category, price, stock_quantity, product_sku)
        self.products.append(new_product)
        print(f"Product '{name}' added successfully with ID: {product_id}")
        return new_product

    
    def get_product(self, product_id: int) -> Optional[Product]:
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def update_product(self, product_id: int, name: Optional[str] = None, price: Optional[float] = None, stock_quantity: Optional[int] = None) -> bool:
        if self.user.role != const.Role.ADMIN:
            print("Error: Only admins can update products.")
            return False

        product = self.get_product(product_id)
        if not product:
            print(f"Error: No product found with ID {product_id}.")
            return False

        if name is not None:
            product.name = name
        if price is not None:
            product.price = price
        if stock_quantity is not None:
            product.stock_quantity = stock_quantity

        print(f"Product ID {product_id} updated successfully.")
        return True


    def remove_product(self, product_id: int) -> bool:
        if self.user.role != const.Role.ADMIN:
            print("Error: Only admins can remove products.")
            return False

        product = self.get_product(product_id)
        if not product:
            print(f"Error: No product found with ID {product_id}.")
            return False

        self.products.remove(product)
        print(f"Product ID {product_id} removed successfully.")
        return True

    def view_all_products(self) -> List[Product]:
        return self.products

    def search_product_by_name(self, product_name: str) -> List[Product]: 
        return [product for product in self.products if product_name.lower() in product.name.lower()]

    def search_products_by_category(self, product_category: str) -> List[Product]: 
        return [product for product in self.products if product_category.lower() == product.category.lower()]

    def filter_by_stock(self, min_stock: int = const.MIN_STOCK, max_stock: Optional[int] = None) -> List[Product]:
        if max_stock is None:
            return [product for product in self.products if product.stock_quantity >= min_stock]
        else:
            return [product for product in self.products if min_stock <= product.stock_quantity <= max_stock]

    def restock_product(self, product_id: int, quantity: int) -> bool:
        if self.user.role != const.Role.ADMIN:
            print("Error: Only admins can restock products.")
            return False

        product = self.get_product(product_id)
        if not product:
            print(f"Error: No product found with ID {product_id}.")
            return False

        if quantity <= 0:
            print("Error: Restock quantity must be greater than 0.")
            return False

        product.stock_quantity += quantity
        print(f"Product ID {product_id} restocked successfully. New stock: {product.stock_quantity}")
        return True

    def make_sale(self, product_id: int, quantity: int) -> bool:
        if quantity <= 0:
            print("Error: Sale quantity must be greater than 0.")
            return False

        product = self.get_product(product_id)
        if not product:
            print(f"Error: No product found with ID {product_id}.")
            return False

        if product.stock_quantity < quantity:
            print(f"Error: Insufficient stock for '{product.name}'. Available stock: {product.stock_quantity}.")
            return False

        product.stock_quantity -= quantity
        print(f"Sale completed successfully. '{product.name}' stock reduced by {quantity}. New stock: {product.stock_quantity}.")
        return True


    def check_low_stock(self) -> List[Product]:
        low_stock_products = [product for product in self.products if product.stock_quantity <= self.low_stock_threshold]
        if low_stock_products:
            print("Warning: The following products are low in stock and may need restocking:")
            for product in low_stock_products:
                print(f"{product.name} (SKU: {product.product_sku}) - Stock: {product.stock_quantity}")
        return low_stock_products
