###############################################################################
# To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
# Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
# SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
# The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
# Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
###############################################################################

from .db import db
from .db import db_utils # Required to avoid import error
from .route import account, annotation, category, export, free_annotation, post, xml
from flask import Flask
from flask import render_template
from flask import send_from_directory

import mimetypes
import os

def create_app(test_config=None):

    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('text/css', '.css')

    app = Flask(__name__, static_url_path="/static")
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.get("/")
    def index():
        return render_template("index.html")
    
    @app.get("/account")
    def accountPage():
        return render_template("account.html")
    
    @app.get("/edit_category_account")
    def editAccountCategory():
        return render_template("edit_category_account.html")
    
    @app.get("/edit_category_post")
    def editPostCategory():
        return render_template("edit_category_post.html")
    
    @app.get("/export_post")
    def exportPost():
        return render_template("export_post.html")
    
    @app.get("/export_account")
    def exportAccount():
        return render_template("export_account.html")

    @app.get('/favicon.ico')
    def favicon():
        account.getAccount
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

    # Return an array with the account names (i.e. all directory names)
    @app.get("/api/accounts")
    def getAccountList():
        return account.getAccountList()
    
    # Return an array with the account names (i.e. all directory names)
    @app.get("/api/accounts/<username>")
    def getAccount(username: str):
        return account.getAccount(username)

    # Return an array with the post ids
    @app.get("/api/accounts/<username>/posts")
    def getPostList(username: str):
        return post.getPostList(username)

    # Return an array with the post ids
    @app.get("/api/count/posts")
    def getPostCount():
        return post.getPostCount()   

    # Return the content of the DB
    @app.get("/api/accounts/<username>/posts/<post_id>")
    def getPost(username: str, post_id: str):
        return post.getPost(username, post_id)
    
    # Store a post in the database
    # Used only for debug
    @app.post("/api/accounts/<username>/posts/<post_name>/create")
    def postPost(username: str, post_name: str):
        return post.postPost(username, post_name)
    
    # Return the list of category from the database
    @app.get("/api/categories/<category_type>")
    def getCategories(category_type: str):
        return category.getCategories(category_type)
      
    # Add a category
    @app.post("/api/categories/<category_type>/create")
    def postCategory(category_type: str):
        return category.postCategory(category_type)
      
    # Archive a category
    @app.post("/api/categories/<category_type>/<category_id>/archive")
    def archiveCategory(category_type: str, category_id: str):
        return category.archiveCategory(category_type, category_id)
    
    # Unarchive a category
    @app.post("/api/categories/<category_type>/<category_id>/unarchive")
    def unarchiveCategory(category_type: str, category_id: str):
        return category.unarchiveCategory(category_type, category_id)
    
    # Delete the category in the database and return the number of row deleted
    @app.delete("/api/categories/<category_type>/<category_id>")
    def deleteCategory(category_type: str, category_id: str):
        return category.deleteCategory(category_type, category_id)
    
    # Add a label
    @app.post("/api/labels/<category_type>/create")
    def postLabel(category_type: str):
        return category.postLabel(category_type)
    
    # Archive a label
    @app.post("/api/labels/<category_type>/<label_id>/archive")
    def archiveLabel(category_type: str, label_id: str):
        return category.archiveLabel(category_type, label_id)
    
    # Unarchive a label
    @app.post("/api/labels/<category_type>/<label_id>/unarchive")
    def unarchiveLabel(category_type: str, label_id: str):
        return category.unarchiveLabel(category_type, label_id)
    
    # Delete the label in the database and return the number of row deleted
    @app.delete("/api/labels/<category_type>/<label_id>")
    def deleteLabel(category_type: str, label_id: str):
        return category.deleteLabel(category_type, label_id)

    # Return the list of annotations from the database for one post
    @app.get("/api/annotations")
    def getAnnotations():
        return annotation.getAnnotations()
    
    # Store the annotation in the database and return the id of the annotation
    @app.post("/api/annotations/create")
    def postAnnotations():
        return annotation.postAnnotations()
    
    # Delete the annotation in the database and return the number of row deleted
    @app.delete("/api/annotations/<post_id>/<category_id>")
    def deleteAnnotations(post_id: str, category_id: str):
        return annotation.deleteAnnotations(post_id, category_id)

    # Return the list of annotations from the database for one post
    @app.get("/api/account_annotations")
    def getAccountAnnotations():
        return annotation.getAccountAnnotations()
    
    # Store the annotation in the database and return the id of the annotation
    @app.post("/api/account_annotations/create")
    def postAccountAnnotations():
        return annotation.postAccountAnnotations()
    
    # Delete the annotation in the database and return the number of row deleted
    @app.delete("/api/account_annotations/<account_id>/<category_id>")
    def deleteAccountAnnotations(account_id:str, category_id: str):
        return annotation.deleteAccountAnnotations(account_id, category_id)

    # Return the list of annotations from the database for one post
    @app.get("/api/free_annotations")
    def getFreeAnnotations():
        return free_annotation.getFreeAnnotations()

    # Store the annotation in the database and return the id of the annotation
    @app.post("/api/free_annotations/create")
    def postFreeAnnotations():
        return free_annotation.postFreeAnnotations()

    # Return the list of annotations from the database for one account
    @app.get("/api/free_account_annotations")
    def getFreeAccountAnnotations():
        return free_annotation.getFreeAccountAnnotations()
    
    # Store the annotation in the database and return the id of the annotation
    @app.post("/api/free_account_annotations/create")
    def postFreeAccountAnnotations():
        return free_annotation.postFreeAccountAnnotations()

    # Read xml file
    @app.get("/api/xml")
    def getXML():
        return xml.getXML()
    
    @app.post("/api/export/excel/post")
    def postExportExcelPost():
        return export.postExportExcelPost()
    
    @app.post("/api/export/excel/account")
    def postExportExcelAccount():
        return export.postExportExcelAccount()

    return app