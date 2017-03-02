from glue.viewers.common.qt.data_viewer import DataViewer
from glue.viewers.common.qt.toolbar import BasicToolbar

from glue_aladin.aladin_lite import AladinLiteQtWidget
from glue_aladin.viewer_state import AladinLiteState
from glue_aladin.options_widget import AladinLiteOptionsPanel
from glue_aladin.layer_artist import AladinLiteLayer


class AladinLiteViewer(DataViewer):

    LABEL = "Aladin Lite Viewer"
    _toolbar_cls = BasicToolbar

    def __init__(self, session, parent=None):
        super(AladinLiteViewer, self).__init__(session, parent=parent)
        self.aladin_widget = AladinLiteQtWidget()
        self.setCentralWidget(self.aladin_widget)
        self.state = AladinLiteState()
        self._options_widget = AladinLiteOptionsPanel(parent=self, viewer_state=self.state)

    def add_data(self, data):

        if data in self._layer_artist_container:
            return True

        layer_artist = AladinLiteLayer(layer=data,
                                       aladin_widget=self.aladin_widget,
                                       viewer_state=self.state)

        self._layer_artist_container.append(layer_artist)

        return True

    def options_widget(self):
        return self._options_widget
