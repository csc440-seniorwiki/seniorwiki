from flask_principal import RoleNeed
from flask_principal import Permission


edit_permission = Permission(RoleNeed('wiki_edit'))
delete_permission = Permission(RoleNeed('wiki_delete'))
rename_page_permission = Permission(RoleNeed('wiki_rename_page'))
create_page_permission = Permission(RoleNeed('wiki_create_page'))
edit_protected_permission = Permission(RoleNeed('wiki_edit_protected'))
