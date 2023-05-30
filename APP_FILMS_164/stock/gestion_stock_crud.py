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

@app.route("/stock_afficher/<string:order_by>/<int:id_stock_sel>", methods=['GET', 'POST'])
def stock_afficher(order_by, id_stock_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_stock_sel == 0:
                    strsql_stock_afficher = """select t_stock.lieuStock, t_stock.quantiteStock, t_produit.nomProduit, t_produit.tailleProduit, t_stock.dernieredateajout
                                               from t_stock 
                                               Inner join t_produit on t_stock.fk_Produit = t_produit.id_Produit
                                               ORDER BY lieuStock ASC"""

                    mc_afficher.execute(strsql_stock_afficher)
                elif order_by == "ASC":
                    valeur_id_stock_selected_dictionnaire = {"value_id_stock_selected": id_stock_sel}
                    strsql_stock_afficher = """SELECT * FROM t_stock WHERE id_stock = %(
                    value_id_stock_selected)s """

                    mc_afficher.execute(strsql_stock_afficher, valeur_id_stock_selected_dictionnaire)
                else:
                    strsql_stock_afficher = """SELECT * FROM t_stock ORDER BY id_stock DESC"""

                    mc_afficher.execute(strsql_stock_afficher)

                data_stock = mc_afficher.fetchall()
                print("data_stock ", data_stock, " Type : ", type(data_stock))

                print("data_stock ", data_stock, " Type : ", type(data_stock))
                if not data_stock and id_stock_sel == 0:
                    flash("""La table "t_stock" est vide. !!""", "warning")
                elif not data_stock and id_stock_sel > 0:
                    flash(f"Le stock demandé n'existe pas !!", "warning")
                else:
                    flash(f"Voici la liste des produits dans les stocks.", "success")

        except Exception as Exception_stock_afficher:
            raise ExceptionStockAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{stock_afficher.__name__} ; "
                                          f"{Exception_stock_afficher}")

    return render_template("stock/stock_afficher.html", data=data_stock)
