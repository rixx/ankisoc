# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
from anki.utils import fmtTimeSpan

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def miniStats() -> None:
    unique_cards_today, total_time = mw.col.db.first(
        """select count(distinct cid), sum(time)/1000 from revlog where id > ?""",
        (mw.col.sched.dayCutoff-86400)*1000)
    cards_today = mw.col.db.first(
        """select count() from revlog where id > ?""",
        (mw.col.sched.dayCutoff - 86400) * 1000)[0]
    total_time = fmtTimeSpan(total_time or 0, unit=1)

    new = 0
    due = 0
    total_cards = 0
    breakpoint()
    for node in mw.col.sched.deck_due_tree().children:
        new += node.new_count
        due += node.learn_count
        total_cards += node.total_in_deck

    info = "\n".join([
        f"Card count: {total_cards}",
        f"Unique cards studied today: {unique_cards_today or 0}",
        f"Cards studied today: {cards_today or 0}",
        f"New cards added(?) today: {new}",
        f"Cards still due today: {due}",
        f"Study time today: {total_time}"
    ])

    showInfo(info)

# create a new menu item, "test"
action = QAction("Mini stats", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, miniStats)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
