from time import sleep

from mock import MagicMock

from glue_qt.app import GlueApplication
from glue.core import Data, message
from glue_aladin.aladin_lite import AladinLiteQtWidget

from glue_aladin.tests.utils import assert_js_result_equals

from ..data_viewer import AladinLiteViewer


class AladinLiteViewerBlocking(AladinLiteViewer):

    def _initialize_aladin(self):
        self.aladin_widget = AladinLiteQtWidget(block_until_ready=True)


class TestAladinLiteViewer(object):

    def setup_method(self, method):
        self.d = Data(ra=[1, 2, 3], dec=[2, 3, 4], c=[4, 5, 6])
        self.application = GlueApplication()
        self.dc = self.application.data_collection
        self.dc.append(self.d)
        self.hub = self.dc.hub
        self.session = self.application.session
        self.viewer = self.application.new_data_viewer(AladinLiteViewerBlocking)
        sleep(0.5)

    def teardown_method(self, method):
        self.viewer.aladin_widget.close()

    def register(self):
        self.viewer.register_to_hub(self.hub)

    def test_add_data(self):
        self.viewer.add_data(self.d)
        self.viewer.state.ra_att = self.d.id["ra"]
        self.viewer.state.dec_att = self.d.id["dec"]
        assert len(self.viewer.state.layers) == 1
        assert self.viewer.state.layers[0].layer is self.d

    def test_center(self):
        self.viewer.add_data(self.d)
        self.viewer.state.ra_att = self.d.id["ra"]
        self.viewer.state.dec_att = self.d.id["dec"]
        self.viewer.layers[0].center()
        assert_js_result_equals(
            self.viewer.aladin_widget,
            "aladin.getFov()",
            [
                4.23994874401167,
                3.1799615580087526,
            ]
        )

    def test_new_subset_group(self):
        # Make sure only the subset for data that is already inside the viewer
        # is added.
        d2 = Data(a=[4, 5, 6])
        self.dc.append(d2)
        self.viewer.add_data(self.d)
        assert len(self.viewer.layers) == 1
        self.dc.new_subset_group(subset_state=self.d.id['ra'] > 1, label='A')
        assert len(self.viewer.layers) == 2

    def test_double_add_ignored(self):
        assert len(self.viewer.layers) == 0
        self.viewer.add_data(self.d)
        assert len(self.viewer.layers) == 1
        self.viewer.add_data(self.d)
        assert len(self.viewer.layers) == 1

    # def test_remove_data(self):
    #     self.register()
    #     self.viewer.add_data(self.d)
    #     layer = self.viewer._layer_artist_container[self.d][0]

    #     layer.clear = MagicMock()
    #     self.hub.broadcast(message.DataCollectionDeleteMessage(self.dc,
    #                                                            data=self.d))
    #     assert self.d not in self.viewer._layer_artist_container

    # def test_remove_subset(self):
    #     self.register()
    #     s = self.d.new_subset()
    #     self.viewer.add_subset(s)

    #     layer = self.viewer._layer_artist_container[s][0]
    #     layer.clear = MagicMock()

    #     self.hub.broadcast(message.SubsetDeleteMessage(s))

    #     # assert layer.clear.call_count == 1
    #     print([s for s in self.viewer._layer_artist_container])
    #     assert s not in self.viewer._layer_artist_container

    # def test_subsets_added_with_data(self):
    #     s = self.d.new_subset()
    #     self.viewer.add_data(self.d)
    #     assert s in self.viewer._layer_artist_container

    # def test_subsets_live_added(self):
    #     self.register()
    #     self.viewer.add_data(self.d)
    #     s = self.d.new_subset()
    #     assert s in self.viewer._layer_artist_container

