""" Admin commands
this modules exposes a dictionary called `cmds` which maps
to a function that executes an admin task

important note: create a config.json in the root src folder
"""

from guards import BANNED, noexcept
from logger import log_on_call
import json

config = json.load(open("./config.json", "r"))

@log_on_call
@noexcept(Exception)
def unban(user_id, admin_id):
    if user_id in BANNED and config["admin_key"] == admin_id:
        BANNED.remove(user_id)


@log_on_call
@noexcept(Exception)
def shutdown(admin_id):
    if config["admin_key"] == admin_id:
        exit()


cmds = {
    "__admin_ unban": unban,
    "__admin_ shutdown": shutdown
}