"""
This file defines the database models.
All db.define_table() calls live here.
"""

import datetime
import uuid as _uuid

from py4web import URL
from pydal.validators import IS_INT_IN_RANGE, IS_NOT_EMPTY, IS_NOT_IN_DB

from . import settings
from .common import Field, auth, db

# ── pages ──────────────────────────────────────────────────────────────────

db.define_table(
    "pages",
    Field("title", "string", length=255, notnull=True,
          requires=IS_NOT_EMPTY(error_message="Tittel er påkrevd.")),
    Field("slug", "string", length=255, unique=True, notnull=True,
          requires=[
              IS_NOT_EMPTY(error_message="Slug er påkrevd."),
              IS_NOT_IN_DB(db, "pages.slug", error_message="Denne sluggen er allerede i bruk."),
          ]),
    Field("content", "text"),
    Field("position", "integer", default=0,
          requires=IS_INT_IN_RANGE(0, None, error_message="Posisjon må være et ikke-negativt heltall.")),
    Field("is_published", "boolean", default=False),
    # ── Tracking fields (set automatically, not editable via Form) ──────────
    Field("self_uuid", "string", length=36, unique=True,
          default=lambda: str(_uuid.uuid4()),
          writable=False),
    Field("created_by", "string", length=36,
          default=lambda: (auth.get_user() or {}).get("uuid"),
          writable=False),
    Field("updated_by", "string", length=36,
          update=lambda: (auth.get_user() or {}).get("uuid"),
          writable=False),
    Field("created_on", "date",
          default=lambda: datetime.date.today(),
          writable=False),
    Field("updated_on", "date",
          update=lambda: datetime.date.today(),
          writable=False),
)

# ── page_images ────────────────────────────────────────────────────────────
# One-to-many: each page can have multiple images with individual descriptions.
# Images are ordered by position and will be rendered as a carousel on the
# public page.

db.define_table(
    "page_images",
    Field("page_id", "reference pages", notnull=True),
    Field("image", "upload",
          uploadfolder=settings.UPLOAD_FOLDER,
          download_url=lambda name: URL("download", name)),
    Field("description", "string", length=500, default=""),
    Field("position", "integer", default=0),
)

db.commit()
