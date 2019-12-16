header = """class INTEGER:
    def __init__(self, value):
        self.value = value
    def copy(self):
        return INTEGER(self.value)
    def negative(self):
        return INTEGER(-self.value)
    def positive(self):
        return INTEGER(self.value)
"""