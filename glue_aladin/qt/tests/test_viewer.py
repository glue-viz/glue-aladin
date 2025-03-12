# from time import sleep
#
# from glue_qt.app import GlueApplication
# from glue.core import Data
# from numpy import allclose
# from glue_aladin.layer_state import AladinLiteLayerState
#
# from glue_aladin.tests.utils import assert_js_result_equals, assert_js_result_satisfies
#
# from ..data_viewer import AladinLiteViewer


class TestAladinLiteViewer(object):

    def test_dummy(self):
        assert True

# class TestAladinLiteViewer(object):
#
#     def setup_method(self, method):
#         self.d = Data(ra=[1, 2, 3], dec=[2, 3, 4], c=[4, 5, 6])
#         self.application = GlueApplication()
#         self.dc = self.application.data_collection
#         self.dc.append(self.d)
#         self.hub = self.dc.hub
#         self.session = self.application.session
#         self.viewer = self.application.new_data_viewer(AladinLiteViewer)
#         sleep(0.5)
#
#     def teardown_method(self, method):
#         self.viewer.aladin_widget.close()
#
#     def register(self):
#         self.viewer.register_to_hub(self.hub)
#
#     def test_add_data(self):
#         self.viewer.add_data(self.d)
#         self.viewer.state.ra_att = self.d.id["ra"]
#         self.viewer.state.dec_att = self.d.id["dec"]
#         assert len(self.viewer.state.layers) == 1
#         assert self.viewer.state.layers[0].layer is self.d
#
#     def test_catalog_color(self):
#         self.viewer.add_data(self.d)
#         layer_state = self.viewer.layers[0].state
#         for color in ("#002244", "#C60C30", "#B0B7BC"):
#             layer_state.color = color
#             assert_js_result_equals(
#                 self.viewer.aladin_widget,
#                 "aladin.view.catalogs[0].color",
#                 color
#             )
#
#     def test_catalog_size(self):
#         self.viewer.add_data(self.d)
#         layer_state = self.viewer.layers[0].state
#         for size in (1, 2, 3, 5, 7, 9, 10, 15):
#             layer_state.size = size
#             assert_js_result_equals(
#                 self.viewer.aladin_widget,
#                 "aladin.view.catalogs[0].sourceSize",
#                 size
#             )
#
#     def test_catalog_shape(self):
#         self.viewer.add_data(self.d)
#         layer_state = self.viewer.layers[0].state
#         for shape in AladinLiteLayerState.shape.get_choices(layer_state):
#             layer_state.shape = shape
#             assert_js_result_equals(
#                 self.viewer.aladin_widget,
#                 "aladin.view.catalogs[0].shape",
#                 shape
#             )
#
#     def test_center(self):
#         self.viewer.add_data(self.d)
#         self.viewer.state.ra_att = self.d.id["ra"]
#         self.viewer.state.dec_att = self.d.id["dec"]
#         self.viewer.layers[0].center()
#         assert_js_result_satisfies(
#             self.viewer.aladin_widget,
#             "aladin.getFov()",
#             lambda result: result[0] == 4.23994874401167
#         )
#         assert_js_result_satisfies(
#             self.viewer.aladin_widget,
#             # Aladin Lite returns RA/Dec as a Float64Array
#             # This seems like the simplest way to deal with that
#             "[...aladin.getRaDec()]",
#             lambda result: allclose(result, [1.999390145878301, 3.0003040684363738])
#         )
#
#     def test_new_subset_group(self):
#         # Make sure only the subset for data that is already inside the viewer
#         # is added.
#         d2 = Data(a=[4, 5, 6])
#         self.dc.append(d2)
#         self.viewer.add_data(self.d)
#         assert len(self.viewer.layers) == 1
#         self.dc.new_subset_group(subset_state=self.d.id['ra'] > 1, label='A')
#         assert len(self.viewer.layers) == 2
#
#     def test_double_add_ignored(self):
#         assert len(self.viewer.layers) == 0
#         self.viewer.add_data(self.d)
#         assert len(self.viewer.layers) == 1
#         self.viewer.add_data(self.d)
#         assert len(self.viewer.layers) == 1
