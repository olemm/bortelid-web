"""News listing controller — /nyheter"""

import re

from py4web import action

from ..common import auth, db, session


def _excerpt(html: str, length: int = 150) -> str:
    text = re.sub(r'<[^>]+>', ' ', html or '')
    text = ' '.join(text.split())
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + '…'


@action("nyheter")
@action.uses("news.html", db, session, auth)
def news() -> dict:
    pages = db(db.pages.is_published == True).select(
        orderby=~db.pages.created_on | ~db.pages.id,
        limitby=(0, 15),
    )
    page_ids = [p.id for p in pages]
    all_images = db(db.page_images.page_id.belongs(page_ids)).select(
        orderby=db.page_images.page_id | db.page_images.position
    )
    images_by_page = {}
    for img in all_images:
        images_by_page.setdefault(img.page_id, []).append(img)

    items = [
        {'page': p, 'excerpt': _excerpt(p.content), 'images': images_by_page.get(p.id, [])}
        for p in pages
    ]
    return dict(items=items)
