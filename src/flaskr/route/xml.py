###############################################################################
# To quote : Tiago Joseph, Michaël Stappers, Gent University. 2025. SMIQQDA, Social Media Interface for Quantitative and Qualitative Data Analysis. Version 1.0. Zenodo, https://doi.org/10.5281/zenodo.15642544.
# Copyright (c) 2025, Tiago Joseph (Ghent University), Michaël Stappers (independent programmer), and Gent University. 
# SMIQQDA is protected by the GNU General Public License LICENCE [version 3 or any later version]. 
# The full text of the license is available at the following address: https://www.gnu.org/licenses/gpl-3.0.html
# Contact : tiago.joseph@hotmail.com / tiago.joseph@ugent.be
###############################################################################

import xml.etree.ElementTree as ET

def getXML():
    tree = ET.parse('Essai-TXM-500-posts-chiffres-bien-affichés.xml')
    root = tree.getroot()
    # print(root)
    # print(root.attrib)
    # print(root.tag)
    default_namespace = root.tag[0:root.tag.index('}')+1]
    txm_namespace = "{http://textometrie.org/1.0}"
    # print("namespace : ", default_namespace)
    posts = root[1][0]
    for post in posts:
        if post.tag == (default_namespace + "post"):
            post_id = post.attrib["number"]
            caption = post[1]
            if caption.tag == (default_namespace + "caption"):
                p = caption[0]
                # print("p :", p.tag, p.attrib)
                for child_p in p:
                    if child_p.tag.startswith(txm_namespace):
                        # print("post :", post_id)
                        category = child_p.tag[txm_namespace.index('}')+1:]
                        # print("Category :", category)
            else:
                # Précaution au cas où le xml aurait changé par rapport à quand ce code a été écrit
                print("Error in parsing, the xml tags are not in the expected order")

    return "ok"