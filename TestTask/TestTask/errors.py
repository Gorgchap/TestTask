from flask import render_template
from TestTask import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('page-500.html'), 500
