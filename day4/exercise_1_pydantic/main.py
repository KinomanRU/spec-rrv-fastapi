from pydantic import BaseModel


# 1
def sol_1():
    print("=== Solution 1 ===")
    user_data = {"id": 1, "name": "Иван", "email": "ivan@example.com"}

    class User(BaseModel):
        id: int
        name: str
        email: str

    user = User(**user_data)
    print(f"{user=}")
    user_json = user.model_dump_json()
    print(f"{user_json=}")
    user = User.model_validate_json(user_json)
    print(f"{user=}")


# 2
def sol_2():
    print("=== Solution 2 ===")
    user_data = {"id": 1, "name": "Иван", "email": "ivan@example.com", "age": 30}
    user_data2 = {"id": 2, "name": "Петр", "email": "petr@example.com"}

    class User(BaseModel):
        id: int
        name: str
        email: str
        age: int | None = None

    user = User(**user_data)
    print(f"{user=}")
    user2 = User(**user_data2)
    print(f"{user2=}")


# 3
def sol_3():
    print("=== Solution 3 ===")
    user_data = {
        "id": 1,
        "name": "Иван",
        "email": "ivan@example.com",
        "address": {"street": "Тверская", "city": "Москва", "zip_code": "123456"},
    }

    class Address(BaseModel):
        street: str
        city: str
        zip_code: str

    class User(BaseModel):
        id: int
        name: str
        email: str
        address: Address

    user = User(**user_data)
    print(f"{user=}")
    user_json = user.model_dump_json()
    print(f"{user_json=}")
    user = User.model_validate_json(user_json)
    print(f"{user=}")


# 4
def sol_4():
    print("=== Solution 4 ===")
    order_data = {
        "items": [{"name": "Яблоко", "price": 1.5}, {"name": "Банан", "price": 2.0}]
    }

    class Order(BaseModel):
        name: str
        price: float

    class Orders(BaseModel):
        items: list[Order]

    orders = Orders(**order_data)
    print(f"{orders=}")
    orders_json = orders.model_dump_json()
    print(f"{orders_json=}")
    orders = Orders.model_validate_json(orders_json)
    print(f"{orders=}")


# 5
def sol_5():
    print("=== Solution 5 ===")
    users_data = [
        {"id": 1, "name": "Иван", "email": "ivan@example.com"},
        {"id": 2, "name": "Петр", "email": "petr@example.com"},
    ]

    class User(BaseModel):
        id: int
        name: str
        email: str

    users = [User(**user) for user in users_data]
    print(f"{users=}")


def main():
    sol_1()
    sol_2()
    sol_3()
    sol_4()
    sol_5()


if __name__ == "__main__":
    main()
