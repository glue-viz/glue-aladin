from __future__ import absolute_import, division, print_function

from glue.core.layer_artist import LayerArtistBase
from glue.core.exceptions import IncompatibleAttribute
from glue.utils import nonpartial
from glue_aladin.layer_state import AladinLiteLayerState

__all__ = ['AladinLiteLayer']


class AladinLiteLayer(LayerArtistBase):

    def __init__(self, layer, aladin_widget, viewer_state):
        super(AladinLiteLayer, self).__init__(layer)
        self.aladin_widget = aladin_widget
        self.viewer_state = viewer_state
        self.viewer_state.add_callback('ra_att', nonpartial(self.update))
        self.viewer_state.add_callback('dec_att', nonpartial(self.update))
        self.layer_state = AladinLiteLayerState(layer=layer)
        self.viewer_state.layers.append(self.layer_state)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        self.update()

    def clear(self):
        # TODO: Here we need to write javascript to remove markers associated with this layer
        js = ""
        self.aladin_widget.run_js(js)

    def update(self, view=None):

        self.clear()

        if not self.visible:
            return

        try:
            ra = self.layer[self.viewer_state.ra_att]
            dec = self.layer[self.viewer_state.dec_att]
        except IncompatibleAttribute:
            print("Cannot fetch attributes %s and %s" % (self.viewer_state.ra_att, self.viewer_state.dec_att))
            return

        # TODO: Here we need to write javascript to add the markers associated with this layer
        js = ""
        self.aladin_widget.run_js(js)

    def redraw(self):
        pass
