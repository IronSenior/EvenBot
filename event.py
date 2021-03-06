class Event:
    def __init__(self, date, tag, name, group, locX, locY, description, image):
        self.date = date
        self.tag = tag
        self.name = name
        self.group = group
        self.locX = locX
        self.locY = locY
        self.description = description
        self.image = image

    # GETTERS
    @property
    def date(self):
        return self.date

    @property
    def tag(self):
        return self.tag

    @property
    def name(self):
        return self.name

    @property
    def group(self):
        return self.group

    @property
    def location(self):
        return self.locX, self.locY

    @property
    def description(self):
        return self.description

    @property
    def image(self):
        return self.image

    # SETTERS

    @date.setter
    def date(self, date):
        self.date = date

    @tag.setter
    def tag(self, tag):
        self.tag = tag

    @name.setter
    def name(self, name):
        self.name = name

    @group.setter
    def group(self, group):
        self.group = group

    @location.setter
    def location(self, x, y):
        self.locX = x
        self.locY = y

    @description.setter
    def description(self, description):
        self.description = description

    @image.setter
    def image(self, image):
        self.image = image
