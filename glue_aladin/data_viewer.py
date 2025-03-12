from echo import add_callback
from glue.core import message as msg
from glue_qt.viewers.common.data_viewer import DataViewer
from glue_qt.viewers.common.toolbar import BasicToolbar

from glue_aladin.aladin_lite import AladinLiteQtWidget
from glue_aladin.catalog_layer_widget import AladinLiteCatalogOptionsPanel
from glue_aladin.viewer_state import AladinLiteState
from glue_aladin.options_widget import AladinLiteOptionsPanel
from glue_aladin.layer_artist import AladinLiteLayer


class AladinLiteViewer(DataViewer):

    LABEL = "Aladin Lite Viewer"
    _toolbar_cls = BasicToolbar
    _layer_style_widget_cls = AladinLiteCatalogOptionsPanel
    _state_cls = AladinLiteState

    def _initialize_aladin(self):
        # We need to block because otherwise some of the layer artist
        # JS commands will run before the Aladin JS setup is complete
        self.aladin_widget = AladinLiteQtWidget(block_until_ready=True)

    def __init__(self, session, state=None, parent=None):
        super(AladinLiteViewer, self).__init__(session, parent=parent)
        self._initialize_aladin()
        self.setCentralWidget(self.aladin_widget)
        self.state = state or AladinLiteState()
        self._options_widget = AladinLiteOptionsPanel(parent=self, viewer_state=self.state)

        add_callback(self.state, 'projection', self._update_projection)
        add_callback(self.state, 'reticle', self._update_reticle)
        add_callback(self.state, 'reticle_color', self._update_reticle_color)
        add_callback(self.state, 'coordinate_grid', self._update_coordinate_grid)
        add_callback(self.state, 'coordinate_frame', self._update_coordinate_frame)
        add_callback(self.state, 'coordinate_grid_color', self._update_coordinate_grid_color)

    def closeEvent(self, event):
        self.aladin_widget.close()
        return super(AladinLiteViewer, self).closeEvent(event)

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

    def _bool_js_string(self, boolean):
        return str(boolean).lower()

    def _update_projection(self, projection):
        self.aladin_widget.run_js(f"aladin.setProjection('{projection}')")

    def _update_reticle(self, reticle):
        self.aladin_widget.run_js(f"aladin.showReticle({self._bool_js_string(reticle)})")

    def _update_reticle_color(self, color):
        self.aladin_widget.run_js(f"aladin.reticle.update({{color: '{color}'}})")

    def _update_coordinate_grid(self, grid):
        prefix = "show" if grid else "hide"
        self.aladin_widget.run_js(f"aladin.{prefix}CooGrid()")

    def _update_coordinate_frame(self, frame):
        self.aladin_widget.run_js(f"aladin.setFrame('{frame}')")

    def _update_coordinate_grid_color(self, color):
        self.aladin_widget.run_js(f"aladin.setCooGrid({{color: '{color}'}})")
