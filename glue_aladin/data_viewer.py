from glue.viewers.common.qt.data_viewer import DataViewer


class AladinLiteViewer(DataViewer):

    LABEL = "Aladin Lite Viewer"

    def __init__(self, session, parent=None):
        super(MyViewer, self).__init__(session, parent=parent)
        # self.setCentralWidget(my_qt_widget)

    def add_data(self, data):
        return True
