from flask import render_template
from . import user

@user.app_errorhandler(404)
def page_not_fund(e):
    return render_template('404.html'),404


@user.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500