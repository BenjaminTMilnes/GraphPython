

class GContentElement (object):
    def __init__(self):

        self._elementNames = []
        self.subelements = []

        self.styleClass = ""


class GParagraph (GContentElement):
    def __init__(self):
        super(GParagraph, self).__init__()

        self._elementNames = ["paragraph", "p"]


class GHeading (GContentElement):
    def __init__(self, level=1):
        super(GHeading, self).__init__()

        self.level = level
        self._elementNames = ["heading{0}".format(self.level), "h{0}".format(self.level)]


class GBold (GContentElement):
    def __init__(self):

        self._elementNames = ["bold", "b"]


class GItalic (GContentElement):
    def __init__(self):

        self._elementNames = ["italic", "i"]


class GUnderline (GContentElement):
    def __init__(self):

        self._elementNames = ["underline", "u"]


class GStrikethrough (GContentElement):
    def __init__(self):

        self._elementNames = ["strikethrough", "s"]
