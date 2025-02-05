from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
index = Blueprint('index', __name__, template_folder='templates')

@index.route('/')
def root_index():
    return redirect(url_for('player.root_player'))
