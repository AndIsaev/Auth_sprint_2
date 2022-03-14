from . import api
from .create import RoleCreate
from .detail import RoleDetail
from .list import RoleList

api.add_resource(RoleList, "/role/")
api.add_resource(RoleCreate, "/role/")
api.add_resource(RoleDetail, "/role/<string:role_id>")
