"""
    Fichier : gestion_films_genres_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les films et les genres.
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_ETAM_164.database.database_tools import DBconnection
from APP_ETAM_164.erreurs.exceptions import *

"""
    Nom : films_genres_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /films_genres_afficher
    
    But : Afficher les films avec les genres associés pour chaque film.
    
    Paramètres : id_genre_sel = 0 >> tous les films.
                 id_genre_sel = "n" affiche le film dont l'id est "n"
                 
"""


@app.route("/galerie_afficher/<string:order_by>/<int:id_galerie_sel>", methods=['GET', 'POST'])
def galerie_afficher(order_by, id_galerie_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_galerie_sel == 0:
                    strsql_galerie_afficher = """select * from t_categorieproduit 
                                                          ORDER BY id_categorie ASC"""

                    mc_afficher.execute(strsql_galerie_afficher)
                elif order_by == "ASC":
                    valeur_id_categorie_selected_dictionnaire = {"value_id_categorie_selected": id_galerie_sel}
                    strsql_galerie_afficher = """SELECT * FROM t_categorieproduit WHERE id_categorie = %(
                    value_id_galerie_selected)s """

                    mc_afficher.execute(strsql_galerie_afficher, valeur_id_categorie_selected_dictionnaire)
                else:
                    strsql_galerie_afficher = """SELECT * FROM t_categorieproduit ORDER BY id_categorie DESC"""

                    mc_afficher.execute(strsql_galerie_afficher)

                data_categorieproduit = mc_afficher.fetchall()
                print("data_categorieproduit ", data_categorieproduit, " Type : ", type(data_categorieproduit))

                print("data_categorieproduit ", data_categorieproduit, " Type : ", type(data_categorieproduit))
                if not data_categorieproduit and id_galerie_sel == 0:
                    flash("""La table "t_categorieproduit" est vide. !!""", "warning")
                elif not data_categorieproduit and id_galerie_sel > 0:
                    flash(f"La catégorie demandée n'existe pas !!", "warning")
                else:
                    flash(f"Voici les images relatives aux différentes catégories.", "success")

        except Exception as Exception_galerie_afficher:
            raise ExceptionCategorieProduitAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{galerie_afficher.__name__} ; "
                                          f"{Exception_galerie_afficher}")

    return render_template("galerie/galerie_afficher.html", data=data_categorieproduit)