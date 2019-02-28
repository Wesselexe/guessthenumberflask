from random import randint
from smartninja_nosql.odm import Model


class Player(Model):
    def __init__(self, name, email, secret_number, **kwargs):
        self.name = name
        self.email = email
        self.secret_number = secret_number

        super().__init__(**kwargs)

    def make_secret_number(self):
        self.secret_number = randint(1, 30)
        return self.secret_number
