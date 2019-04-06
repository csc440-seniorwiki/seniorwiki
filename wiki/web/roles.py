from flask_principal import RoleNeed
from flask_principal import Permission


wiki_edit = 'wiki_edit'
wiki_delete = 'wiki_delete'
wiki_rename_page = 'wiki_rename_page'
wiki_create_page = 'wiki_create_page'
wiki_edit_protected = 'wiki_edit_protected'
wiki_delete_user = 'wiki_delete_user'
wiki_edit_user = 'wiki_edit_user'
wiki_edit_group = 'wiki_edit_group'
wiki_delete_group = 'wiki_delete_group'
wiki_create_group = 'wiki_create_group'

edit_permission = Permission(RoleNeed(wiki_edit))
delete_permission = Permission(RoleNeed(wiki_delete))
rename_page_permission = Permission(RoleNeed(wiki_rename_page))
create_page_permission = Permission(RoleNeed(wiki_create_page))
edit_protected_permission = Permission(RoleNeed(wiki_edit_protected))
delete_user_permission = Permission(RoleNeed(wiki_delete_user))
edit_user_permission = Permission(RoleNeed(wiki_edit_user))
edit_group_permission = Permission(RoleNeed(wiki_edit_group))
delete_group_permission = Permission(RoleNeed(wiki_delete_group))
create_group_permission = Permission(RoleNeed(wiki_create_group))

wiki_roles = []
wiki_roles.append(tuple([wiki_edit, "Edit Page"]))
wiki_roles.append(tuple([wiki_delete, "Delete Page"]))
wiki_roles.append(tuple([wiki_rename_page, "Rename Page"]))
wiki_roles.append(tuple([wiki_create_page, "Create Page"]))
wiki_roles.append(tuple([wiki_edit_protected, "Edit Protected Page"]))
wiki_roles.append(tuple([wiki_delete_user, "Delete User"]))
wiki_roles.append(tuple([wiki_edit_user, "Edit User Permissions"]))
wiki_roles.append(tuple([wiki_edit_group, "Edit Group Permissions"]))
wiki_roles.append(tuple([wiki_delete_group, "Delete Group Permissions"]))
wiki_roles.append(tuple([wiki_create_group, "Delete Group Permissions"]))

wiki_permissions = [edit_permission,
                    delete_permission,
                    rename_page_permission,
                    create_page_permission,
                    rename_page_permission,
                    create_page_permission,
                    edit_protected_permission,
                    delete_user_permission,
                    edit_user_permission,
                    edit_group_permission,
                    delete_group_permission,
                    create_group_permission
                    ]
