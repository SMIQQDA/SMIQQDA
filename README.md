README.MD            

****************************
TOOLBOX/SOFTWARE SMIQQDA
****************************

SMIQQDA (Social Media Interface for Quantitative and Qualitative Data Analysis) is a free, open-source research software for analyzing text-image digital corpora. It supports synthesis, exploration, and annotation while integrating with quantitative text and visual analysis tools, enhancing the methodological toolkit of media, digital, and visual studies. SMIQQDA adapts to diverse multimodal data, including social media posts, news articles, posters, comics, illustrated books, etc.. The software enables database creation (associate, structure, synthesize, and connect data and tools), data editing (clean, update, correct, verify), exploration (display, search, sort, filter), and advanced analysis through free annotation and categorization (content analysis).
For a detailed guide to the operation and features of SMIQQDA, please refer to the "Vademecum SMIQQDA” document included with the software (directory: Documentation).


Author: Tiago Joseph (tiago.joseph@UGent.be / tiago.joseph@hotmail.com)
Promoter: Catherine Bouko (catherine.bouko@UGent.be)
Programmer: Michaël Stappers
Website: https://research.flw.ugent.be/nl/tiago.joseph
Version: SMIQQDA 1.0

Download	https://doi.org/10.5281/zenodo.15642544 / https://github.com/SMIQQDA/SMIQQDA.git

To quote the software : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
Copyright (c) 2025, Tiago Joseph (Gent University), Michaël Stappers (independent programmer), and Gent University.

-------------------------------------------------------------------------------
0. SECURITY WARNING
----------- 

This program is intended to be run only locally on your computer. It must not be run on a server exposed on internet ! They are some features useful in locally but dangerous if exposed on internet.

1. ABSTRACT
-----------

The manual analysis of image-based social media posts has gained growing scholarly importance, yet suitable analytical tools remain scarce. Our review of 15 years of research (N = 906) reveals a persistent dominance of small-team authorship, which may partly explain the limited development of tools and methodological innovation. Instagram is the most studied platform, while cross-platform analyses remain rare. Content analysis is the predominant method, and few studies employ multiple approaches. Despite its limitations for multimodal and visual content analysis, Excel remains the most widely used software. Against this backdrop of technological limitations, this article introduces SMIQQDA (Social Media Interface for Quantitative and Qualitative Data Analysis), a free and open-source tool designed for multimodal data analysis. SMIQQDA allows users to structure, enrich, and synthesize multimodal datasets within a unified database; visualize, sort, and annotate data; create text-image sub-corpora; integrate additional quantitative tools; and synthesize analytical results. (Tiago JOSEPH & Catherine BOUKO. 2025. SMIQQDA: A free, open-source and free of charge tool for qualitative, quantitative and mixed-method analysis of image-based social media posts. (paper under evaluation)).

2. SOFTWARE DEPENDENCIES
------------------------

