import pytest

def test_equal_or_not_equal():
    assert 2 == 2, "1 is not equal to 2"

def test_is_istance():
    assert isinstance(1, int)
    assert isinstance(1.0, float), "1.0 is not an int"

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'hello') is True, "hello is not equal to hello"

def test_type():
    assert type(1) == int
    assert type(1.0) == float
    assert type("hello") == str

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student("John", "Doe", "Computer Science", 3)

def test_person_initializzation(default_employee):
    assert default_employee.first_name == "John", "First name is not John"
    assert default_employee.last_name == "Doe", "Last name is not Doe"
    assert default_employee.major == "Computer Science", "Major is not Computer Science"
    assert default_employee.years == 3, "Years is not 3"