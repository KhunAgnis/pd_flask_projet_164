"""Gestion des "routes" FLASK et des données pour les couleurs.
Fichier : gestion_couleur_crud.py
Auteur : OM 2022.04.11
"""
from pathlib import Path


from flask import request


from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *



"""Ajouter un film grâce au formulaire "couleur_add_wtf.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_add

Test : exemple: cliquer sur le menu "Films/produits" puis cliquer sur le bouton "ADD" d'un "film"

Paramètres : sans


Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""

@app.route("/categorieproduit_afficher/<string:order_by>/<int:id_stock_sel>", methods=['GET', 'POST'])
def categorieproduit_afficher(order_by, id_categorie_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_categorie_sel == 0:
                    strsql_categorieproduit_afficher = """select * from t_categorieproduit 
                                                          ORDER BY id_stock ASC"""

                    mc_afficher.execute(strsql_categorieproduit_afficher)
                elif order_by == "ASC":
                    valeur_id_categorieproduit_selected_dictionnaire = {"value_id_categorieproduit_selected": id_categorieproduit_sel}
                    strsql_categorieproduit_afficher = """SELECT * FROM t_categorieproduit WHERE id_categorie = %(
                    value_id_categorie_selected)s """

                    mc_afficher.execute(strsql_categorieproduit_afficher, valeur_id_categorieproduit_selected_dictionnaire)
                else:
                    strsql_categorieproduit_afficher = """SELECT * FROM t_categorieproduit ORDER BY id_categorie DESC"""

                    mc_afficher.execute(strsql_categorieproduit_afficher)

                data_stock = mc_afficher.fetchall()
                print("data_categorie ", data_categorie, " Type : ", type(data_categorie))

                print("data_categorie ", data_categorie, " Type : ", type(data_categorie))
                if not data_categorie and id_categorie_sel == 0:
                    flash("""La table "t_categorieproduit" est vide. !!""", "warning")
                elif not data_categorie and id_categorie_sel > 0:
                    flash(f"La catégorie demandée n'existe pas !!", "warning")
                else:
                    flash(f"Voici la liste des catégories.", "success")

        except Exception as Exception_categorieproduit_afficher:
            raise ExceptionCategorieProduitAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{categorieproduit_afficher.__name__} ; "
                                          f"{Exception_categorieproduit_afficher}")

    return render_template("categorieproduit/categorieproduit_afficher.html", data=data_categorie)
