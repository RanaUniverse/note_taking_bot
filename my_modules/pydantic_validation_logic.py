"""
No Use Of This Module ❌❌❌

I Still not get where i will use this,
I am not sure how i can use this, i just kept this module
Just for future using Reference.
This module will have some validataion logic i will make and use in my projects
"""

from pydantic import BaseModel, Field, EmailStr, ValidationError

from faker import Faker

fake = Faker()


class UserEmailValidate(BaseModel):
    """
    This Email is just my own wish of what i want
    """

    email: EmailStr = Field(min_length=10)


def main():
    """Just for checking"""
    user_email_from_input = "a@d.com"

    try:
        email_instance = UserEmailValidate(email=user_email_from_input)
        output_email = email_instance.email
        print("Valid Email:", output_email)

    except ValidationError as e:
        fake_email = fake.email()
        print("Validation Error:", e)
        print("So, a new email is being assigned for you.")
        email_instance = UserEmailValidate(email=fake_email)
        print(f"Your new email is: {email_instance.email}")


if __name__ == "__main__":
    print("Somehign")
    main()
