###############################################################################
# To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
# Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
# SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
# The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
# Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
###############################################################################

from .. import db
from flask import request

# Return an array with the account names (i.e. all directory names)
def getAccountList():

    account_annotation_id_list = request.args.getlist("accountAnnotationId")
    post_annotation_id_list = request.args.getlist("postAnnotationId")
    date = request.args.get("date")
    account_only = request.args.get("accountOnly")
    # print("Account, annotation list : ", annotation_id_list)
    # print("Date : ", date)
    sql_query_params = []

    db_conn = db.get_db()

    if(account_only):
        if(len(account_annotation_id_list) > 0):
            sql="SELECT DISTINCT(account) FROM account JOIN account_annotation ON account_annotation.account_id = account.idAccount WHERE account_annotation.label_id IN ({seq}) GROUP BY account HAVING count(DISTINCT account_annotation.label_id) = {lenght} ORDER BY account".format(seq=','.join(['?']*len(account_annotation_id_list)), lenght=str(len(account_annotation_id_list)))
            accounts = db_conn.execute(sql, account_annotation_id_list).fetchall()
        else:
            accounts = db_conn.execute(
            "SELECT DISTINCT(account) FROM account ORDER BY account"
            ).fetchall()
    else:
        if(len(post_annotation_id_list) > 0 or len(account_annotation_id_list) > 0):

            sql="SELECT DISTINCT(account) FROM post JOIN annotation ON annotation.post_id = post.postId "
            
            if(len(account_annotation_id_list) > 0):
                sql = sql + "JOIN account_annotation ON account_annotation.account_id = post.idAccount"

            sql = sql + " WHERE "

            if(len(account_annotation_id_list) > 0):
                sql = sql + "account_annotation.label_id IN ({seq})".format(seq=','.join(['?']*len(account_annotation_id_list)))
                sql_query_params = account_annotation_id_list

            if(len(post_annotation_id_list) > 0 and len(account_annotation_id_list) > 0):
                sql = sql + " AND "

            if(len(post_annotation_id_list) > 0):
                sql = sql + "annotation.label_id IN ({seq}) GROUP BY account HAVING count(DISTINCT annotation.label_id) = {lenght} ORDER BY account".format(seq=','.join(['?']*len(post_annotation_id_list)), lenght=str(len(post_annotation_id_list)))
                sql_query_params += post_annotation_id_list

            if(date):
                sql = sql + " AND (date(post.timestampApify) = ? OR date(post.timestampApify, 'unixepoch') = ?)"
                # Add the parameters to the list to have the right number of parameters required for the query
                sql_query_params.append(date)
                sql_query_params.append(date)

            print(sql)
            print("SQL query parameters: ")
            print(sql_query_params)
            accounts = db_conn.execute(sql, sql_query_params).fetchall()
        else:
            if(date):
                accounts = db_conn.execute(
                "SELECT DISTINCT(account) FROM post WHERE (date(post.timestampApify) = ? OR date(post.timestampApify, 'unixepoch') = ?) ORDER BY account"
                , (date, date)).fetchall()
            else:
                accounts = db_conn.execute(
                "SELECT DISTINCT(account) FROM post ORDER BY account"
                ).fetchall()

    # Return an array of array with category_id, category, label_id, label
    results_tuple = [tuple(row) for row in accounts]
    results = []
    for result in results_tuple:
        results.append(result[0])

    return results

# Return an array with the account names (i.e. all directory names)
def getAccount(account: str):

    data = {}
    db_conn = db.get_db()
            
    rows = db_conn.execute(
    "SELECT idAccount, account, fullName, biography, externalUrl, postsCount, followersCount, followsCount, \
         postsReallyCollected, postsMissing, postsAsked FROM account WHERE account = ?"
    , ([account])).fetchall()

    if(len(rows) > 0):
        data['idAccount'] = str(rows[0][0]) # Convert into string because JS doesn't like BigInt
        data['account'] = (rows[0][1])
        data['fullName'] = (rows[0][2])
        data['biography'] = (rows[0][3])
        data['externalUrl'] = (rows[0][4])
        data['postsCount'] = (rows[0][5])
        data['followersCount'] = (rows[0][6])
        data['followsCount'] = (rows[0][7])
        data['postsReallyCollected'] = (rows[0][8])
        data['postsMissing'] = (rows[0][9])
        data['postsAsked'] = (rows[0][10])

    return data