#!/usr/bin/env python

from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy.QtWidgets import QWidget, QVBoxLayout

ALADIN_LITE_HTML = """
<html>
<head>
  <link rel="stylesheet" href="http://aladin.u-strasbg.fr/AladinLite/api/v2/latest/aladin.min.css" />
  <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.min.js" charset="utf-8"></script>
</head>
<body>
<div id="aladin-lite-div"></div>
<script type="text/javascript" src="http://aladin.u-strasbg.fr/AladinLite/api/v2/latest/aladin.min.js" charset="utf-8">
</script>
<script type="text/javascript">
    var aladin = A.aladin('#aladin-lite-div', {survey: "P/DSS2/color", fov:60});
</script>
</body>
</html>
"""


class AladinLiteQtWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(AladinLiteQtWidget, self).__init__(*args, **kwargs)
        web = QWebEngineView()
        web.setHtml(ALADIN_LITE_HTML)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(web)
        self.page = web.page()

    def run_js(self, js):
        # print("Running javascript: " + js)
        self.page.runJavaScript(js)
