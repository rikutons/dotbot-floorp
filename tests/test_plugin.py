# dotbot-floorp -- Configure your Floorp profile(s) using dotbot.
# Copyright 2022-2024 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT


import os
import sys
import typing
import unittest.mock

import dotbot.plugin
import pytest

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import dotbot_floorp


@pytest.fixture(
    ids=("windows", "mac", "linux", "linux-snap", "linux-flatpak"),
    params=(
        ("win32", "/adrift/win32/appdata/Mozilla/Floorp/Profiles/bogus"),
        ("darwin", "/adrift/darwin/Library/Application Support/Floorp/Profiles/bogus"),
        ("linux", "/adrift/linux/.mozilla/floorp/bogus"),
        ("linux", "/adrift/linux/snap/floorp/common/.mozilla/floorp/bogus"),
        ("linux", "/adrift/linux/.var/app/org.mozilla.floorp/.mozilla/floorp/bogus"),
    ),
)
def get_profile(request, fs, monkeypatch):
    """Create a profile that the plugin should be able to find."""

    platform, path = request.param
    home = f"/adrift/{platform}"
    appdata = f"{home}/appdata"

    monkeypatch.setenv("HOME", home)  # POSIX
    monkeypatch.setenv("USERPROFILE", home)  # Windows
    monkeypatch.setenv("APPDATA", appdata)  # Windows

    def get_path(status: typing.Literal[None, "exists", "is_valid"]):
        if status in {"exists", "is_valid"}:
            fs.create_dir(path)
        if status == "is_valid":
            fs.create_file(f"{path}/prefs.js")
        return path.replace("/", os.path.sep)

    with unittest.mock.patch("dotbot_floorp.sys.platform", platform):
        yield get_path


@pytest.mark.parametrize("status", (None, "exists", "is_valid"))
def test_get_profile_directories(get_profile, status):
    """Test that profile directories are returned when they exist."""

    expected = get_profile(status=status)

    paths = [str(path) for path in dotbot_floorp._get_profile_directories()]

    if status == "is_valid":
        assert expected in paths
    else:
        assert paths == []


def test_directive_handling_mismatch():
    """Verify the plugin rejects unexpected directives."""

    plugin = dotbot_floorp.Floorp(None)
    assert plugin.can_handle("wrong-directive") is False
    with pytest.raises(ValueError):
        plugin.handle("wrong-directive", {})


@pytest.mark.parametrize("link_success", (True, False))
def test_directive_handling_success(get_profile, link_success):
    """Verify the plugin incorporates the success code of the Link plugin."""

    target = os.path.join(get_profile(status="is_valid"), "user.js")
    plugin = dotbot_floorp.Floorp(context=None)

    link_mock = unittest.mock.MagicMock()
    link_mock.return_value = link_mock
    link_mock.handle.return_value = link_success
    with unittest.mock.patch("dotbot_floorp.dotbot.plugins.link.Link", link_mock):
        assert plugin.handle("floorp", {"user.js": "js-file"}) is link_success
    assert link_mock.handle.call_count == 1
    assert link_mock.handle.call_args.args == ("link", {target: "js-file"})


def test_logging_when_no_profiles_found(get_profile):
    """Verify the plugin logs a warning when no Floorp profiles are found."""

    plugin = dotbot_floorp.Floorp(context=None)

    log_mock = unittest.mock.Mock()
    link_mock = unittest.mock.MagicMock()

    with unittest.mock.patch("dotbot_floorp.dotbot.plugins.link.Link", link_mock):
        with unittest.mock.patch("dotbot_floorp.log", log_mock):
            assert plugin.handle("floorp", {"user.js": "js-file"}) is True

    assert link_mock.handle.call_count == 0, "The Link plugin should not have been used"
    assert log_mock.warning.call_count == 1
    assert log_mock.warning.call_args.args == ("No Floorp profiles found",)


def test_no_user_js_key(get_profile):
    """Test the plugin behavior when there is no "user.js" key in `data`."""

    plugin = dotbot_floorp.Floorp(context=None)
    assert plugin.handle("floorp", {}) is True


def test_versions_match():
    """Verify that duplicated version numbers all match."""

    with open("pyproject.toml", "rb") as file:
        toml_version: str = tomllib.load(file)["tool"]["poetry"]["version"]
    assert toml_version != ""

    with open("dotbot_floorp.py") as file:
        python = file.read()
    python_version = ""
    for line in python.splitlines():  # pragma: no branch
        key, _, value = line.partition("=")
        if key.strip() == "__version__":
            python_version = value.strip('" ')
            break
    assert python_version != ""

    assert toml_version == python_version


def test_exactly_one_class_inheriting_from_dotbot_plugin():
    """Verify that there is only one class inheriting from dotbot.plugin.Plugin."""

    subclass_quantity = len(
        [
            name
            for name in dir(dotbot_floorp)
            if (
                hasattr(getattr(dotbot_floorp, name), "__bases__")
                and issubclass(getattr(dotbot_floorp, name), dotbot.plugin.Plugin)
            )
        ]
    )
    assert subclass_quantity == 1, "Only 1 class can inherit from dotbot.plugin.Plugin"
