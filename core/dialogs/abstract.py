class AbstractWindow(object):

    def __init__(self, *args, **kwargs):
        super(AbstractWindow, self).__init__(*args, **kwargs)
        self.setupUI()

    def setupUI(self):
        pass
