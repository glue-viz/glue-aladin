from glue.viewers.common.qt.data_viewer import DataViewer
from glue.viewers.common.qt.toolbar import BasicToolbar
from glue.core import message as msg

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

    def add_subset(self, subset):

        if subset in self._layer_artist_container:
            return

        layer_artist = AladinLiteLayer(layer=subset,
                                       aladin_widget=self.aladin_widget,
                                       viewer_state=self.state)

        self._layer_artist_container.append(layer_artist)

    def options_widget(self):
        return self._options_widget

    def _add_subset(self, message):
        self.add_subset(message.subset)

    def _update_subset(self, message):
        if message.subset in self._layer_artist_container:
            for layer_artist in self._layer_artist_container[message.subset]:
                layer_artist.update()

    def _remove_subset(self, message):
        if message.subset in self._layer_artist_container:
            layer_artist = self._layer_artist_container.pop(message.subset)
            layer_artist.clear()

    def register_to_hub(self, hub):

        super(AladinLiteViewer, self).register_to_hub(hub)

        def subset_has_data(x):
            return x.sender.data in self._layer_artist_container.layers

        def has_data(x):
            return x.sender in self._layer_artist_container.layers

        hub.subscribe(self, msg.SubsetCreateMessage,
                      handler=self._add_subset,
                      filter=subset_has_data)

        hub.subscribe(self, msg.SubsetUpdateMessage,
                      handler=self._update_subset,
                      filter=subset_has_data)

        hub.subscribe(self, msg.SubsetDeleteMessage,
                      handler=self._remove_subset,
                      filter=subset_has_data)
