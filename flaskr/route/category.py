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

# Return the list of category from the database
def getCategories(category_type: str):

    table_category = getCategoryTable(category_type)
    table_label = getLabelTable(category_type)

    select_all = request.args.get("selectAll")
    if(select_all):
        # print("SELECT ALL")
        sql = f"SELECT {table_category}.title AS 'category', {table_category}.id AS 'category_id' , {table_label}.title AS 'label' , {table_label}.id AS 'label_id', {table_category}.deleted, {table_label}.deleted FROM {table_category} LEFT JOIN {table_label} ON {table_category}.id = {table_label}.category_id ORDER BY {table_category}.title"
    else:
        # print("SELECT PAS ALL")
        sql = f"SELECT {table_category}.title AS 'category', {table_category}.id AS 'category_id' , {table_label}.title AS 'label' , {table_label}.id AS 'label_id', {table_category}.deleted, {table_label}.deleted FROM {table_category} LEFT JOIN {table_label} ON {table_category}.id = {table_label}.category_id WHERE {table_category}.deleted = 0 AND {table_label}.deleted = 0 ORDER BY {table_category}.title"
    db_conn = db.get_db()
    print(sql)
    
    categories = db_conn.execute(sql).fetchall()
    # Return an array of array with category_id, category, label_id, label
    results = [tuple(row) for row in categories]
    # print(results)
    
    return json.dumps(results, ensure_ascii=False)
    
# Add a category
def postCategory(category_type: str):

    table = getCategoryTable(category_type)

    category_title = request.json["category_title"]

    db_conn = db.get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        f"INSERT INTO {table} (title) VALUES (?)",
        ([category_title])
    ).fetchall()
    db_conn.commit()

    results = cursor.lastrowid
    
    return json.dumps(results, ensure_ascii=False)
    
# Archive a category
def archiveCategory(category_type: str, category_id: str):

    table = getCategoryTable(category_type)

    db_conn = db.get_db()
    categories = db_conn.execute(
        f"UPDATE {table} SET deleted = 1 WHERE id = ?", ([category_id])
    ).fetchall()
    db_conn.commit()

    results = [tuple(row) for row in categories]
    
    return json.dumps(results, ensure_ascii=False)

# Unarchive a category
def unarchiveCategory(category_type: str, category_id: str):

    table = getCategoryTable(category_type)

    db_conn = db.get_db()
    categories = db_conn.execute(
        f"UPDATE {table} SET deleted = 0 WHERE id = ?", ([category_id])
    ).fetchall()
    db_conn.commit()

    results = [tuple(row) for row in categories]
    
    return json.dumps(results, ensure_ascii=False)

# Delete the category in the database and return the number of row deleted
def deleteCategory(category_type: str, category_id: str):

    table = getCategoryTable(category_type)

    # print(category_id)
    db_conn = db.get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        f"DELETE FROM {table} WHERE id = ?",
        ([category_id])
    ).fetchall()
    db_conn.commit()

    results = cursor.rowcount
    
    return json.dumps(results, ensure_ascii=False)

# Add a label
def postLabel(category_type: str):

    table = getLabelTable(category_type)

    category_id = request.json["category_id"]
    label_title = request.json["label_title"]

    db_conn = db.get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        f"INSERT INTO {table} (category_id, title) VALUES (?, ?)",
        (category_id, label_title)
    ).fetchall()
    db_conn.commit()

    results = cursor.lastrowid
    
    return json.dumps(results, ensure_ascii=False)

# Archive a label
def archiveLabel(category_type: str, label_id: str):

    table = getLabelTable(category_type)

    db_conn = db.get_db()
    labels = db_conn.execute(
        f"UPDATE {table} SET deleted = 1 WHERE id = ?", ([label_id])
    ).fetchall()
    db_conn.commit()

    results = [tuple(row) for row in labels]
    # print(results)
    
    return json.dumps(results, ensure_ascii=False)

# Unarchive a label
def unarchiveLabel(category_type: str, label_id: str):

    table = getLabelTable(category_type)

    db_conn = db.get_db()
    labels = db_conn.execute(
        f"UPDATE {table} SET deleted = 0 WHERE id = ?", ([label_id])
    ).fetchall()
    db_conn.commit()

    results = [tuple(row) for row in labels]
    
    return json.dumps(results, ensure_ascii=False)

# Delete the label in the database and return the number of row deleted
def deleteLabel(category_type: str, label_id: str):

    table = getLabelTable(category_type)

    # print(label_id)
    db_conn = db.get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        f"DELETE FROM {table} WHERE id = ?",
        ([label_id])
    ).fetchall()
    db_conn.commit()

    results = cursor.rowcount
    
    return json.dumps(results, ensure_ascii=False)

def getCategoryTable(category_type: str):
    if category_type == "account":
        table = "account_category"
    else:
        table = "post_category"
    return table

def getLabelTable(category_type: str):
    if category_type == "account":
        table = "account_label"
    else:
        table = "post_label"
    return table