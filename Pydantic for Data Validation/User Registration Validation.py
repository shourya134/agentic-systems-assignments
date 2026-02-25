from pydantic import BaseModel, EmailStr,Field,ValidationError

class UserRegister(BaseModel):
    username: str = Field(min_length=5,description="Provide user name")
    email: EmailStr = Field(description="Provide user email")
    age: int = Field(ge=18,description="Provide user age")

# Demonstration of validation
if __name__ == "__main__":

    test_data = [
        {"username": "johndoe", "email": "john@example.com", "age": 25},    # Valid
        {"username": "john", "email": "john@example.com", "age": 25},       # Invalid username (< 5)
        {"username": "johndoe", "email": "invalid-email", "age": 25},      # Invalid email
        {"username": "johndoe", "email": "john@example.com", "age": 17},    # Invalid age (< 18)
    ]

    for data in test_data:
        try:
            user = UserRegister(**data)
            print(f" Success: {user}")
        except ValidationError as e:
            print(f" Validation Error for {data['username'] if 'username' in data else 'unknown'}:")
            for error in e.errors():
                print(error)
