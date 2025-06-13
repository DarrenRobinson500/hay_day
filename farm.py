from animals import *

print_messages = False

class Action:
    def __init__(self, farm, type, item, time):
        time = int(time)
        self.type = type
        self.item = item
        self.time = time
        # print("Action made:", self)
        farm.time_list[time] = farm.time_list[int(time)] + [self]

    def __str__(self):
        return f"Time: {self.time} {self.type} {self.item}"

class Farm:
    def __init__(self):
        self.production_dict = {}
        self.resource_dict = {}
        self.coins = 0
        self.time = 0
        self.time_limit = 60 * 16
        self.time_list = [[]] * 60 * 24
        self.messages = []
        self.set_parameters()
        self.set_starting_position()

    # Utilities
    def set_parameters(self):
        for item in items:
            item.set(2, 4)
            if item.production == field:
                item.set(10, 20)

    def set_starting_position(self):
        for production_unit in production_units:
            self.production_dict[production_unit] = production_unit.count
        for item in items:
            self.resource_dict[item] = 0
            if item.production == field:
                self.resource_dict[item] = 30

    def print_position(self):
        print()
        print("Production Units")
        for production, count in self.production_dict.items():
            print(f"  {production}: {count}")
        print()
        print("Resources")
        for item, count in self.resource_dict.items():
            if count > 0: print(f"  {item}: {count}")

    def print_time_list(self):
        print("\nActions")
        for time in self.time_list:
            for action in time:
                print(action)

    def print_messages(self):
        if not print_messages: return
        message_dict = {}
        for message in self.messages:
            message_dict[message] = message_dict.get(message, 0) + 1
        for message, count in message_dict.items():
            if count == 1:
                print(message)
            else:
                print(f"{message} x {count}")
        self.messages = []

    # Run
    def run(self, priority_list):
        while self.time < self.time_limit:
            # Make priority items
            for priority in priority_list:
                can_make = True
                while can_make:
                    can_make = self.make_item(priority)
            # Perform Actions
            self.perform_actions()
            self.sell_excess()

            self.time += 1
            self.print_messages()
            # print("\nTIME:", self.time)
            # self.print_position()

    def make_item(self, item):
        ready_to_make = True
        # print("Item ingredients", item, item.ingredients, type(item.ingredients))
        for ingredient, count in item.ingredients.items():
            if self.resource_dict[ingredient] < count:
                ready_to_make = False
                self.make_item(ingredient)
        if item.production == field and self.resource_dict[item] == 0:
            # print(f"No {item}s left")
            ready_to_make = False
        if self.production_dict[item.production] == 0:
            # print(f"No {item.production}s left")
            ready_to_make = False

        if ready_to_make:
            self.consume_ingredients(item)
            Action(farm=self, type="Finished", item=item, time=self.time + item.creation_time)
            message = f"Time {self.time}: Starting {item}. Remaining {item.production} = {self.production_dict[item.production]}"
            self.messages.append(message)
            return True

    def consume_ingredients(self, item):
        for ingredient, count in item.ingredients.items():
            self.resource_dict[ingredient] -= count
        if item.production == field: self.resource_dict[item] -= 1
        self.production_dict[item.production] -= 1

    def perform_actions(self):
        actions = self.time_list[self.time]
        if actions:
            # print(self.time)
            for action in actions:
                if action.type == "Finished":
                    # Add created resources
                    self.resource_dict[action.item] += 1
                    if action.item.production == field: self.resource_dict[action.item] += 1
                    # Release the production
                    self.production_dict[action.item.production] += 1
                    # Message
                    message = f"Time {self.time}: Finished {action.item} {self.resource_dict[action.item]}"
                    self.messages.append(message)

    def sell_excess(self):
        for item in items:
            excess = int(self.resource_dict[item] - item.max)
            if excess > 0:
                self.resource_dict[item] -= excess
                self.coins += excess * item.price
                message = f"Time {self.time}: Selling {excess} x {item}. Coins up {excess * item.price} to {self.coins}."
                self.messages.append(message)




# priorities = [("Wheat", [wheat]), ("Sugar cane", [sugar_cane]), ("Sugar cane and Animals", [sugar_cane, eggs, milk, bacon, wool]), ("Sugar cane and Bacon", [sugar_cane, bacon])]
# for name, priority in priorities:
#     farm = Farm()
#     farm.run(priority)
#     print(f"Priority: {name}. End coins: {farm.coins:,} at t={farm.time_limit}")
    # print(farm.print_time_list())
# farm.print_time_list()
