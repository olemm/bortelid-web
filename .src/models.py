"""
This file defines the database models.
All db.define_table() calls live here.
"""

from py4web import URL
from pydal.validators import IS_INT_IN_RANGE, IS_NOT_EMPTY, IS_NOT_IN_DB

from . import settings
from .common import Field, db

# ── pages ──────────────────────────────────────────────────────────────────
# CMS pages served by the dynamic frontend.
#
# The 'image' field uses pydal's native 'upload' type with uploadfolder set
# to the absolute path of .src/uploads/.  pydal automatically:
#   • generates a collision-proof filename  (pages.image.<uuid>.<b64name>.ext)
#   • writes the file to uploadfolder on insert / update
#   • stores only the generated filename string in the DB column
#
# Serving: the existing download/<filename> route in common.py resolves
# pydal-encoded filenames back to the correct uploadfolder path.

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
    Field("image", "upload",
          uploadfolder=settings.UPLOAD_FOLDER,
          download_url=lambda name: URL("download", name)),
    Field("position", "integer", default=0,
          requires=IS_INT_IN_RANGE(0, None, error_message="Posisjon må være et ikke-negativt heltall.")),
    Field("is_published", "boolean", default=False),
)
db.commit()
