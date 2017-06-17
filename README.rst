django-debug-toolbar-vcs-info
==============================

.. image:: https://travis-ci.org/giginet/django-debug-toolbar-vcs-info.svg?branch=master
    :target: https://travis-ci.org/giginet/django-debug-toolbar-vcs-info
.. image:: https://coveralls.io/repos/giginet/django-debug-toolbar-vcs-info/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/giginet/django-debug-toolbar-vcs-info?branch=master



A `Django Debug Toolbar 
<https://github.com/django-debug-toolbar/django-debug-toolbar>`_ panel to show VCS info

.. image:: https://raw.githubusercontent.com/giginet/django-debug-toolbar-vcs-info/master/images/vcs_info_panel.png

Supported python versions
    2.7, 3.3, 3.4, 3.5, 3.6
Supported django versions
    1.7 - 1.11
Supported VCS
    git

Installation
------------------------

Use pip_ ::

    $ pip install django-debug-toolbar-vcs-info

.. _pip:  https://pypi.python.org/pypi/pip

Add ``vcs_info_panel`` into ``INSTALL_APPS`` in ``settings.py`` file

.. code:: python

  INSTALLED_APPS += (
      'vcs_info_panel',
  )

Add the panel you want to use. currently, you can use ``GitInfoPanel`` only.


.. code:: python

  DEBUG_TOOLBAR_PANELS = (
    ...
    'vcs_info_panel.panels.GitInfoPanel',
  )

Author
-------------------

giginet <giginet.net@gmail.com>

LICENSE
-------------------------

MIT License
