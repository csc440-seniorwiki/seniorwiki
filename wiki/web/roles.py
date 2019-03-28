from flask_principal import RoleNeed
from flask_principal import Permission


wiki_edit = 'wiki_edit'
wiki_delete = 'wiki_delete'
wiki_rename_page = 'wiki_rename_page'
wiki_create_page = 'wiki_create_page'
wiki_edit_protected = 'wiki_edit_protected'
wiki_delete_user = 'wiki_delete_user'
wiki_edit_user = 'wiki_edit_user'

edit_permission = Permission(RoleNeed(wiki_edit))
delete_permission = Permission(RoleNeed(wiki_delete))
rename_page_permission = Permission(RoleNeed(wiki_rename_page))
create_page_permission = Permission(RoleNeed(wiki_create_page))
edit_protected_permission = Permission(RoleNeed(wiki_edit_protected))
delete_user_permission = Permission(RoleNeed(wiki_delete_user))
edit_user_permission = Permission(RoleNeed(wiki_edit_user))

wiki_roles = []
wiki_roles.append(tuple([wiki_edit, "Edit Page"]))
wiki_roles.append(tuple([wiki_delete, "Delete Page"]))
wiki_roles.append(tuple([wiki_rename_page, "Rename Page"]))
wiki_roles.append(tuple([wiki_create_page, "Create Page"]))
wiki_roles.append(tuple([wiki_edit_protected, "Edit Protected Page"]))
wiki_roles.append(tuple([wiki_delete_user, "Delete User"]))
wiki_roles.append(tuple([wiki_edit_user, "Edit User Permissions"]))