•	Python==3.11.6 (https://www.python.org/downloads/release/python-3116/; PSF License; Python Software Foundation) 
•	Flask==2.2.3 (https://pypi.org/project/Flask/2.2.3/; BSD-3-Clause; Pallets Projects)
•	pandas==2.2.2 (https://pypi.org/project/pandas/2.2.2/; BSD-3-Clause; Pandas development team)
•	XlsxWriter==3.1.4 (https://pypi.org/project/XlsxWriter/3.1.4/; BSD-2-Clause; John McNamara)

3. THE FILES YOU SHOULD GET
---------------------------

C:.
├───.gigignore [if downloaded on Github]
├───Licence.txt
├───Readme.md
├───Documentation
│   ├───SMIQQDA_Research software management plan_Presoft Project.docx
│   ├───Vademecum SMIQQDA_FR.docx
│   ├───Vademecum SMIQQDA_FR.pdf
│   ├───Vademecum SMIQQDA_EN.docx
│   ├───Vademecum SMIQQDA_EN.pdf
│   ├───download_postpictures.py
│   ├───download_profilepictures.py
│   ├───ExampleOCRCorpus.xlsx
│   ├───ExamplePostCorpus.xlsx
│   ├───ExampleAccountCorpus.xlsx
│   ├───ExamplePostCorpus.xml
│   └───ExampleCorporaImages
│       ├───comptes [4 subfolders filled with images : ellen.johnson.sirleaf, lindiwesisulusa, phumzilemlambongcuka, rebeccakadagaug]
│       └───profilepictures [filled with the 4 matching profile pictures]
└───insta-picky-main
    ├───flaskr
    │   ├───__init__.py
    │   ├───schema.sql
    │   ├───db
    │   │   ├───db.py
    │   │   ├───db_import.py
    │   │   ├───db_utils.py
    │   │   └───__pycache__ [created during the first launch of SMIQQDA]
    │   │       ├───db.cpython-311.pyc
    │   │       ├───db.cpython-312.pyc
    │   │       ├───db_import.cpython-311.pyc
    │   │       ├───db_import.cpython-312.pyc
    │   │       ├───db_utils.cpython-311.pyc
    │   │       └───db_utils.cpython-312.pyc
    │   ├───export
    │   │   ├───excel
    │   │   │   ├───account
    │   │   │   │   └───.gitkeep
    │   │   │   └───post
    │   │   │       └───.gitkeep
    │   │   └───img
    │   ├───import
    │   │   ├───excel
    │   │   │   ├───account
    │   │   │   │   └───.gitkeep
    │   │   │   ├───ocr
    │   │   │   │   └───.gitkeep
    │   │   │   └───post
    │   │   │       └───.gitkeep
    │   │   └───txm
    │   │       ├───account
    │   │       └───post
    │   ├───route
    │   │   ├───account.py
    │   │   ├───annotation.py
    │   │   ├───category.py
    │   │   ├───export.py
    │   │   ├───free_annotation.py
    │   │   ├───post.py
    │   │   ├───xml.py
    │   │   └───__pycache__ [created during the first launch of SMIQQDA]
    │   │       ├───account.cpython-311.pyc
    │   │       ├───account.cpython-312.pyc
    │   │       ├───annotation.cpython-311.pyc
    │   │       ├───annotation.cpython-312.pyc
    │   │       ├───category.cpython-311.pyc
    │   │       ├───category.cpython-312.pyc
    │   │       ├───export.cpython-311.pyc
    │   │       ├───export.cpython-312.pyc
    │   │       ├───free_annotation.cpython-311.pyc
    │   │       ├───free_annotation.cpython-312.pyc
    │   │       ├───post.cpython-311.pyc
    │   │       ├───post.cpython-312.pyc
    │   │       ├───xml.cpython-311.pyc
    │   │       └───xml.cpython-312.pyc
    │   ├───static
    │   │   ├───favicon.ico
    │   │   ├───css
    │   │   │   ├───account.css
    │   │   │   ├───edit_category.css
    │   │   │   └───main.css
    │   │   ├───insta
    │   │   │   ├───comptes
    │   │   │       └───.gigignore [if downloaded on Github]
    │   │   │   └───profilepictures
    │   │   │       └───.gigignore [if downloaded on Github]
    │   │   └───js
    │   │       ├───edit_category.js
    │   │       └───main.js
    │   ├───templates
    │   │   ├───account.html
    │   │   ├───edit_category_account.html
    │   │   ├───edit_category_post.html
    │   │   ├───export_account.html
    │   │   ├───export_post.html
    │   │   └───index.html
    │   └───__pycache__ [created during the first launch of SMIQQDA]
    │       ├───__init__.cpython-311.pyc
    │       └───__init__.cpython-312.pyc
    └───instance
        └───.gitkeep

4. GETTING STARTED
------------------

For a detailed guide to the operation and features of SMIQQDA, please refer to the "Vademecum SMIQQDA” document included with the software (directory: Documentation).
Example files are also supplied with the software (directory : Documentation).

## Installation

In you terminal, run the following command :
```bash
python -m pip install Flask
python -m pip install pandas
python -m pip install XlsxWriter
python -m flask --app flaskr init-db
```

## Run

To launch the app, run the following command:
```bash
python -m flask --app flaskr run
```
Open your browser to the address : http://localhost:5000/

To update the path to the files for the import, update the value of the variable `PATH_EXCEL` or `PATH_TXM` in the file `db.py`

To import excel account, run the following command:
```bash
python -m flask --app flaskr import-excel-account-in-db
```

To import excel post, run the following command:
```bash
python -m flask --app flaskr import-excel-post-in-db
```

To import txm annotation for account, run the following command:
```bash
python -m flask --app flaskr import-txm-account-in-db
```

To import txm annotation for post, run the following command:
```bash
python -m flask --app flaskr import-txm-post-in-db
```

To export account, go to the url http://localhost:5000/export_account and select your criteria and then click on the button "SQL"
To export post, go to the url http://localhost:5000/export_post and select your criteria and then click on the button "SQL"

The database is stored in the file instance/flaskr.sqlite then you can copy this file somewhere to make a backup. Replace the file with your copy to restore the backup.


5. KNOWN LIMITATIONS/BUGS
-------------------------

Bugs:
-	In date mode, selecting a date not available in the data causes the software to bug. It is necessary to return to a date available in the data. 

Limitations and directions for future versions:
-	Integrating an OCR editing interface. This interface would allow for the direct comparison and correction of images and their OCR results. This feature is especially important for corpora in which the images contain the main textual content of the publications, rather than just captions.
-	Integrating more multimodal formats (e.g., audio, audiovisual). This would allow for a more comprehensive analysis of the mentioned social media platforms, as well as the study of other platforms or corpus types (e.g., TikTok, Netflix, podcasts, etc.);
-	Expanding import and export formats and possibilities to better integrate with other tools (.png, .csv, .xml, TEI tags for automated annotations in Iramuteq, etc.);
-	Developing additional annotation features (e.g., tags, ie. annotations localized on images);
-	Enhancing the design to make it more aesthetically pleasing and user-friendly (e.g., creating bash scripts for SMIQQDA installation, database creation, imports, and launching the software);
-	Expanding image naming possibilities and thus facilitate the articulation of visual and textual data ;
-	Translating the documentation and interface of SMIQQDA into other languages to promote its dissemination and accessibility.

6. CHANGE LOG
-------------

Not applicable.

6. OPEN SOURCE LICENCE - GNU General Public License LICENCE [version 3 or any later version]
----------------------------------------------------------------

Copyright (c) 2025, Tiago Joseph (Gent University), Michaël Stappers (independent programmer), and Gent University.

GNU General Public License LICENCE [version 3 or any later version]. The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html


7. CONTACTING THE AUTHOR(s)
---------------------------

We would very much appreciate hearing from you if you use SMIQQDA and find problems, or if you can think of ways it could be improved - and even if you just think it's great. Even if the facility you would like to see appears to be of interest only to you, tell us about it - you'd be
surprised how many ideas in that class have a much wider appeal.

See above for further contact information.

We read and consider all mail we receive, even though we may not have time to reply.


8. ACKNOWLEDGEMENTS
-------------------
We thank Lisa Bueres for her many wise advices on the development of SMIQQDA, and Catherine Bouko for her help in the software funding process and in the software distribution.
