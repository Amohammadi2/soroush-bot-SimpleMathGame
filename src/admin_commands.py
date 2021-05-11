from guards import BANNED, noexcept
from logger import log_on_call

@log_on_call
@noexcept(Exception)
def unban(user_id):
    if user_id in BANNED: BANNED.remove(user_id)

cmds = {
    "__admin_ unban": unban
}