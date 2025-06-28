###############################################################################
# To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
# Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
# SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
# The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
# Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
###############################################################################

from . import db, db_utils
from datetime import datetime

import pandas as pd
import xml.etree.ElementTree as ET

def import_excel_post_in_db():

    db.backup_db()
    db_conn = db.get_db()

    PATH_EXCEL = 'flaskr/import/excel/post/post.xlsx'

    # Returns a DataFrame
    df = pd.read_excel(PATH_EXCEL, dtype=str)
    df = df.astype({'numberImagesPost':'int'})

    # If the columns don't exist, initialize it to 0 (for backward compatability with previous version of the app)
    if 'ocrConfidenceCoef' not in df:
        df['ocrConfidenceCoef'] = 0
    if 'oldAccount' not in df:
        df['oldAccount'] = ''
    
    df.rename(columns = { 'type': 'type_' }, inplace = True)   
    
    # Ensure the timestampApify column is interpreted as datetime
    # print("Before datetime", df['timestampApify'])
    df['timestampApify'] = pd.to_datetime(df['timestampApify'])
    
    # Localize timestamp
    # print("After datetime", df['timestampApify'])
    df['timestampApify'] = df['timestampApify'].dt.tz_localize('Europe/Brussels', 'NaT').dt.tz_convert('UTC')

    # Keep only the posts for which an account exists in the database
    account_df = pd.read_sql('SELECT account, postsAsked FROM account', db_conn)
    filtered_df = df[df['account'].isin(account_df['account'])].copy()

    # Insert the free post annotations
    free_text_df = df[['postId', 'freeAnnotationPost']]
    free_text_df.to_sql('free_annotation', db_conn, if_exists='replace', index=True, index_label='id')

    # Remove the column from the filtered dataframe to avoid insert it in the post table
    filtered_df.drop(columns=['freeAnnotationPost'], inplace=True)

    # Keep only the column started by "catPost_" and remove "catPost_" from it
    post_categories_column = [x for x in df.columns if x.startswith('catPost_')]
    account_categories_column = [x for x in df.columns if x.startswith('catAccount_')]

    filtered_df.drop(columns=post_categories_column, inplace=True)
    filtered_df.drop(columns=account_categories_column, inplace=True)
    
    # Insert the post data
    filtered_df.to_sql('post', db_conn, if_exists='replace', index=False, index_label='postId')

    # Find the category and sub_category in the columns
    category_and_sub = db_utils.find_category_and_sub(df, post_categories_column)
    # print(category_and_sub)

    category_list = category_and_sub.keys()
    category_and_sub = db_utils.fill_category_and_sub_with_id(db_conn, category_and_sub, 'post', True)

    # Add the post annotations
    db_utils.add_annotation(db_conn, df, category_and_sub, category_list, 1000, 'postId', 'post')

    # Count the number of posts by account from the database
    posts_df = pd.read_sql('SELECT postId, account FROM post', db_conn)
    posts_occurence_by_account = posts_df.groupby(['account']).size()

    # Update the posts count in account table
    db_utils.update_post_actually_missing_count(db_conn, posts_occurence_by_account, account_df)
    
    return 'ok'


def import_excel_account_in_db():

    db.backup_db()
    db_conn = db.get_db()

    PATH_EXCEL = 'flaskr/import/excel/account/accounts.xlsx'

    # Returns a DataFrame
    df = pd.read_excel(PATH_EXCEL, dtype=str)

    # If the columns don't exist, initialize it to 0 (they will be updated during the import of the posts)
    if 'postsReallyCollected' not in df:
        df['postsReallyCollected'] = 0
    if 'postsMissing' not in df:
        df['postsMissing'] = 0
    if 'postsAsked' not in df:
        df['postsAsked'] = 500
    if 'oldAccount' not in df:
        df['oldAccount'] = ''

    # Insert the free account annotations
    free_text_df = df[['idAccount', 'freeAnnotationAccount']]
    free_text_df.to_sql('free_account_annotation', db_conn, if_exists='replace', index=True, index_label='id')

    # Remove the column freeAnnotationAccount from the dataframe to avoid insert it in the account table
    filtered_df = df.drop(columns=['freeAnnotationAccount'])

    # Keep only the column started by "catAccount_" and remove "catAccount_" from it
    account_categories_column = [x for x in df.columns if x.startswith('catAccount_')]
    post_categories_column = [x for x in df.columns if x.startswith('catPost_')]

    filtered_df.drop(columns=account_categories_column, inplace=True)
    filtered_df.drop(columns=post_categories_column, inplace=True)

    # Insert the account data
    filtered_df.to_sql('account', db_conn, if_exists='replace', index=False)

    # Find the category and sub_category in the columns
    category_and_sub = db_utils.find_category_and_sub(df, account_categories_column)
    # print(category_and_sub)

    category_list = category_and_sub.keys()
    category_and_sub = db_utils.fill_category_and_sub_with_id(db_conn, category_and_sub, 'account', True)

    # Add the account annotations
    db_utils.add_annotation(db_conn, df, category_and_sub, category_list, 1, 'idAccount', 'account')

    return 'ok'

