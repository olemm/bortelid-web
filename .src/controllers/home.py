from py4web import URL, action

from ..common import T, auth, db, session, flash


@action("index")
@action.uses("home.html", db, auth, T)
def index() -> dict:
    nav_pages = db(db.pages.is_published == True).select(orderby=db.pages.position)
    return dict(user=auth.get_user(), nav_pages=nav_pages)
