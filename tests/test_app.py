from project.helpers import priv_convert

class TestClass:
    def test_one(self):
        one = priv_convert("False")
        assert one == False

    def test_two(self):
        two = priv_convert("True")
        assert two == True