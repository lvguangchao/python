"""Python compatiblity utilities."""
from __future__ import absolute_import, unicode_literals

from functools import (
    WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES,
    update_wrapper as _update_wrapper,
    partial,
)

__all__ = ['update_wrapper', 'wraps']


def update_wrapper(wrapper, wrapped, *args, **kwargs):
    """Update wrapper, also setting .__wrapped__."""
    wrapper = _update_wrapper(wrapper, wrapped, *args, **kwargs)
    wrapper.__wrapped__ = wrapped
    return wrapper


def wraps(wrapped,
          assigned=WRAPPER_ASSIGNMENTS,
          updated=WRAPPER_UPDATES):
    """Backport of Python 3.5 wraps that adds .__wrapped__."""
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)
