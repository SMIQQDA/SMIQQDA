###############################################################################
# To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
# Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
# SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
# The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
# Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
###############################################################################

from .. import db
from flask import request

import glob
import json
import pandas as pd
import os

# Return an array with the post ids
def getPostList(username: str):

    annotation_id_list = request.args.getlist("postAnnotationId")
    date = request.args.get("date")
    
    db_conn = db.get_db()

    if(len(annotation_id_list) > 0):
        sql="SELECT post.postId FROM post JOIN annotation ON annotation.post_id = post.postId WHERE post.account = ? AND annotation.label_id IN ({seq}) GROUP BY post.postId HAVING count(DISTINCT annotation.label_id) = {lenght}".format(seq=','.join(['?']*len(annotation_id_list)), lenght=str(len(annotation_id_list)))
        print(sql)
        annotation_id_list.insert(0, username)
        if(date):
            sql = sql + " AND (date(post.timestampApify) = ? OR date(post.timestampApify, 'unixepoch') = ?)"
            # Add the parameters to the list to have the right number of parameters required for the query
            annotation_id_list.append(date)
            annotation_id_list.append(date)
            accounts = db_conn.execute(
                sql, (annotation_id_list)).fetchall()
        else:
            accounts = db_conn.execute(
                sql, annotation_id_list).fetchall()
    else:
        db_conn = db.get_db()
        sql="SELECT DISTINCT(post.postId) FROM post WHERE account = ?"
        if(date):
            sql = sql + " AND (date(post.timestampApify) = ? OR date(post.timestampApify, 'unixepoch') = ?)"
            accounts = db_conn.execute(
            sql,(username, date, date)).fetchall()
        else:
            accounts = db_conn.execute(
            sql,([username])).fetchall()

    results_tuple = [tuple(row) for row in accounts]
    results = []
    for result in results_tuple:
        results.append(str(result[0]))
    return results

# Return the content of the DB
def getPost(username: str, post_id: str):
    data = {}

    db_conn = db.get_db()
    rows = db_conn.execute(
        "SELECT post.postId, ocr, coalesce(datetime(timestampApify, 'unixepoch'), datetime(timestampApify)) AS timestampApify , numberImagesPost, \
        caption, locationName, likesCount, commentsCount, account.fullName AS owner_full_name, post.urlPost, \
        account.postsCount, account.postsReallyCollected, account.postsMissing, account.followersCount, account.followsCount, post.type_, post.account FROM post \
        JOIN account ON account.account = post.account WHERE post.postId = ?",
        ([post_id])
    ).fetchall()
    if(len(rows) > 0):
        data['postId'] = str(rows[0][0]) # Convert into string because JS doesn't like BigInt
        data['ocr'] = (rows[0][1])
        data['timestamp'] = (rows[0][2])
        data['totalImage'] = getTotalImage(rows[0][16],rows[0][2]) # Get the number of images in the directory because numberImagesPost is not always correct
        data['caption'] = (rows[0][4])
        data['localisation'] = (rows[0][5])
        data['likesCount'] = (rows[0][6])
        data['commentsCount'] = (rows[0][7])
        data['ownerFullName'] = (rows[0][8])
        data['url'] = (rows[0][9])
        data['postsCount'] = (rows[0][10])
        data['postsReallyCollected'] = (rows[0][11])
        data['postsMissing'] = (rows[0][12])
        data['followersCount'] = (rows[0][13])
        data['followsCount'] = (rows[0][14])
        data['type'] = (rows[0][15])
    # print(data)
    return data

def getPostCount():

    account_list = request.args.getlist("account")
    print(account_list)
    annotation_id_list = request.args.getlist("postAnnotationId")
    date = request.args.get("date")
    sql_query_params = []
    
    db_conn = db.get_db()

    if(len(annotation_id_list) > 0):
        if(len(account_list) > 0):
            sql="SELECT count(post.postId) FROM post JOIN annotation ON annotation.post_id = post.postId WHERE post.account IN ({seq}) AND annotation.label_id IN ({seq2}) GROUP BY post.postId HAVING count(DISTINCT annotation.label_id) = {lenght}".format(seq=','.join(['?']*len(account_list)), seq2=','.join(['?']*len(annotation_id_list)), lenght=str(len(annotation_id_list)))
            sql_query_params = account_list + annotation_id_list
        else:
            sql="SELECT count(post.postId) FROM post JOIN annotation ON annotation.post_id = post.postId WHERE annotation.label_id IN ({seq}) GROUP BY post.postId HAVING count(DISTINCT annotation.label_id) = {lenght}".format(seq=','.join(['?']*len(annotation_id_list)), lenght=str(len(annotation_id_list)))
            sql_query_params = annotation_id_list
        print(sql)

        if(date):
            sql = sql + " AND (date(post.timestampApify) = ? OR date(post.timestampApify, 'unixepoch') = ?)"
            # Add the parameters to the list to have the right number of parameters required for the query
            sql_query_params.append(date)
            sql_query_params.append(date)
            rows = db_conn.execute(
                sql, (sql_query_params)).fetchall()
        else:
            rows = db_conn.execute(
                sql, sql_query_params).fetchall()
    else:
        db_conn = db.get_db()
        sql="SELECT count(post.postId) FROM post"

        if(len(account_list) > 0 or date):
            sql = sql + " WHERE "

            if(len(account_list) > 0):
                sql = sql + "post.account IN ({seq})".format(seq=','.join(['?']*len(account_list)))
                sql_query_params = account_list
                print(sql)
                if(date):
                    sql = sql + " AND "

            if(date):
                sql = sql + "(date(post.timestampApify) = ? OR date(post.timestampApify, 'unixepoch') = ?)"
                sql_query_params.append(date)
                sql_query_params.append(date)
                print(sql)

            rows = db_conn.execute(
            sql,(sql_query_params)).fetchall()
        else:
            rows = db_conn.execute(
            sql).fetchall()

    results_tuple = [tuple(row) for row in rows]
    results = 0
    for result in results_tuple:
        results += result[0]

    return str(results)

# Store a post in the database
# Used only for debug
def postPost(username: str, post_name: str):
    
    post_name_without_extension = post_name.split(".json")
    post_name_splitted = post_name_without_extension[0].split("_")
    print(post_name_splitted)
    created = post_name_splitted[1] + " " + post_name_splitted[2].replace("-",":")

    db_conn = db.get_db()
    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT INTO post (account, file_name, created) VALUES (?, ?, ?)",
        (username, post_name, created)
    ).fetchall()
    db_conn.commit()

    results = cursor.lastrowid
    
    return json.dumps(results, ensure_ascii=False)

def getTotalImage(account: str, timestamp: str):

    img_path_prefix = f'{os.getcwd()}\\flaskr\static\insta\comptes\\'
    formatted_date = pd.Timestamp(timestamp, tz='Europe/Brussels').strftime('%d-%m-%y_%H-%M-%S')

    img_name = f'{account}_{formatted_date}'
    pattern = f'{img_path_prefix}{account}\{img_name}_*'

    # print(pattern)
    list_img = glob.glob(pattern)
    # print(list_img)

    return len(list_img)