"""Admin controller – CRUD for CMS pages."""

from py4web import URL, abort, action, redirect
from py4web.utils.form import Form

from ..common import auth, db, flash, session


@action("admin/index")
@action.uses("admin_home.html", session, auth.user)
def admin_home() -> dict:
    return dict()


@action("admin/pages")
@action.uses("admin_pages.html", db, session, auth.user, flash)
def admin_pages_list() -> dict:
    rows = db(db.pages).select(orderby=db.pages.position)
    return dict(pages=rows)


@action("admin/pages/new", method=["GET", "POST"])
@action.uses("admin_page_form.html", db, session, auth.user, flash)
def admin_page_new() -> dict:
    form = Form(db.pages)
    if form.accepted:
        flash.set("Siden ble opprettet.")
        redirect(URL("admin/pages"))
    return dict(form=form, page_title="Ny side")


@action("admin/pages/<page_id:int>/edit", method=["GET", "POST"])
@action.uses("admin_page_form.html", db, session, auth.user, flash)
def admin_page_edit(page_id: int) -> dict:
    page = db.pages[page_id] or abort(404)
    form = Form(db.pages, page_id)
    if form.accepted:
        flash.set("Siden ble oppdatert.")
        redirect(URL("admin/pages"))
    return dict(form=form, page=page, page_title="Rediger side")


@action("admin/pages/<page_id:int>/delete", method=["POST"])
@action.uses(db, session, auth.user, flash)
def admin_page_delete(page_id: int) -> None:
    db(db.pages.id == page_id).delete()
    flash.set("Siden ble slettet.")
    redirect(URL("admin/pages"))
