"""
controllers package – py4web discovers all @action-decorated routes
from this package and its sub-modules.

Add new feature modules inside this directory and import them below
so that py4web registers their routes.
"""

from yatl.helpers import A

from py4web import URL, abort, action, redirect, request

from ..common import (
    T,
    auth,
    authenticated,
    cache,
    db,
    flash,
    logger,
    session,
    unauthenticated,
)

# ── Route modules ──────────────────────────────────────────────
from . import home   # noqa: F401  – registers the / (index) route
from . import admin  # noqa: F401  – registers /admin/pages/* routes
from . import page   # noqa: F401  – registers /<slug> public route (must be last)
