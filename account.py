class Account:
    def __init__(self, name, number, cow, field_length):
        self.name = name
        self.number = number
        self.cow_squares_x_1, self.cow_squares_y_1 = cow
        self.field_length = field_length

baby = Account("Baby", 0, cow=[-6, -4], field_length=6)
main = Account("Main", 1, cow=[-1, -4], field_length=8)

account = main
