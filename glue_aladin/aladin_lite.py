#!/usr/bin/env python

from qtpy import QtWebEngineWidgets
from qtpy.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from qtpy.QtWidgets import QWidget, QVBoxLayout

ALADIN_LITE_HTML = """
<html>
<head>
    <!-- Mandatory when setting up Aladin Lite v3 for a smartphones/tablet usage -->
    <!--
    <meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0, user-scalable=no">
    -->
</head>
<body style="margin: 0;">

<div id="aladin-lite-div" style="width: 100%; height: 100%;"></div>
<script type="text/javascript" src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>

<script type="text/javascript">
    var aladin;
    var aladinPromise = A.init;
    aladinPromise.then(() => {
        aladin = A.aladin('#aladin-lite-div', {
            fov: 360,
            cooFrame: 'ICRS',
            projection: 'TAN',
            showCooGridControl: false,
            showSimbadPointerControl: false,
            showCooGrid: false,
            showReticle: false,
            showProjectionControl: false,
            showFullscreenControl: false,
            showShareControl: false,
            showFrame: false,
        });
    });
</script>

</body>
</html>
"""


class AladinWebEnginePage(QWebEnginePage):

    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        print(f"JavaScript console message: {message} (level: {level}, line: {line_number}, source: {source_id})")


class AladinLiteQtWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(AladinLiteQtWidget, self).__init__(*args, **kwargs)
        web = QWebEngineView()
        layout = QVBoxLayout()
        self.setLayout(layout)
        page = AladinWebEnginePage()
        web.setPage(page)
        web.setHtml(ALADIN_LITE_HTML)
        layout.addWidget(web)
        self.web = web
        self.page = web.page()

    def run_js(self, js, callback=None):
        print("Running javascript: " + js)
        # js = f"window.aladinPromise.then(() => {{ {js} }})"
        if callback:
            self.page.runJavaScript(js, 0, callback)
        else:
            self.page.runJavaScript(js)
