###############################################################################
# To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
# Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
# SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
# The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
# Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
###############################################################################

from .. import db, db_utils
from flask import request
from datetime import datetime

import glob
import pandas as pd
import os

def postExportExcelPost():

    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    PATH_EXCEL = f'flaskr/export/excel/post/posts_{now}.xlsx'

    where = request.json["where"]
    sub_corpus = request.json["subCorpus"]

    db_conn = db.get_db()

    post_categories = db_conn.execute(
        "SELECT post_category.title AS 'category', post_category.id AS 'category_id' FROM post_category",
        ()
    ).fetchall()

    post_category_sql = ""
    for row in post_categories:
        row_tuple = tuple(row)
        post_category_sql = post_category_sql + ", \
        group_concat(DISTINCT CASE \
            WHEN annotation.category_id = " + str(row_tuple[1]) + " THEN (SELECT title FROM post_label WHERE post_label.id = annotation.label_id) \
        END) AS 'catPost_" + row_tuple[0] + "'"
        # print(tuple(row))

    account_categories = db_conn.execute(
        "SELECT account_category.title AS 'category', account_category.id AS 'category_id' FROM account_category",
        ()
    ).fetchall()

    account_category_sql = ""
    for row in account_categories:
        row_tuple = tuple(row)
        account_category_sql = account_category_sql + ", \
        group_concat(DISTINCT CASE \
            WHEN account_annotation.category_id = " + str(row_tuple[1]) + " THEN (SELECT title FROM account_label WHERE account_label.id = account_annotation.label_id) \
        END) AS 'catAccount_" + row_tuple[0] + "'"
        # print(tuple(row))

    # Get all columns and remove timestampApify from the list because the timezone +00:00 is stuck with pandas due to colon
    cleaned_column = db_utils.get_columns_name(db_conn, column_name_to_exclude=['timestampApify'])

    sql = "SELECT * FROM (SELECT \
        " + cleaned_column + ", \
        coalesce(datetime(post.timestampApify,'unixepoch'), datetime(post.timestampApify)) AS timestamp_, \
        free_annotation.freeAnnotationPost \
        " + post_category_sql + account_category_sql + " \
    FROM \
        post \
    LEFT JOIN \
        annotation ON post.postId = annotation.post_id \
    LEFT JOIN \
        account_annotation ON post.idAccount = account_annotation.account_id \
    LEFT JOIN \
        free_annotation ON post.postId = free_annotation.postId \
    LEFT JOIN \
        post_label ON post_label.id = annotation.label_id \
    GROUP BY \
        post.postId) \
    LEFT JOIN \
        annotation ON postId = annotation.post_id \
    LEFT JOIN \
        account_annotation ON idAccount = account_annotation.account_id WHERE " + where + "\
    GROUP BY \
        postId;"
    
    # print(sql)

    df = pd.read_sql_query(sql, db_conn, parse_dates={'timestamp_': {'format': '%Y-%m-%d %H:%M:%S'}, 'timestampApify': {'errors': 'ignore'}})
    df.drop(columns=['id', 'post_id', 'account_id', 'category_id', 'label_id' ], inplace=True, errors='ignore')

    if not df.empty:
        df.rename(columns={"type_": "type"}, inplace=True)

        df['timestamp_'] = df['timestamp_'].dt.tz_localize('UTC', True)
        df['timestamp_'] = df['timestamp_'].dt.tz_convert('Europe/Brussels')
        df['timestamp_'] = df['timestamp_'].dt.tz_localize(None, True)
        df['timestampApify'] = df['timestamp_']
        df.drop(columns=['timestamp_'], inplace=True)

        # "date" column for TXM
        df['date'] = df['timestampApify'].dt.strftime('%Y/%m/%d')

        # Add a column with the url of the account
        df['urlAccount'] = 'https://www.instagram.com/' + df['account']

        # Move the column urlAccount after the fullName column
        fullName_col_position = df.columns.get_loc("fullName")
        df.insert(fullName_col_position + 1, 'urlAccount', df.pop('urlAccount'))

        # Add a colum with the list of images that should be exist
        img_path_prefix = f'{os.getcwd()}\\flaskr\static\insta\comptes\\'
        suffix = '.jpg'
        df['imagesLocalPath'] = df.apply(lambda x: generateImgList(img_path_prefix, suffix, x), axis=1)

        if sub_corpus:
            df['imagesLocalPath'].apply(lambda x: copyImgListToExportFolder(x, f'posts_{now}'))

        df['imagesReallyCollected'] = df.apply(lambda x: countExistingImgPerPost(img_path_prefix, x), axis=1)

        df['imagesMissing'] = df['numberImagesPost'] - df['imagesReallyCollected']
        
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(PATH_EXCEL, engine='xlsxwriter', datetime_format='dd-mm-yy hh:mm', engine_kwargs={'options': {'strings_to_urls': False, 'strings_to_formulas': False}})
        df.to_excel(writer, sheet_name='Sheet1', index=False)

        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        worksheet.set_column('A:Z', 20)
        writer.close()

        # print(df)

        return "Data exported"
    else:
        return "No data to export"

