###############################################################################
# To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
# Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
# SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
# The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
# Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
###############################################################################

import pandas as pd

def find_category_and_sub(df, categories_column):

    category_and_sub = dict()

    for category in categories_column:
        category_and_sub[category] = { 'id' : 0, 'subcat': dict()}
        sub_category_values = df[category].unique()

        for sub_category in sub_category_values:
            if not pd.isna(sub_category):
                category_and_sub[category]['subcat'][sub_category] = { 'id' : 0 }

    return category_and_sub

def fill_category_and_sub_with_id(db_conn, category_and_sub, category_type='account', remove_prefix=False):

    if category_type == 'account':
        char_to_remove =  len('catAccount_')
    else:
        char_to_remove =  len('catPost_')

    category_list = category_and_sub.keys()

    for category_title in category_list:
        
        if remove_prefix:
            category_id = insert_category(db_conn, category_title[char_to_remove:], category_type) # remove the 'cat_'
            # print("remove pre and cat id ", category_id)
        else:
            category_id = insert_category(db_conn, category_title, category_type)
            # print("cat id ", category_id)
        category_and_sub[category_title]['id'] = category_id

        sub_category_list = category_and_sub[category_title]['subcat'].keys()

        for sub_category_title in sub_category_list:
            # print("insert label", category_id, sub_category_title)
            label_id = insert_label(db_conn, category_id, sub_category_title, category_type)
            category_and_sub[category_title]['subcat'][sub_category_title]['id'] = label_id

        # print(category_title, sub_category_title, label_id)

    return category_and_sub

def add_annotation(db_conn, df, category_and_sub, category_list, modulo_print, id_column_name, mode):

    # print('All : ', category_and_sub)
    index = 1
    max_index = len(df. index)
    for _, row in df.iterrows():
        if(index % modulo_print == 0 or index == max_index):
            print(index, '/', max_index)
        for category_title in category_list:
            # print(category_and_sub[category_title]['id'])
            # print(row[category_title])
            if not pd.isna(row[category_title]):
                # print(category_and_sub[category_title]['subcat'][row[category_title]]['id'])
                if mode == 'account':
                    insert_account_annotation(db_conn, str(row[id_column_name]), category_and_sub[category_title]['id'], category_and_sub[category_title]['subcat'][row[category_title]]['id'])
                elif mode == 'post':
                    insert_post_annotation(db_conn, str(row[id_column_name]), category_and_sub[category_title]['id'], category_and_sub[category_title]['subcat'][row[category_title]]['id'])
            else:
                if mode == 'account':
                    delete_account_annotation(db_conn, str(row[id_column_name]), category_and_sub[category_title]['id'])
                elif mode == 'post':
                    delete_post_annotation(db_conn, str(row[id_column_name]), category_and_sub[category_title]['id'])
        index += 1

def insert_post_annotation(db_conn, post_id, category_id, label_id):
        
    if not post_id.isnumeric():
        print("Bad post id during the insert of the annotation. Value : ", post_id, "Type : ", type(post_id))

    # print("insert ", post_id, category_id, label_id)
    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT INTO annotation (post_id, category_id, label_id) VALUES (?, ?, ?) ON CONFLICT (post_id, category_id) DO UPDATE SET label_id=excluded.label_id",
        (post_id, category_id, label_id)
    ).fetchall()
    db_conn.commit()

def delete_post_annotation(db_conn, post_id, category_id):
        
    if not post_id.isnumeric():
        print("Bad post id during the deletion of the annotation. Value : ", post_id, "Type : ", type(post_id))

    # print("Delete the post annotation if it already exist.", "Post id : ", post_id, "Category id : " ,category_id)
    cursor = db_conn.cursor()
    cursor.execute(
        "DELETE FROM annotation WHERE post_id = ?  AND  category_id = ?",
        (post_id, category_id)
    ).fetchall()
    db_conn.commit()

def insert_account_annotation(db_conn, account_id, category_id, label_id):
        
    if not account_id.isnumeric():
        print("Bad account id during the insert of the annotation. Value : ", account_id, "Type : ", type(account_id))

    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO account_annotation (account_id, category_id, label_id) VALUES (?, ?, ?) ON CONFLICT (account_id, category_id) DO UPDATE SET label_id=excluded.label_id",
        (account_id, category_id, label_id)
    ).fetchall()
    db_conn.commit()

def delete_account_annotation(db_conn, account_id, category_id):
        
    if not account_id.isnumeric():
        print("Bad account id during the deletion of the annotation. Value : ", account_id, "Type : ", type(account_id))

    # print("Delete the account annotation if it already exist.", "Account id : ", account_id, "Category id : " ,category_id)
    cursor = db_conn.cursor()
    cursor.execute(
        "DELETE FROM account_annotation WHERE account_id = ?  AND  category_id = ?",
        (account_id, category_id)
    ).fetchall()
    db_conn.commit()

def insert_category(db_conn, category_title, category_type):

    if category_type == 'account':
        table_name = 'account_category'
    else:
        table_name = 'post_category'

    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO {table_name} (title) VALUES (?) RETURNING id".format(table_name=table_name),
        ([category_title])
    ).fetchall()
    db_conn.commit()

    results_tmp = db_conn.execute(
        "SELECT id FROM {table_name} WHERE title = ?".format(table_name=table_name), ([category_title])
    ).fetchall()
    category_id = [tuple(row) for row in results_tmp][0][0]
    
    return category_id

def insert_label(db_conn, category_id, sub_category_title, category_type):

    if category_type == 'account':
        table_name = 'account_label'
    else:
        table_name = 'post_label'

    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO {table_name} (category_id, title) VALUES (?, ?)".format(table_name=table_name),
        (category_id, sub_category_title)
    ).fetchall()
    db_conn.commit()

    results_tmp = db_conn.execute(
        "SELECT id FROM {table_name} WHERE title = ? AND category_id = ?".format(table_name=table_name), (sub_category_title, category_id)
    ).fetchall()
    label_id = [tuple(row) for row in results_tmp][0][0]

    return label_id

def update_post_actually_missing_count(db_conn, posts_occurence_by_account, account_df):
    
    for account_name, post_really_collected in zip(posts_occurence_by_account.index, posts_occurence_by_account):

        post_asked = account_df.loc[account_df['account'] == account_name]['postsAsked'].values[0]
        post_missing = int(post_asked) - int(post_really_collected)
        # print('post count :', post_count)
        # print('post actually count :', post_really_collected)
        # print('post missing count :', post_missing)

        account = db_conn.execute(
            "UPDATE account SET postsReallyCollected = ?, postsMissing = ? WHERE account = ?", (post_really_collected, post_missing, account_name)
        ).fetchall()
        db_conn.commit()

    return 'ok'

# Get all columns and remove timestampApify from the list because the timezone +00:00 is stuck with pandas due to colon
def get_columns_name(db_conn, column_name_to_exclude=['timestampApify']):

    columns =  pd.read_sql_query("SELECT name FROM pragma_table_info('post')", db_conn)
    columns_list = columns['name'].to_list()
    cleaned_column_list = []
    for column in columns_list:
        if column not in column_name_to_exclude:
            cleaned_column_list.append(f'post.\'{column}\'')

    cleaned_columns = ','.join(cleaned_column_list)

    return cleaned_columns