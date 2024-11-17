from constant import Role
from product_crud_methods import ProductCRUD
from user import User

shared_products = []

users = {
    "admin": {"password": "admin123", "role": Role.ADMIN},
    "user": {"password": "user123", "role": Role.USER}
}

def display_menu(user: User, product_crud: ProductCRUD):
    print("\nMain Menu:")
    print("1. View All Products")
    print("2. Search Product by Name")
    print("3. Search Product by Category")
    print("4. Filter Products by Stock Levels")
    print("5. Make Sale")
    
    if user.role == Role.ADMIN:
        print("6. Add Product")
        print("7. Update Product")
        print("8. Remove Product")
        print("9. Restock Product")
    
    print("10. Check Low Stock")
    print("0. Logout")
    print("S. Switch User")

def handle_menu_choice(choice: str, user: User, product_crud: ProductCRUD):
    if choice == "1":
        products = product_crud.view_all_products()
        if not products:
            print("No products found.")
        for product in products:
            print(str(product))

    elif choice == "2":
        name = input("Enter product name to search: ")
        products = product_crud.search_product_by_name(name)
        if not products:
            print(f"No products found with name containing '{name}'.")
        for product in products:
            print(str(product))

    elif choice == "3":
        category = input("Enter category to search: ")
        products = product_crud.search_products_by_category(category)
        if not products:
            print(f"No products found in category '{category}'.")
        for product in products:
            print(str(product))

    elif choice == "4":
        min_stock = int(input("Enter minimum stock level: "))
        max_stock = input("Enter maximum stock level (press Enter to skip): ")
        max_stock = int(max_stock) if max_stock else None
        products = product_crud.filter_by_stock(min_stock, max_stock)
        if not products:
            print("No products found in the specified stock range.")
        for product in products:
            print(str(product))

    elif choice == "5":
        product_id = int(input("Enter product ID to make a sale: "))
        quantity = int(input("Enter quantity to sell: "))
        success = product_crud.make_sale(product_id, quantity)
        if success:
            print("Sale completed successfully.")
        else:
            print("Failed to complete the sale.")

    elif choice == "6" and user.role == Role.ADMIN:
        sku = input("Enter product SKU: ")
        name = input("Enter product name: ")
        category = input("Enter category: ")
        price = float(input("Enter price: "))
        stock = int(input("Enter stock quantity: "))
        added_product = product_crud.add_product(name, category, price, stock, sku)
        if added_product:
            print(f"Product {name} (ID: {added_product.product_id}) added successfully.")

    elif choice == "7" and user.role == Role.ADMIN:
        product_id = int(input("Enter product ID to update: "))
        name = input("Enter new name (leave blank to skip): ") or None
        price = input("Enter new price (leave blank to skip): ")
        price = float(price) if price else None
        stock = input("Enter new stock quantity (leave blank to skip): ")
        stock = int(stock) if stock else None
        success = product_crud.update_product(product_id, name, price, stock)
        if success:
            print(f"Product ID {product_id} updated successfully.")

    elif choice == "8" and user.role == Role.ADMIN:
        product_id = int(input("Enter product ID to remove: "))
        success = product_crud.remove_product(product_id)
        if success:
            print(f"Product ID {product_id} removed successfully.")

    elif choice == "9" and user.role == Role.ADMIN:
        product_id = int(input("Enter product ID to restock: "))
        quantity = int(input("Enter quantity to add: "))
        success = product_crud.restock_product(product_id, quantity)
        if success:
            print(f"Product ID {product_id} restocked successfully.")

    elif choice == "10":
        low_stock_products = product_crud.check_low_stock()
        if not low_stock_products:
            print("No low-stock products found.")

    elif choice == "0":
        print("Logging out...")
        return "logout"

    elif choice.upper() == "S":
        print("Switching user...")
        return "switch_user"

    else:
        print("Invalid choice or unauthorized access.")
    
    return "continue"

def login():
    print("Welcome to the Inventory Management System Developed by Sarmad Rehan")
    
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users and users[username]["password"] == password:
        print("Login successful!")
        role = users[username]["role"]
        return username, role
    else:
        print("Invalid username or password. Please try again.")
        return None, None

def main():
    while True:
        username, role = None, None
        while not username:
            username, role = login()
        
        user = User(user_id=len(users) + 1, name=username, username=username, password="", role=role)
        print(repr(user))
        product_crud = ProductCRUD(user, shared_products)
        
        while True:
            display_menu(user, product_crud)
            choice = input("Enter your choice: ")
            action = handle_menu_choice(choice, user, product_crud)
            
            if action == "logout":
                break
            elif action == "switch_user":
                username, role = None, None
                break

if __name__ == "__main__":
    main()
