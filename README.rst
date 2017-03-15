Experimental glue plugin for Aladin Lite
========================================

|Travis Status| |AppVeyor Status| |Coverage Status|

Requirements
------------

Note that this plugin requires `Glue <http://glueviz.org/>`__ to be installed,
and for now only works with Qt5.

Installing the plugin
---------------------

You can install the latest developer version from the git repository
using:

::

    pip install https://github.com/glue-viz/glue-aladin/archive/master.zip

This will auto-register the plugin with Glue, and one of the available viewers
will now be 'Aladin Lite Viewer'.

Testing
-------

To run the tests, do:

::

    py.test glue_aladin

at the root of the repository. This requires the
`pytest <http://pytest.org>`__ module to be installed.

.. |Travis Status| image:: https://travis-ci.org/glue-viz/glue-aladin.svg
   :target: https://travis-ci.org/glue-viz/glue-aladin?branch=master
.. |AppVeyor Status| image:: https://ci.appveyor.com/api/projects/status/7h9js5tdu9v9nnlg/branch/master?svg=true
   :target: https://ci.appveyor.com/project/glue-viz/glue-aladin/branch/master
.. |Coverage Status| image:: https://coveralls.io/repos/github/glue-viz/glue-aladin/badge.svg
   :target: https://coveralls.io/github/glue-viz/glue-aladin
