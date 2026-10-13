from py4web import action

from ..common import T, auth, session


@action("index")
@action.uses("home.html", auth, T)
def index() -> dict:
    return dict(user=auth.get_user())
