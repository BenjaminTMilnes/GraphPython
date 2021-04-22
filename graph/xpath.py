


class Selector(object):
    pass 

class ElementNameSelector(Selector):
    def __init__(self, elementName):
        super(ElementNameSelector, self).__init__()

        self.elementName = elementName 

class SubelementsSelector(Selector):
    def __init__(self):
        super(SubelementsSelector, self).__init__()

class RootElementSelector(Selector):
    def __init__(self):
        super(RootElementSelector, self).__init__()

class SuperelementSelector(Selector):
    def __init__(self):
        super(SuperelementSelector, self).__init__()
