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
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web import current_user_manager
from wiki.web.user import protect
from wiki.web.roles import edit_permission
from wiki.web.roles import delete_permission
from wiki.web.roles import create_page_permission
from wiki.web.roles import rename_page_permission
from wiki.web.roles import edit_protected_permission
from wiki.web.md2pdf import md2pdf_single_page
from wiki.web.md2pdf import md2pdf_multiple_page
from wiki.web.md2pdf import md2pdf_full_wiki

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
    if wiki_page.protected == 'True':
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
        current_user_manager.add_user(form.name.data, form.password.data)
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
    pass


@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass


@bp.route('/pdf/<path:url>/')
@protect
def single_page_pdf(url):
    return md2pdf_single_page(url, 'pdf_page.html')


@bp.route('/selectpdf/', methods=['GET', 'POST'])
@protect
def multiple_page_pdf():
    return md2pdf_multiple_page('pdf_page.html', 'pdf_select_pages.html')


@bp.route('/fullpdf/')
@protect
def full_wiki_pdf():
    return md2pdf_full_wiki('pdf_page.html')


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
