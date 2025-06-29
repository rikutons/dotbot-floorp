..  dotbot-floorp -- Configure your Floorp profile(s) using dotbot.
..  Copyright 2022-2024 Kurt McKee <contactme@kurtmckee.org>
..  SPDX-License-Identifier: MIT


dotbot-floorp
##############

Configure your Floorp profile(s) using `dotbot`_.

-------------------------------------------------------------------------------


Table of contents
=================

*   `What you can do with it`_
*   `Installation`_
*   `Configuration`_
*   `Floorp profile locations`_
*   `Development`_


What you can do with it
=======================

When Floorp starts, it will look for a ``user.js`` file in your profile directory.
If found, the ``user.js`` settings will be copied to ``prefs.js`` and used.

You can enforce a consistent Floorp configuration across all your profiles
by using dotbot-floorp to create symlinks to a custom ``user.js``.
The plugin will find Floorp profile directories that contain a ``prefs.js`` file
and will use dotbot's builtin Link plugin to create the symlinks.


Installation
============

There are two ways to install and use the plugin:

1.  Install it as a Python package.
2.  Add it as a git submodule in your dotfiles repository.
3.  Copy ``dotbot_floorp.py`` into your dotfiles directory.


Python package
--------------

If you want to install dotbot-floorp as a Python package
(for example, if you're using a virtual environment),
then you can install the plugin using ``pip``:

..  code-block::

    pip install dotbot-floorp

Then, when running dotbot, use the ``-p`` or ``--plugin`` option
to tell dotbot to load the plugin:

..  code-block::

    dotbot [...] --plugin dotbot_floorp [...]

If you're using one of dotbot's ``install`` scripts,
you'll need to edit that file to add the ``--plugin`` option.


Git submodule
-------------

If you want to track dotbot-floorp as a git submodule
(for example, if you manage your dotfiles using git)
then you can add the plugin repository as a submodule using ``git``:

..  code-block::

    git submodule add https://github.com/kurtmckee/dotbot-floorp.git

This will clone the repository to a directory named ``dotbot-floorp``.
Then, when running dotbot, use the ``-p`` or ``--plugin`` option
to tell dotbot to load the plugin:

..  code-block::

    dotbot [...] --plugin dotbot-floorp/dotbot_floorp.py [...]

Note that you may need to initialize the plugin's git submodule
when you clone your dotfiles repository or pull new changes
to another computer.
The command for this will look something like:

..  code-block::

    git submodule update --init dotbot-floorp


Copy ``dotbot_floorp.py``
--------------------------

If desired, you can copy ``dotbot_floorp.py`` to your dotfiles directory.
You might choose to do this if you already use other plugins
and have configured dotbot to load all plugins from a plugin directory.

If you copy ``dotbot_floorp.py`` to the root of your dotfiles directory
then, when running dotbot, use the ``-p`` or ``--plugin`` option
to tell dotbot to load the plugin:

..  code-block::

    dotbot [...] --plugin dotbot_floorp.py [...]

If you copy ``dotbot_floorp.py`` to a directory containing other plugins,
you can use dotbot's ``--plugin-dir`` option to load all plugins in the directory.
In the example below, the plugin directory is named ``dotbot-plugins``:

..  code-block::

    dotbot [...] --plugin-dir dotbot-plugins [...]


Configuration
=============

First, create a ``user.js`` file in the dotfiles directory that dotbot manages.
For example, it could contain this configuration to set your homepage:

..  code-block:: js

    user_pref("browser.startup.homepage", "https://dashboard.example");

(MozillaZine maintains an extensive list of `Floorp configuration settings`_.)

Then, add a ``floorp`` directive to your dotbot config with a ``user.js`` key.
The value of the key follows the syntax of the `dotbot Link plugin`_.
Now you can create a link for ``chrome`` directory as well.

..  code-block:: yaml

    # Example 1:
    # "user.js" can be specified as a string.
    floorp:
      user.js: floorp/user.js


    # Example 2:
    # "user.js" can have no value, and will be found
    # in the same directory as your dotbot config file.
    floorp:
      user.js:


    # Example 3:
    # The extended Link plugin syntax is supported.
    floorp:
      user.js:
        path: floorp/user.js
        force: true


Floorp profile locations
=========================

The dotbot-floorp plugin is aware of the following default directories:

*   ``%APPDATA%\Mozilla\Floorp\Profiles`` (Windows)
*   ``~/Library/Application Support/Floorp/Profiles`` (Mac OS)
*   ``~/.mozilla/floorp`` (Linux)
*   ``~/snap/floorp/common/.mozilla/floorp`` (Floorp Snap for Linux)
*   ``~/.var/app/org.mozilla.floorp/.mozilla/floorp`` (Floorp Flatpak for Linux)

Only profile subdirectories that contain a ``prefs.js`` file
will be considered valid by the plugin.


Development
===========

To set up a development environment, clone the dotbot-floorp plugin's git repository.
Then, follow these steps to create a virtual environment and run the unit tests locally:

..  code-block:: shell

    # Create the virtual environment
    $ python -m venv .venv

    # Activate the virtual environment (Linux)
    $ . .venv/bin/activate

    # Activate the virtual environment (Windows)
    $ & .venv/Scripts/Activate.ps1

    # Update pip and setuptools, and install wheel
    (.venv) $ pip install -U pip setuptools wheel

    # Install poetry, tox, and scriv
    (.venv) $ pip install poetry tox scriv

    # Install all dependencies
    (.venv) $ poetry install

    # Run the unit tests locally
    (.venv) $ tox


..  Links
..  =====
..
..  _dotbot: https://github.com/anishathalye/dotbot
..  _dotbot Link plugin: https://github.com/anishathalye/dotbot#link
..  _Floorp configuration settings: https://kb.mozillazine.org/About:config_entries
