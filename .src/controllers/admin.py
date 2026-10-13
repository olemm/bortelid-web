"""Admin controller – CRUD for CMS pages."""

from py4web import URL, abort, action, redirect, request
from py4web.utils.form import Form

from ..common import auth, db, flash, session


# ── Image helpers ────────────────────────────────────────────────────────────

def _save_new_images(page_id: int) -> None:
    """Insert uploaded new_image_N files into page_images."""
    i = 0
    while True:
        upload = request.files.get(f"new_image_{i}")
        if upload is None:
            break
        if upload.raw_filename:
            upload.file.seek(0)
            db.page_images.insert(
                page_id=page_id,
                image=upload,
                description=request.POST.get(f"new_desc_{i}", "").strip(),
                position=i,
            )
        i += 1


def _update_existing_images(page_id: int) -> None:
    """Update descriptions or delete existing page_images based on POST data."""
    for img in db(db.page_images.page_id == page_id).select():
        if request.POST.get(f"delete_{img.id}"):
            img.delete_record()
        else:
            img.update_record(
                description=request.POST.get(f"desc_{img.id}", "").strip()
            )


# ── Routes ───────────────────────────────────────────────────────────────────

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
        _save_new_images(form.vars['id'])
        flash.set("Siden ble opprettet.")
        redirect(URL("admin/pages"))
    return dict(form=form, page_title="Ny side", page_images=[])


@action("admin/pages/<page_id:int>/edit", method=["GET", "POST"])
@action.uses("admin_page_form.html", db, session, auth.user, flash)
def admin_page_edit(page_id: int) -> dict:
    page = db.pages[page_id] or abort(404)
    form = Form(db.pages, page_id)
    if form.accepted:
        _update_existing_images(page_id)
        _save_new_images(page_id)
        flash.set("Siden ble oppdatert.")
        redirect(URL("admin/pages"))
    images = db(db.page_images.page_id == page_id).select(
        orderby=db.page_images.position
    )
    return dict(form=form, page=page, page_title="Rediger side", page_images=images)


@action("admin/pages/<page_id:int>/delete", method=["POST"])
@action.uses(db, session, auth.user, flash)
def admin_page_delete(page_id: int) -> None:
    db(db.page_images.page_id == page_id).delete()
    db(db.pages.id == page_id).delete()
    flash.set("Siden ble slettet.")
    redirect(URL("admin/pages"))
