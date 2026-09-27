import pytest


def test_pkg_resources_available():
    # Regression for #146: `pymorphy2` discovers dictionaries through
    # `pkg_resources` entry points (shipped with `setuptools`). In
    # environments without `setuptools` this raises `ModuleNotFoundError:
    # No module named 'pkg_resources'`. natasha declares `setuptools` as a
    # runtime dependency to keep this path working.
    import pkg_resources  # noqa: F401


def test_pymorphy2_entry_point_discovery():
    # Exercise the exact code path that imports `pkg_resources` and iterates
    # entry points, so a missing dependency surfaces here rather than at
    # first `MorphVocab()` construction.
    from pymorphy2 import analyzer

    paths = analyzer._lang_dict_paths()
    assert 'ru' in paths
