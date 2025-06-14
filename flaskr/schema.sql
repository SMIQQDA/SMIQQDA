/*
 * To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
 * Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
 * SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
 * The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
 * Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
*/

PRAGMA foreign_keys = OFF;
DROP TABLE IF EXISTS account_category;
DROP TABLE IF EXISTS post_category;
DROP TABLE IF EXISTS account_label;
DROP TABLE IF EXISTS post_label;
DROP TABLE IF EXISTS annotation;
DROP TABLE IF EXISTS account_annotation;
PRAGMA foreign_keys = ON;

CREATE TABLE account_category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  deleted INTEGER NOT NULL DEFAULT 0,
  UNIQUE (title)
);

CREATE TABLE post_category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  deleted INTEGER NOT NULL DEFAULT 0,
  UNIQUE (title)
);

/*INSERT INTO category (title)
VALUES
  ("a"),
  ("b"),
  ("c"),
  ("d");*/

CREATE TABLE account_label (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  deleted INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (category_id) REFERENCES account_category (id) ON DELETE CASCADE,
  UNIQUE (category_id, title)
);

CREATE TABLE post_label (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  deleted INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (category_id) REFERENCES post_category (id) ON DELETE CASCADE,
  UNIQUE (category_id, title)
);

/*INSERT INTO label (category_id, title)
VALUES
  (1, "petit a"),
  (1, "petit b"),
  (2, "c"),
  (4, "d"),
  (1, "petit e");*/

/*
  Les labels sont mutuellement exclusifs au sein d'une catégorie
  D'où le besoin d'avoir le category_id dans la table pour y appliquer
  une contrainte d'unicité avec le post_id
*/
CREATE TABLE annotation (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
  label_id INTEGER NOT NULL,
  -- FOREIGN KEY (post_id) REFERENCES post (id),
  FOREIGN KEY (label_id) REFERENCES post_label (id) ON DELETE CASCADE,
  FOREIGN KEY (category_id) REFERENCES post_category (id) ON DELETE CASCADE,
  UNIQUE (post_id, category_id)
);

/*
  Les labels sont mutuellement exclusifs au sein d'une catégorie
  D'où le besoin d'avoir le category_id dans la table pour y appliquer
  une contrainte d'unicité avec l'account_id
*/
CREATE TABLE account_annotation (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
  label_id INTEGER NOT NULL,
  -- FOREIGN KEY (account_id) REFERENCES account (id),
  FOREIGN KEY (label_id) REFERENCES account_label (id) ON DELETE CASCADE,
  FOREIGN KEY (category_id) REFERENCES account_category (id) ON DELETE CASCADE,
  UNIQUE (account_id, category_id)
);