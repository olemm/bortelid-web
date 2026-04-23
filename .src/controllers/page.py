"""Public dynamic page controller – serves CMS pages by slug."""

from py4web import abort, action

from ..common import db, session


@action("<slug>")
@action.uses("page.html", db, session)
def page(slug: str) -> dict:
    row = db((db.pages.slug == slug) & (db.pages.is_published == True)).select().first()
    if not row:
        abort(404)
    nav_pages = db(db.pages.is_published == True).select(orderby=db.pages.position)
    return dict(page=row, nav_pages=nav_pages)
