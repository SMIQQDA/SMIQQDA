###############################################################################
# To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
# Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
# SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
# The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
# Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
###############################################################################

from .. import db
from flask import request

import json

# Return the list of annotations from the database for one post
def getAnnotations():

    post_id = request.args.get("postId")

    db_conn = db.get_db()
    annotations = db_conn.execute(
        "SELECT id, label_id FROM annotation WHERE post_id = ?",
        ([post_id])
    ).fetchall()

    results = [tuple(row) for row in annotations]
    
    return json.dumps(results, ensure_ascii=False)

# Store the annotation in the database and return the id of the annotation
def postAnnotations():

    post_id = request.json["post_id"]
    category_id = request.json["category_id"]
    label_id = request.json["label_id"]
    # print(post_id, label_id)
    db_conn = db.get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT INTO annotation (post_id, category_id, label_id) VALUES (?, ?, ?)",
        (post_id, category_id, label_id)
    ).fetchall()
    db_conn.commit()

    results = cursor.lastrowid
    
    return json.dumps(results, ensure_ascii=False)

# Delete the annotation in the database and return the number of row deleted
def deleteAnnotations(post_id: str, category_id: str):
    # print(category_id)
    db_conn = db.get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        "DELETE FROM annotation WHERE post_id = ? AND category_id = ?",
        (post_id, category_id)
    ).fetchall()
    db_conn.commit()

    results = cursor.rowcount
    
    return json.dumps(results, ensure_ascii=False)

# Return the list of annotations from the database for one post
def getAccountAnnotations():

    account_id = request.args.get("accountId")

    db_conn = db.get_db()
    annotations = db_conn.execute(
        "SELECT id, label_id FROM account_annotation WHERE account_id = ?",
        ([account_id])
    ).fetchall()

    results = [tuple(row) for row in annotations]
    
    return json.dumps(results, ensure_ascii=False)

# Store the annotation in the database and return the id of the annotation
def postAccountAnnotations():

    account_id = request.json["account_id"]
    category_id = request.json["category_id"]
    label_id = request.json["label_id"]
    # print(account_id, label_id)
    db_conn = db.get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT INTO account_annotation (account_id, category_id, label_id) VALUES (?, ?, ?)",
        (account_id, category_id, label_id)
    ).fetchall()
    db_conn.commit()

    results = cursor.lastrowid
    
    return json.dumps(results, ensure_ascii=False)

# Delete the annotation in the database and return the number of row deleted
def deleteAccountAnnotations(account_id:str, category_id: str):
    # print(category_id)
    db_conn = db.get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        "DELETE FROM account_annotation WHERE account_id = ? AND category_id = ?",
        (account_id, category_id)
    ).fetchall()
    db_conn.commit()

    results = cursor.rowcount
    
    return json.dumps(results, ensure_ascii=False)