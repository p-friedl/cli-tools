import click
from datetime import datetime
import csv


class Protocol:
    """
    Protocol class that contains the protocol items
    """
    def __init__(self):
        self.items = []

    def list_items(self):
        """
        List all protocol items
        """
        click.echo("ID --|-- Item Title")
        for index, item in enumerate(self.items):
            click.echo(" {} --|-- {}".format(index, item.title))

    def list_items_by_type(self, item_type):
        """
        List protocol items by a specific type
        """
        click.echo("ID --|-- Item Title")
        for index, item in enumerate(self.items):
            if item.type.lower() == item_type.lower():
                click.echo(" {} --|-- {}".format(index, item.title))

    def add_item(self, item):
        """
        add a protocol item
        """
        self.items.append(item)

    def remove_item(self, item_id):
        """
        remove a protocol item
        """
        self.items.pop(item_id)

    def clear(self):
        """
        delete the protocol
        """
        self.items = []

    def save(self):
        """
        save the protocol to a CSV file
        """
        with open("protocol.csv", mode="w") as csv_file:
            csv_file.truncate()
            fieldnames = ["creation_date", "creation_time", "type", "title", "desc", "given_by", "result", "owner",
                          "priority", "due"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="|")
            writer.writeheader()

            for item in self.items:
                row = {"creation_date": item.creation_date,
                       "creation_time": item.creation_time,
                       "type": item.type,
                       "title": item.title,
                       "desc": item.desc}

                if item.type == "Information":
                    row["given_by"] = item.given_by
                elif item.type == "Decision":
                    row["result"] = item.result
                elif item.type == "Task":
                    row["owner"] = item.owner
                    row["priority"] = item.priority
                    row["due"] = item.due

                writer.writerow(row)

    def load(self):
        """
        load the protocol from a CSV file
        """
        try:
            with open("protocol.csv", mode="r") as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter="|")

                for index, row in enumerate(csv_reader):
                    if index != "0":
                        if row["type"] == "Information":
                            item = Information(row["title"], row["desc"], row["given_by"])
                        if row["type"] == "Decision":
                            item = Decision(row["title"], row["desc"], row["result"])
                        if row["type"] == "Task":
                            item = Task(row["title"], row["desc"], row["owner"], row["priority"], row["due"])
                        item.creation_date = row["creation_date"]
                        item.creation_time = row["creation_time"]
                        self.add_item(item)
        except IOError:
            # create the file if it doesn't exist yet
            csv_file = open("protocol.csv", "w+")
            csv_file.close()


class ProtocolItem:
    """
    Protocol item base class
    """
    def __init__(self, title, desc):
        timestamp = datetime.now()
        self.creation_date = "{}/{}/{}".format(timestamp.day, timestamp.month, timestamp.year)
        self.creation_time = "{}:{}:{}".format(timestamp.hour, timestamp.minute, timestamp.second)
        self.title = title
        self.desc = desc


class Information(ProtocolItem):
    """
    Protocol item class of type Information
    """
    def __init__(self, title, desc, given_by):
        super().__init__(title, desc)
        self.given_by = given_by
        self.type = "Information"


class Decision(ProtocolItem):
    """
    Protocol item class of type Decision
    """
    def __init__(self, title, desc, result):
        super().__init__(title, desc)
        self.result = result
        self.type = "Decision"


class Task(ProtocolItem):
    """
    Protocol item class of type Task
    """
    def __init__(self, title, desc, owner, priority, due):
        super().__init__(title, desc)
        self.owner = owner
        self.priority = priority
        self.due = due
        self.type = "Task"


# Group CLI commands
@click.group()
def cli():
    pass


# Command to show all protocol items or specific ones per type
@cli.command()
@click.option("-t", "item_type", type=click.Choice(["information", "decision", "task"], case_sensitive=False))
def show(item_type):
    protocol = Protocol()
    protocol.load()
    if item_type:
        protocol.list_items_by_type(item_type)
    else:
        protocol.list_items()


# Command to add a new protocol item
@cli.command()
@click.option("-i", "item_type", flag_value="Information")
@click.option("-d", "item_type", flag_value="Decision")
@click.option("-t", "item_type", flag_value="Task")
@click.argument("title", nargs=-1)
def add(item_type, title):
    if item_type:
        protocol = Protocol()
        protocol.load()
        title = " ".join(title)
        desc = click.prompt("Description", type=str)

        if item_type == "Information":
            given_by = click.prompt("Information Provider", type=str)
            item = Information(title, desc, given_by)
        elif item_type == "Decision":
            result = click.prompt("Decision Result", type=str)
            item = Decision(title, desc, result)
        elif item_type == "Task":
            owner = click.prompt("Task Owner", type=str)
            priority = click.prompt("Task Priority", type=str)
            due = click.prompt("Task Due Date", type=str)
            item = Task(title, desc, owner, priority, due)

        protocol.add_item(item)
        protocol.save()
    else:
        click.echo("Invalid: please provide a valid option parameter")


# Command to delete a specific protocol item by ID
@cli.command()
@click.confirmation_option(prompt="Are you sure you want to delete the chosen protocol item?")
@click.argument("item_id", type=click.INT)
def remove(item_id):
    protocol = Protocol()
    protocol.load()
    if item_id > len(protocol.items) - 1:
        click.echo("Invalid: the ID does not exist and therefore the item can't be deleted")
    else:
        protocol.remove_item(item_id)
        protocol.save()


# Command to delete the whole protocol
@cli.command()
@click.confirmation_option(prompt="Are you sure you want to delete the chosen protocol item?")
def delete():
    protocol = Protocol()
    protocol.load()
    protocol.clear()
    protocol.save()


if __name__ == "__main__":
    cli()
