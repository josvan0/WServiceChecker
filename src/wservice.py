class WService:
    def __init__(self, name, description, startup):
        self.name = name
        self.description = description
        self.startup = startup

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def startup(self):
        return self._startup

    @name.setter
    def name(self, value):
        self._name = value

    @description.setter
    def description(self, value):
        self._description = value

    @startup.setter
    def startup(self, value):
        self._startup = value
