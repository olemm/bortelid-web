"""Public dynamic page controller – serves CMS pages by slug."""

from py4web import abort, action

from ..common import auth, db, session


@action("<slug:path>")
@action.uses("page.html", db, session, auth)
def page(slug: str) -> dict:
    row = db((db.pages.slug == slug) & (db.pages.is_published == True)).select().first()
    if not row:
        abort(404)
    page_images = db(db.page_images.page_id == row.id).select(orderby=db.page_images.position)
    return dict(page=row, page_images=page_images)
