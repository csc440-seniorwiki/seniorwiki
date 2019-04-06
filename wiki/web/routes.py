"""
    Routes
    ~~~~~~
"""
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import current_app
from flask import session
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_principal import Identity
from flask_principal import AnonymousIdentity
from flask_principal import identity_changed

from wiki.core import Processor
from wiki.web.forms import EditorForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web.forms import RegisterForm
from wiki.web.forms import UserRoleForm
from wiki.web.forms import GroupRoleForm
from wiki.web.forms import CreateGroupForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web import current_group_manager
from wiki.web import load_user
from wiki.web import load_group
from wiki.web.user import protect
from wiki.web.roles import edit_permission
from wiki.web.roles import delete_permission
from wiki.web.roles import create_page_permission
from wiki.web.roles import rename_page_permission
from wiki.web.roles import edit_protected_permission
from wiki.web.roles import delete_user_permission
from wiki.web.roles import edit_user_permission
from wiki.web.roles import edit_group_permission
from wiki.web.roles import delete_group_permission
from wiki.web.roles import create_group_permission
from wiki.web.roles import wiki_roles

bp = Blueprint('wiki', __name__)


@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
@create_page_permission.require(http_exception=401)
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
@edit_permission.require(http_exception=401)
def edit(url):
    def load_page(page, can_edit):
        form = EditorForm(obj=page)
        if form.validate_on_submit():
            if not page:
                page = current_wiki.get_bare(url)
            form.populate_obj(page)
            page.save()
            flash('"%s" was saved.' % page.title, 'success')
            return redirect(url_for('wiki.display', url=url))
        return render_template('editor.html', form=form, page=page, can_edit_protected_permission=can_edit)

    wiki_page = current_wiki.get(url)
    if wiki_page and wiki_page.protected == 'True':
        with edit_protected_permission.require(http_exception=401):
            return load_page(wiki_page, True)
    else:
        if edit_protected_permission.can():
            return load_page(wiki_page, True)
        return load_page(wiki_page, False)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
@rename_page_permission.require(http_exception=401)
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
@delete_permission.require(http_exception=401)
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        login_user(user)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.name))
        user.set('authenticated', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('login.html', form=form)


@bp.route('/user/register/', methods=['GET', 'POST'])
def user_register():
    form = RegisterForm()
    if form.validate_on_submit():
        current_users.add_user(form.name.data, form.password.data)
        flash('Registration successful, please login.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.user_login'))
    return render_template('register.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
def user_index():
    users = current_users.index()
    return render_template('userindex.html', users=users)

@bp.route('/group/')
def group_index():
    groups = current_group_manager.index()
    return render_template('groupindex.html', groups=groups)

@bp.route('/user/<string:user_id>/', methods=['GET', 'POST'])
@protect
@edit_user_permission.require(http_exception=401)
def user_admin(user_id):
    form = UserRoleForm()
    form.roles.choices = wiki_roles
    form.groups.choices = map(lambda x: tuple([x.get_id(), x.get_id()]), current_group_manager.get_groups())
    if form.validate_on_submit():
        user = load_user(user_id)
        user.set('roles', form.roles.data)
        user.set('groups', form.groups.data)
        return redirect(request.args.get("next") or url_for('wiki.user_login'))
    return render_template('useradmin.html', form=form, page= {"url": user_id})


@bp.route('/user/delete/<string:user_id>/')
@protect
@delete_user_permission.require(http_exception=401)
def user_delete(user_id):
    current_users.delete_user(user_id)
    flash('User deleted.', 'success')
    return redirect(request.args.get("next") or url_for('wiki.user_login'))


@bp.route('/group/create/', methods=['GET', 'POST'])
@create_group_permission.require(http_exception=401)
def group_create():
    form = CreateGroupForm()
    form.roles.choices = wiki_roles
    if form.validate_on_submit():
        current_group_manager.add_group(form.name.data, form.roles.data)
        flash('Group creation successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('creategroup.html', form=form)


@bp.route('/group/<string:group_id>/', methods=['GET', 'POST'])
@protect
@edit_group_permission.require(http_exception=401)
def group_admin(group_id):
    form = GroupRoleForm()
    form.roles.choices = wiki_roles
    if form.validate_on_submit():
        group = load_group(group_id)
        group.set('roles', form.roles.data)
        return redirect(request.args.get("next") or url_for('wiki.user_login'))
    return render_template('groupadmin.html', form=form)


@bp.route('/group/delete/<string:group_id>/', methods=['GET', 'POST'])
@protect
@delete_group_permission.require(http_exception=401)
def group_delete(group_id):
    current_group_manager.delete_group(group_id)
    flash('Group deleted.', 'success')
    return redirect(request.args.get("next") or url_for('wiki.index'))

"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(401)
def page_not_found(error):
    return render_template('401.html'), 401


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
