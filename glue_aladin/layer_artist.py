from __future__ import absolute_import, division, print_function

from uuid import uuid4

from glue.core.layer_artist import LayerArtistBase
from glue.core.exceptions import IncompatibleAttribute
from glue.utils import nonpartial

from numpy import isfinite

from glue_aladin.layer_state import AladinLiteLayerState
from glue_aladin.utils import center_fov, color_to_hex

__all__ = ['AladinLiteLayer']


# TODO: There were issues with properties not being recognized as CallbackProperty instances
# when inheriting from `LayerArtist`. Figure out why
class AladinLiteLayer(LayerArtistBase):

    _layer_state_cls = AladinLiteLayerState

    def __init__(self, layer, aladin_widget, viewer_state):
        self._id = uuid4().hex
        super(AladinLiteLayer, self).__init__(layer)
        self.aladin_widget = aladin_widget
        self.viewer_state = viewer_state
        self.viewer_state.add_callback('ra_att', nonpartial(self.update))
        self.viewer_state.add_callback('dec_att', nonpartial(self.update))
        self.state = AladinLiteLayerState(layer=layer)
        self.state.add_callback('color', self._update_color)
        self.state.add_callback('alpha', self._update_color)
        self.state.add_callback('shape', self._update_shape)
        self.state.add_callback('size', self._update_size)
        self.viewer_state.layers.append(self.state)

    def __gluestate__(self, context):
        return dict(state=context.id(self.state))

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        self.update()

    @property
    def catalog_var(self):
        return f"cat_{self._id}"

    def _update_color(self, color):
        self.aladin_widget.run_js(f"{self.catalog_var}.updateShape({{ color: '{color}' }})")

    def _update_shape(self, shape):
        self.aladin_widget.run_js(f"{self.catalog_var}.updateShape({{ shape: '{shape}' }})")

    def _update_size(self, size):
        self.aladin_widget.run_js(f"{self.catalog_var}.updateShape({{ sourceSize: {size} }})")

    def center(self, *args):
        lon = self.layer[self.viewer_state.ra_att]
        lat = self.layer[self.viewer_state.dec_att]

        if len(lon) == 0 or len(lat) == 0:
            return

        lon_cen, lat_cen, sep_max = center_fov(lon, lat)
        if lon_cen is None or lat_cen is None:
            return

        fov = min(60, sep_max * 3)
        js = f"""
        aladin.setFov({fov});
        aladin.gotoRaDec({lon_cen}, {lat_cen});
        """
        self.aladin_widget.run_js(js)

    def clear(self):
        js = f"{self.catalog_var}.removeAll()"
        self.aladin_widget.run_js(js)

    def remove(self):
        super(AladinLiteLayer, self).remove()
        js = f"""
        console.log({self.catalog_var});
        aladin.view.removeLayer({self.catalog_var});
        delete {self.catalog_var};
        """
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
        js = f"var {self.catalog_var} = A.catalog({{color: '%s'}});\n" % (color_to_hex(self.state.color))
        js += f"aladin.addCatalog({self.catalog_var});\n"
        js += "var sources = [];\n"
        for k in range(0, len(ra)):
            if isfinite(ra[k]) and isfinite(dec[k]):
                js += "sources.push(A.source(%f, %f));\n" % (ra[k], dec[k])

        js += f"{self.catalog_var}.addSources(sources);"
        self.aladin_widget.run_js(js)

    def redraw(self):
        pass