def postExportExcelAccount():

    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    PATH_EXCEL = f'flaskr/export/excel/account/accounts_{now}.xlsx'

    where = request.json["where"]
    sub_corpus = request.json["subCorpus"]

    db_conn = db.get_db()

    categories = db_conn.execute(
        "SELECT account_category.title AS 'category', account_category.id AS 'category_id' FROM account_category",
        ()
    ).fetchall()

    category_sql = ""
    for row in categories:
        row_tuple = tuple(row)
        category_sql = category_sql + ", \
        group_concat(DISTINCT CASE \
            WHEN account_annotation.category_id = " + str(row_tuple[1]) + " THEN (SELECT title FROM account_label WHERE account_label.id = account_annotation.label_id) \
        END) AS 'catAccount_" + str(row_tuple[0]).replace("'","''") + "'"
        # print(tuple(row))

    sql = "SELECT * FROM (SELECT \
        account.*, \
        free_account_annotation.freeAnnotationAccount \
        " + category_sql + " \
    FROM \
        account \
    LEFT JOIN \
        account_annotation ON account.idAccount = account_annotation.account_id \
    LEFT JOIN \
        free_account_annotation ON account.idAccount = free_account_annotation.idAccount \
    LEFT JOIN \
        account_label ON account_label.id = account_annotation.label_id \
    GROUP BY \
        account.idAccount) LEFT JOIN account_annotation ON idAccount = account_annotation.account_id WHERE " + where + " \
    GROUP BY idAccount;"
    
    # print(sql)

    df = pd.read_sql_query(sql, db_conn)
    df.drop(columns=['id', 'account_id', 'category_id', 'label_id' ], inplace=True, errors='ignore')

    if not df.empty:
        # Add a column with the url of the account
        df['urlAccount'] = 'https://www.instagram.com/' + df['account']

        # Move the column urlAccount after the fullName column
        fullName_col_position = df.columns.get_loc("fullName")
        df.insert(fullName_col_position + 1, 'urlAccount', df.pop('urlAccount'))

        # Add a colum with the path of account image that should be exist
        img_path_prefix = f'{os.getcwd()}\\flaskr\static\insta\profilepictures\\'
        suffix = '_pic.jpg'
        df['imagesLocalPathAccount'] = img_path_prefix + df['account'] + suffix

        if sub_corpus:
            df['imagesLocalPathAccount'].apply(lambda x: copyImgListToExportFolder(x, f'accounts_{now}'))
        
        # Create a Pandas Excel writer using XlsxWriter as the engine. python 3.11
        writer = pd.ExcelWriter(PATH_EXCEL, engine='xlsxwriter', datetime_format='dd-mm-yy hh:mm', engine_kwargs={'options':{'strings_to_urls': False, 'strings_to_formulas': False}})
        df.to_excel(writer, sheet_name='Sheet1', index=False)

        worksheet = writer.sheets['Sheet1']
        worksheet.set_column('A:Z', 20)
        writer.close()

        # print(df)

        return "Data exported"
    else:
        return "No data to export"

def generateImgList(img_path_prefix, suffix, row):
    img_list = ''
    delimiter = ';'
    formatted_date = row['timestampApify'].tz_localize('Europe/Brussels', True).tz_convert('UTC').strftime('%d-%m-%y_%H-%M-%S')
    img_name = f'{row.account}_{formatted_date}'

    for i in range(1,row['numberImagesPost']+1):
        # Don't use [] because we are in an f string
        img_list = f'{img_list}{img_path_prefix}{row.account}\{img_name}_{i}_{row.numberImagesPost}{suffix}'
        if i < row['numberImagesPost']:
            img_list = f'{img_list}{delimiter}'

    return img_list

def countExistingImgPerPost(img_path_prefix,row):
    formatted_date = row['timestampApify'].tz_localize('Europe/Brussels', True).tz_convert('UTC').strftime('%d-%m-%y_%H-%M-%S')
    img_name = f'{row.account}_{formatted_date}'
    pattern = f'{img_path_prefix}{row.account}\{img_name}_*'
    # print(pattern)
    list_img = glob.glob(pattern)
    # print(list_img)

    return len(list_img)

def copyImgListToExportFolder(img_list, destination_folder):

    delimiter = ';'
    img_list_splitted = img_list.split(delimiter)

    for img in img_list_splitted:
        img_name = img.split('\static\insta\\')[-1]

        img_dest = f'flaskr\export\img\{destination_folder}\{img_name}'
        # xcopy will create the folder if it doesn't exist
        os.system(f'echo F|xcopy "{img}" "{img_dest}" /c')

    return