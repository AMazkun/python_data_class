import random
import string
from dataclasses import dataclass, field
from enum import StrEnum
import sqlite3
import os

class Role(StrEnum):
    EMPLOYEE = "Employee"
    MANAGER = "Manager"
    SENIOR_MANAGER = "Senior Manager"
    DIRECTOR = "Director"

    @classmethod
    def to_id(cls, role: "Role") -> int:
        """Returns an integer identifier for a given role."""
        return list(cls).index(role)

    @classmethod
    def to_role(cls, id: int) -> "Role":
        """Returns a Role instance from an integer identifier."""
        if 0 <= id < len(cls):
            return list(cls)[id]
        raise ValueError(f"Invalid role ID: {id}")

def generate_id() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=12))


@dataclass
class Person:
    name: str
    address: str
    id: str = field(init=False, default_factory=generate_id)
    role: Role = field(default=Role.EMPLOYEE)  # Explicit default role
    _balance: float = 0.0
    e_mails: list[str] = field(default_factory=list)
    _db_str: str = field(init=False, repr=False)
    active: bool = True

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def bd_str(self):
        return self._db_str

    def withdraw(self, amount):
        if amount < 0 and amount < self._balance:
            raise ValueError(f"Incorrect withdraw amount or insufficient founds {amount} of {self._balance}")
        self._balance -= amount

    def deposit(self, amount):
        if amount < 0 :
            raise ValueError(f"Incorrect deposit amount  {amount}")
        self._balance += amount

    def __post_init__(self):
        mails = ", ".join(self.e_mails)
        role_id = Role.to_id(self.role)

        self._db_str = (
            f"'{self.name}', '{self.address}', '{self.id}', {role_id}, {self._balance}, {int(self.active)}, '{mails}'"
        )

    @classmethod
    def from_db_row(cls, row: tuple) -> "Person":
        """Creates a Person instance from a database row."""
        no, name, address, the_id, role_id, balance, active, emails_str = row
        emails = emails_str.split(", ") if emails_str else []
        role = Role.to_role(role_id)

        new_person = cls(
            name=name,
            address=address,
            role=role,
            _balance=balance if balance is not None else 0.0,  # Handle null balance
            e_mails=emails,
            active=bool(active)
        )
        # Manually set the id (not init)
        new_person.id = the_id
        return new_person

def generate_mock_person() -> Person:
    """Generates a list of mock Person objects."""
    sample_names = ["Alice", "Bob", "Charlie", "Dana", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack"]
    sample_addresses = ["123 Elm St", "456 Oak Ave", "789 Pine Rd", "101 Maple Dr", "202 Birch Ln"]
    sample_emails = ["user1@example.com", "user2@example.com", "user3@example.com"]

    name = random.choice(sample_names)
    address = random.choice(sample_addresses)
    role = random.choice(list(Role))
    emails = random.sample(sample_emails, k=random.randint(1, len(sample_emails)))
    balance = round(random.uniform(500, 5000), 2)
    active = random.choice([True, False])

    person = Person(
        name=name,
        address=address,
        role=role,
        _balance=balance,
        e_mails=emails,
        active=active
    )
    return person

class DatabaseController:
    def __init__(self, db_name: str = "itproger.db"):
        """Initialize the database controller with the given database name."""
        self.db_name = db_name
        if not self._database_exists():
            self._create_table()

    def _database_exists(self) -> bool:
        """Checks if the database file exists."""
        return os.path.exists(self.db_name)

    def _connect(self):
        """Establish and return a connection to the database."""
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        """Creates the staff table if the database does not exist."""
        with self._connect() as db:
            c = db.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS staff (
                name TEXT,
                address TEXT,
                id TEXT PRIMARY KEY,
                role INTEGER,
                balance REAL,
                active INTEGER,
                emails TEXT
            )""")
            db.commit()

    def insert_person(self, person: Person):
        """Inserts a single Person object into the database."""
        with self._connect() as db:
            c = db.cursor()
            c.execute(f"INSERT INTO staff VALUES ({person._db_str})")
            db.commit()

    def insert_multiple(self, persons: list[Person]):
        """Inserts multiple Person objects into the database."""
        with self._connect() as db:
            c = db.cursor()
            for person in persons:
                c.execute(f"INSERT INTO staff VALUES ({person._db_str})")
            db.commit()

    def fetch_staff(self, limit: int = 5, offset: int = 0) -> list[tuple]:
        """Fetches the next set of staff records based on offset."""
        with self._connect() as db:
            c = db.cursor()
            c.execute(f"SELECT rowid, * FROM staff ORDER BY balance LIMIT {limit} OFFSET {offset}")
            return c.fetchall()

    def delete_staff(self, condition: str):
        """Deletes staff entries based on a given condition."""
        with self._connect() as db:
            c = db.cursor()
            c.execute(f"DELETE FROM staff WHERE {condition}")
            db.commit()

    def update_staff(self, set_values: str, condition: str):
        """Updates staff records based on a condition."""
        with self._connect() as db:
            c = db.cursor()
            c.execute(f"UPDATE staff SET {set_values} WHERE {condition}")
            db.commit()

    def delete_table(self):
        """Deletes the staff table from the database."""
        with self._connect() as db:
            c = db.cursor()
            c.execute("DROP TABLE IF EXISTS staff")
            db.commit()
        print("Table 'staff' deleted successfully.")

def insert_staff(db : DatabaseController, count: int = 20) :
    """ Insert moke staff """
    print("\nInsert moke staff")
    for _ in range(count):
        person = generate_mock_person()
        db.insert_person(person)

def single_person_test():
    person = Person(name="Vinlines", address="Oak street 14, Hampton", e_mails=["test@test.com"])
    print(person)
    print(Role.to_id(person.role))
    print(Role.to_role(1))
    person.deposit(100)
    person.withdraw(40)
    print(person)
    print(person.balance)

def db_test():
    db = DatabaseController()
    insert_staff(db)

    print("\nRead moke staff")
    db_items = db.fetch_staff(limit=100)
    for item in db_items:
        print(item)

    persons : list[Person] = []
    print("\nMoke staff - to  persons : list[Person]")
    for row in db_items:
        persons.append(Person.from_db_row(row))

    for person in persons:
        print(person)

    print("\nDelete Moke staff")
    db.delete_staff("1=1")
    print(db.fetch_staff())

if __name__ == "__main__":
    db_test()