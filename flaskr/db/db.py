###############################################################################
# To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
# Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
# SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
# The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
# Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
###############################################################################

from . import db_import
from datetime import datetime
from flask import current_app, g

import click
import sqlite3
import os

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys=ON')

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def backup_db():
    
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    path_to_file = 'instance'
    source_name = f'flaskr.sqlite'
    dest_name = f'flaskr_{now}.sqlite'

    if os.name == 'nt':
        os.system(f'copy ".\{path_to_file}\{source_name}" ".\{path_to_file}\{dest_name}"')
    else:
        os.system(f'cp "./{path_to_file}/{source_name}" "./{path_to_file}/{dest_name}"')

    print('Database copy performed successfully.')

@click.command('init-db')
def init_db_command():
    '''Clear the existing data and create new tables.'''
    init_db()
    click.echo('Initialized the database.')

@click.command('import-excel-post-in-db')
def import_excel_post_in_db_command():
    db_import.import_excel_post_in_db()
    click.echo('Filled the database.')

@click.command('import-excel-account-in-db')
def import_excel_account_in_db_command():
    db_import.import_excel_account_in_db()
    click.echo('Filled the database.')

@click.command('import-excel-ocr-in-db')
def import_excel_ocr_in_db_command():
    db_import.import_excel_ocr_in_db()
    click.echo('Filled the database.')

@click.command('import-txm-post-in-db')
def import_txm_post_in_db_command():
    db_import.import_txm_post_in_db()
    click.echo('Filled the database.')

@click.command('import-txm-account-in-db')
def import_txm_account_in_db_command():
    db_import.import_txm_account_in_db()
    click.echo('Filled the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(import_excel_post_in_db_command)
    app.cli.add_command(import_excel_account_in_db_command)
    app.cli.add_command(import_excel_ocr_in_db_command)
    app.cli.add_command(import_txm_post_in_db_command)
    app.cli.add_command(import_txm_account_in_db_command)