"""Gestion des "routes" FLASK et des données pour les couleurs.
Fichier : gestion_couleur_crud.py
Auteur : OM 2022.04.11
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.couleur.gestion_couleur_wtf_forms import FormWTFAddCouleur
from APP_FILMS_164.couleur.gestion_couleur_wtf_forms import FormWTFDeleteCouleur
from APP_FILMS_164.couleur.gestion_couleur_wtf_forms import FormWTFUpdateCouleur

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
                    strsql_stock_afficher = """select * from t_stock ORDER BY id_stock ASC"""

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
                    flash(f"Voici la liste des stocks.", "success")

        except Exception as Exception_stock_afficher:
            raise ExceptionStockAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{stock_afficher.__name__} ; "
                                          f"{Exception_stock_afficher}")
    return render_template("stock/stock_afficher.html", data=data_stock)

@app.route("/stock_add", methods=['GET', 'POST'])
def stock_add_wtf():
    form_add_stock = FormWTFAddStock()
    if request.method == "POST":
        try:
            if form_add_stock.validate_on_submit():
                nom_stock_add = form_add_stock.nom_stock_add_wtf.data

                valeurs_insertion_dictionnaire = {"value_nom_stock": nom_stock_add}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_stock = """INSERT INTO t_stock (id_stock,lieuStock) VALUES (NULL,%(value_nom_couleur)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_stock, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau film (id_film_sel=0 => afficher tous les films)
                return redirect(url_for('stock_genres_afficher', id_stock_sel=0))

        except Exception as Exception_stock_ajouter_wtf:
            raise ExceptionStockAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{stock_add_wtf.__name__} ; "
                                            f"{Exception_stock_ajouter_wtf}")

    return render_template("stock/stock_add_wtf.html", form_add_stock=form_add_stock)


"""Editer(update) un film qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_update

Test : exemple: cliquer sur le menu "Films/produits" puis cliquer sur le bouton "EDIT" d'un "film"

Paramètres : sans

But : Editer(update) un produit qui a été sélectionné dans le formulaire "produits_afficher.html"

Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""


@app.route("/stock_update", methods=['GET', 'POST'])
def stock_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_film"
    id_stock_update = request.values['id_stock_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_stock = FormWTFUpdateStock()
    try:
        print(" on submit ", form_update_stock.validate_on_submit())
        if form_update_stock.validate_on_submit():
            # Récupèrer la valeur du champ depuis "produit_update_wtf.html" après avoir cliqué sur "SUBMIT".
            nom_stock_update = form_update_stock.nom_stock_update_wtf.data

            valeur_update_dictionnaire = {"value_id_stock": id_stock_update,
                                          "value_nom_stock": nom_stock_update,
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_stock = """UPDATE t_stock SET lieuStock = %(value_nom_couleur)s,"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_stock, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le film modifié, "ASC" et l'"id_film_update"
            return redirect(url_for('stock_afficher', id_stock_sel=id_stock_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_film" et "intitule_produit" de la "t_genre"
            str_sql_id_stock = "SELECT * FROM t_stock WHERE id_stock = %(value_id_stock)s"
            valeur_select_dictionnaire = {"value_id_stock": id_stock_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_stock, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom produit" pour l'UPDATE
            data_stock = mybd_conn.fetchone()
            print("data_stock ", data_stock, " type ", type(data_stock), " stock ",
                  data_stock["nom_stock"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "film_update_wtf.html"
            form_update_stock.nom_stock_update_wtf.data = data_stock["nom_stock"]

    except Exception as Exception_stock_update_wtf:
        raise ExceptionStockUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{stock_update_wtf.__name__} ; "
                                     f"{Exception_stock_update_wtf}")

    return render_template("stock/stock_update_wtf.html", form_update_stock=form_update_stock)


"""Effacer(delete) un film qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_delete
    
Test : ex. cliquer sur le menu "film" puis cliquer sur le bouton "DELETE" d'un "film"
    
Paramètres : sans

Remarque :  Dans le champ "nom_film_delete_wtf" du formulaire "films/film_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/stock_delete", methods=['GET', 'POST'])
def stock_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_stock_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_film"
    id_stock_delete = request.values['id_stock_btn_delete_html']

    # Objet formulaire pour effacer le film sélectionné.
    form_delete_stock = FormWTFDeleteStock()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_stock.submit_btn_annuler.data:
            return redirect(url_for("stock_afficher", id_stock_sel=0))

        if form_delete_stock.submit_btn_conf_del_stock.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_stock_delete = session['data_stock_delete']
            print("data_stock_delete ", data_stock_delete)

            flash(f"Effacer le stock de façon définitif de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer produit" qui va irrémédiablement EFFACER le produit
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_stock.submit_btn_del_stock.data:
            valeur_delete_dictionnaire = {"value_id_stock": id_stock_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_stock = """DELETE FROM t_stock WHERE id_stock = %(value_id_stock)s"""
            # Manière brutale d'effacer d'abord la "fk_film", même si elle n'existe pas dans la "t_produit_film"
            # Ensuite on peut effacer le film vu qu'il n'est plus "lié" (INNODB) dans la "t_produit_film"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_stock, valeur_delete_dictionnaire)

            flash(f"Stock définitivement effacé !!", "success")
            print(f"Stock définitivement effacé !!")

            # afficher les données
            return redirect(url_for('stock_afficher', id_stock_sel=0))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_stock": id_stock_delete}
            print(id_stock_delete, type(id_stock_delete))

            # Requête qui affiche le film qui doit être efffacé.
            str_sql_stock_delete = """SELECT * FROM t_stock WHERE id_stock = %(value_id_stock)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_stock_delete, valeur_select_dictionnaire)
                data_stock_delete = mydb_conn.fetchall()
                print("data_stock_delete...", data_stock_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_stock_delete'] = data_stock_delete

            # Le bouton pour l'action "DELETE" dans le form. "film_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_stock_delete_wtf:
        raise ExceptionStockDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{stock_delete_wtf.__name__} ; "
                                     f"{Exception_stock_delete_wtf}")

    return render_template("stock/stock_delete_wtf.html",
                           form_delete_stock=form_delete_stock,
                           btn_submit_del=btn_submit_del,
                           data_stock_del=data_stock_delete
                           )
