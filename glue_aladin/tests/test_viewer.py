from glue_qt.app import GlueApplication
from glue.core import Data

from ..data_viewer import AladinLiteViewer


class TestAladinLiteViewer(object):

    def setup_method(self, method):
        self.d = Data(ra=[1, 2, 3], dec=[2, 3, 4], c=[4, 5, 6])
        self.application = GlueApplication()
        self.dc = self.application.data_collection
        self.dc.append(self.d)
        self.hub = self.dc.hub
        self.session = self.application.session

    def test_basic(self):
        self.viewer = self.application.new_data_viewer(AladinLiteViewer)
