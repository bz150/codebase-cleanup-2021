# import the code we want to test

# TODO: import some code

from app.shopping import to_usd

def test_to_usd():
    assert to_usd(9.5) == "$9.50"