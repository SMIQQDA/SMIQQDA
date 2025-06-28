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
def getFreeAnnotations():

    post_id = request.args.get("postId")

    db_conn = db.get_db()
    free_annotations = db_conn.execute(
        "SELECT id, freeAnnotationPost FROM free_annotation WHERE postId = ?",
        ([post_id])
    ).fetchall()

    results = [tuple(row) for row in free_annotations]
    
    return json.dumps(results, ensure_ascii=False)

# Store the annotation in the database and return the id of the annotation
def postFreeAnnotations():

    post_id = request.json["post_id"]
    free_text = request.json["free_text"]
    # print(post_id, free_text)
    db_conn = db.get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        "UPDATE free_annotation SET freeAnnotationPost = ? WHERE postId = ?",
        (free_text, post_id)
    ).fetchall()
    db_conn.commit()

    results = cursor.lastrowid
    
    return json.dumps(results, ensure_ascii=False)

# Return the list of annotations from the database for one account
def getFreeAccountAnnotations():

    account_id = request.args.get("accountId")

    db_conn = db.get_db()
    free_annotations = db_conn.execute(
        "SELECT id, freeAnnotationAccount FROM free_account_annotation WHERE idAccount = ?",
        ([account_id])
    ).fetchall()

    results = [tuple(row) for row in free_annotations]
    
    return json.dumps(results, ensure_ascii=False)

# Store the annotation in the database and return the id of the annotation
def postFreeAccountAnnotations():

    account_id = request.json["account_id"]
    free_text = request.json["free_text"]

    # print(account_id, free_text)

    db_conn = db.get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        "UPDATE free_account_annotation SET freeAnnotationAccount = ? WHERE idAccount = ?",
        (free_text, account_id)
    ).fetchall()
    db_conn.commit()

    results = cursor.lastrowid
    
    return json.dumps(results, ensure_ascii=False)