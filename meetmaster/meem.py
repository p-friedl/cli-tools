import click
from datetime import datetime
import csv


class Protocol:
    def __init__(self):
        self.items = []

    def list_items(self):
        return [item.title for item in self.items]

    def list_items_by_type(self, item_type):
        return [item.title for item in self.items if item.type == item_type]

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_id):
        self.items.pop(item_id)

    def clear(self):
        self.items = []

    def save(self):
        with open('protocol.csv', mode='w') as csv_file:
            csv_file.truncate()
            fieldnames = ['creation_date', 'creation_time', 'type', 'title', 'desc', 'given_by', 'result', 'owner',
                          'priority', 'due']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='|')
            writer.writeheader()

            for item in self.items:
                row = {'creation_date': item.creation_date,
                       'creation_time': item.creation_time,
                       'type': item.type,
                       'title': item.title,
                       'desc': item.desc}

                if item.type == 'information':
                    row['given_by'] = item.given_by
                elif item.type == 'decision':
                    row['result'] = item.result
                elif item.type == 'task':
                    row['owner'] = item.owner
                    row['priority'] = item.priority
                    row['due'] = item.due

                writer.writerow(row)

    def load(self):
        try:
            with open('protocol.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter='|')

                for index, row in enumerate(csv_reader):
                    if index != 0:
                        if row['type'] == 'information':
                            item = Information(row['title'], row['desc'], row['given_by'])
                        if row['type'] == 'decision':
                            item = Decision(row['title'], row['desc'], row['result'])
                        if row['type'] == 'task':
                            item = Task(row['title'], row['desc'], row['owner'], row['priority'], row['due'])
                        item.creation_date = row['creation_date']
                        item.creation_time = row['creation_time']
                        self.add_item(item)
        except IOError:
            # If not exists, create the file
            csv_file = open('protocol.csv', 'w+')
            csv_file.close()


class ProtocolItem:
    def __init__(self, title, desc):
        timestamp = datetime.now()
        self.creation_date = "{}/{}/{}".format(timestamp.day, timestamp.month, timestamp.year)
        self.creation_time = "{}:{}:{}".format(timestamp.hour, timestamp.minute, timestamp.second)
        self.title = title
        self.desc = desc


class Information(ProtocolItem):
    def __init__(self, title, desc, given_by):
        super().__init__(title, desc)
        self.given_by = given_by
        self.type = "Information"


class Decision(ProtocolItem):
    def __init__(self, title, desc, result):
        super().__init__(title, desc)
        self.result = result
        self.type = "Decision"


class Task(ProtocolItem):
    def __init__(self, title, desc, owner, priority, due):
        super().__init__(title, desc)
        self.owner = owner
        self.priority = priority
        self.due = due
        self.type = "Task"


@click.group()
def cli():
    pass


@cli.command()
def show():
    protocol = Protocol()
    protocol.load()
    click.echo(protocol.list_items())


@cli.command()
@click.option('-i', 'item_type', flag_value='information')
@click.option('-d', 'item_type', flag_value='decision')
@click.option('-t', 'item_type', flag_value='task')
@click.argument('title')
def add(item_type, title):
    protocol = Protocol()
    protocol.load()
    if item_type == "information":
        desc = click.prompt('Description', type=str)
        given_by = click.prompt('Information Provider', type=str)
        item = Information(title, desc, given_by)
        protocol.add_item(item)
    protocol.save()


if __name__ == '__main__':
    cli()
