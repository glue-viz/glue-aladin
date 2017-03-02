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
        self.layer_state.add_callback('color', nonpartial(self.update))
        self.layer_state.add_callback('alpha', nonpartial(self.update))
        self.viewer_state.layers.append(self.layer_state)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        self.update()

    def clear(self):
        # TODO: need to find a smart way to remove *only* the needed catalog layer and not everything!
        js = "aladin.view.removeLayers();"
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

        # self.layer_state.color

        # create javascript to add associated sources
        color = 'red' # TODO: retrieve color from self.layer_state
        js = "var cat = A.catalog({color: '%s'});\n" % (color)
        js += "aladin.addCatalog(cat);\n"
        js += "var sources = [];\n"
        for k in range(0, len(ra)):
            js += "sources.push(A.source(%f, %f));\n" % (ra[k], dec[k]);
           
        js += "cat.addSources(sources);"
        self.aladin_widget.run_js(js)

    def redraw(self):
        pass