def import_excel_ocr_in_db():

    db.backup_db()
    db_conn = db.get_db()

    PATH_EXCEL = 'flaskr/import/excel/ocr/ocr.xlsx'

    # Get all columns and remove timestampApify from the list because the timezone +00:00 is stuck with pandas due to colon
    cleaned_columns = db_utils.get_columns_name(db_conn, column_name_to_exclude=['timestampApify', 'ocr', 'ocrConfidenceCoef'])

    # post_df = pd.read_sql("SELECT id, account, datetime(timestampApify, '-2 hours') AS timestampApify FROM post", db_conn)
    post_df = pd.read_sql("SELECT " + cleaned_columns +", coalesce(datetime(post.timestampApify,'unixepoch'), datetime(post.timestampApify)) AS timestampApify FROM post", db_conn, parse_dates={'timestampApify': {'format': '%Y-%m-%d %H:%M:%S'}})
    
    # post_df['timestampApify'] = post_df['timestampApify'].apply(str)
    post_df['timestampApify'] = post_df['timestampApify'].dt.tz_localize('UTC')
    #for _, row in post_df.iterrows():
    #    print(row)

    # Returns a DataFrame
    df = pd.read_excel(PATH_EXCEL, dtype=str)

    # Ensure the timestampApify column is interpreted as datetime
    # print("Before datetime", df['timestampApify'])
    df['timestampApify'] = df['timestampApify'].apply(lambda x: str(datetime.strptime(x, '%d-%m-%y_%H-%M-%S')))
    df['timestampApify'] = pd.to_datetime(df['timestampApify'])
    
    # Localize timestamp
    # print("After datetime", df['timestampApify'])
    df['timestampApify'] = df['timestampApify'].dt.tz_localize('UTC')

    # print('post_df : ', post_df['timestampApify'].to_string())
    # print('All : ', df['timestampApify'].to_string())

    merged_df = pd.merge(post_df, df,  how='left', left_on=['account','timestampApify'], right_on = ['account','timestampApify'])
    
    print(merged_df)

    merged_df.to_sql('post', db_conn, if_exists='replace', index=False)

    return 'ok'

def import_txm_post_in_db():

    db.backup_db()
    db_conn = db.get_db()

    PATH_TXM = 'flaskr/import/txm/post/TXMPost.xml'

    tree = ET.parse(PATH_TXM)
    root = tree.getroot()
    category_and_sub = dict()
    post_list = []
    print(root)
    print(root.attrib)
    print(root.tag)
    default_namespace = root.tag[0:root.tag.index('}')+1]
    txm_namespace = '{http://textometrie.org/1.0}'
    print('namespace : ', default_namespace)
    posts = root[1][0]
    # print('debug : ', root[1][0])
    for post in posts:
        # print('debug : ', post)
        if post.tag == (default_namespace + 'post'):
            post_id = post.attrib['number']
            # print('post :', post_id)
            caption = post[1]
            if caption.tag == (default_namespace + 'caption'):
                p = caption[0]
                # print('p :', p.tag, p.attrib)
                for child_p in p:
                    if child_p.tag.startswith(txm_namespace):
                        print('Post id :', post_id)
                        category = child_p.tag[txm_namespace.index('}')+1:]
                        print('Category :', category)
                        sub_category = child_p.attrib['ref']
                        print('Sub-category :', sub_category)
                        if not category_and_sub.get(category):
                            category_and_sub[category] = { 'id' : 0, 'subcat': dict()}
                        category_and_sub[category]['subcat'][sub_category] = { 'id' : 0 }
                        post_list.append((post_id, category, sub_category))
            else:
                # Précaution au cas où le xml aurait changé par rapport à quand ce code a été écrit
                print('Error in parsing, the xml tags are not in the expected order')

    category_and_sub = db_utils.fill_category_and_sub_with_id(db_conn, category_and_sub, 'post')

    print('All : ', category_and_sub)
    index = 1
    max_index = len(post_list)
    for post_tuple in post_list:
        # print(index, '/', max_index)
        db_utils.insert_post_annotation(db_conn, post_tuple[0], category_and_sub[post_tuple[1]]['id'], category_and_sub[post_tuple[1]]['subcat'][post_tuple[2]]['id'])
        index += 1

    return 'ok'

def import_txm_account_in_db():

    db.backup_db()
    db_conn = db.get_db()

    PATH_TXM = 'flaskr/import/txm/account/TXMAccount.xml'

    tree = ET.parse(PATH_TXM)
    root = tree.getroot()
    category_and_sub = dict()
    post_list = []
    print(root)
    print(root.attrib)
    print(root.tag)
    default_namespace = root.tag[0:root.tag.index('}')+1]
    txm_namespace = '{http://textometrie.org/1.0}'
    print('namespace : ', default_namespace)
    posts = root[1][0]
    # print('debug : ', root[1][0])
    for post in posts:
        # print('debug : ', post)
        if post.tag == (default_namespace + 'post'):
            accound_id = post.attrib['number']
            # print('post :', post_id)
            usernametxt = post[1]
            if usernametxt.tag == (default_namespace + 'usernametxt'):
                p = usernametxt[0]
                # print('p :', p.tag, p.attrib)
                for child_p in p:
                    if child_p.tag.startswith(txm_namespace):
                        print('Account id :', accound_id)
                        category = child_p.tag[txm_namespace.index('}')+1:]
                        print('Category :', category)
                        sub_category = child_p.attrib['ref']
                        print('Sub-category :', sub_category)
                        if not category_and_sub.get(category):
                            category_and_sub[category] = { 'id' : 0, 'subcat': dict()}
                        category_and_sub[category]['subcat'][sub_category] = { 'id' : 0 }
                        post_list.append((accound_id, category, sub_category))
            else:
                # Précaution au cas où le xml aurait changé par rapport à quand ce code a été écrit
                print('Error in parsing, the xml tags are not in the expected order')

    # print('Post list',post_list)

    category_and_sub = db_utils.fill_category_and_sub_with_id(db_conn, category_and_sub, 'account')

    print('All : ', category_and_sub)
    index = 1
    max_index = len(post_list)
    for post_tuple in post_list:
        # print(index, '/', max_index)
        db_utils.insert_account_annotation(db_conn, post_tuple[0], category_and_sub[post_tuple[1]]['id'], category_and_sub[post_tuple[1]]['subcat'][post_tuple[2]]['id'])
        index += 1

    return 'ok'
