import os

from flask import current_app
from flask import Flask
from flask import g
from flask_login import LoginManager
from flask_login import current_user
from werkzeug.local import LocalProxy
from flask_principal import Principal
from wiki.core import Wiki
from wiki.web.user import UserManager
from wiki.web.poll import PollManager
from wiki.web.group import GroupManager
from flask_principal import identity_loaded, RoleNeed, UserNeed


class WikiError(Exception):
    pass


def get_wiki():
    wiki = getattr(g, '_wiki', None)
    if wiki is None:
        wiki = g._wiki = Wiki(current_app.config['CONTENT_DIR'])
    return wiki


current_wiki = LocalProxy(get_wiki)


def get_users():
    users = getattr(g, '_users', None)
    if users is None:
        users = g._users = UserManager(current_app.config['USER_DIR'])
        g._user_manager = UserManager(current_app.config['USER_DIR'])
    return users


current_users = LocalProxy(get_users)


def get_group_manager():
    group_manager = getattr(g, '_group_manager', None)
    if group_manager is None:
        g._group = GroupManager(current_app.config['USER_DIR'])
        group_manager = g._group_manager = GroupManager(current_app.config['USER_DIR'])
    return group_manager


current_group_manager = LocalProxy(get_group_manager)

def get_poll_manager():
    return PollManager(current_app.config['USER_DIR'])


current_poll_manager = LocalProxy(get_poll_manager)

def create_app(directory):
    app = Flask(__name__)
    app.config['CONTENT_DIR'] = directory
    app.config['TITLE'] = 'wiki'
    try:
        app.config.from_pyfile(
            os.path.join(app.config.get('CONTENT_DIR'), 'config.py')
        )
    except IOError:
        msg = "You need to place a config.py in your content directory."
        raise WikiError(msg)

    loginmanager.init_app(app)

    principals = Principal(app)

    from wiki.web.routes import bp
    app.register_blueprint(bp)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Assign user privileges based on their roles and group membership
        if not current_user.is_anonymous:
            if current_user.get('roles'):
                for role in current_user.get('roles'):
                    identity.provides.add(RoleNeed(role))
            if current_user.get('groups'):
                for user_group in current_user.get('groups'):
                    for role in load_group(user_group).get('roles'):
                        identity.provides.add(RoleNeed(role))

    return app


loginmanager = LoginManager()
loginmanager.login_view = 'wiki.user_login'


@loginmanager.user_loader
def load_user(name):
    return current_users.get_user(name)


def load_group(name):
    return current_group_manager.get_group(name)

