from . import api
from .change_user_role import ChangeUserRole
from .delete_user_role import DeleteUserRole
from .set_own_role import SetOwnUserRole

api.add_resource(ChangeUserRole, "/user_role/change")
api.add_resource(DeleteUserRole, "/user_role/remove")
api.add_resource(SetOwnUserRole, "/user_role/own")
