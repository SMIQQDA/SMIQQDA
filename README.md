# Insta-picky
## Security Warning
This program is intended to be run only locally on your computer. It must not be run on a server exposed on internet ! They are some features useful in locally but dangerous if exposed on internet.

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

For a detailed guide to the operation and features of SMIQQDA, please refer to the "Vademecum SMIQQDA” document included with the software (directory: Documentation).

## Licence

To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
