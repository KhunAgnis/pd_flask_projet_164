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
from APP_FILMS_164.couleur.gestion_couleur_wtf_forms import FormWTFAjouterCouleur
from APP_FILMS_164.couleur.gestion_couleur_wtf_forms import FormWTFDeleteCouleur
from APP_FILMS_164.couleur.gestion_couleur_wtf_forms import FormWTFUpdateCouleur



"""Ajouter un film grâce au formulaire "couleur_add_wtf.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_add

Test : exemple: cliquer sur le menu "Films/couleurs" puis cliquer sur le bouton "ADD" d'un "film"

Paramètres : sans


Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""

@app.route("/couleur_afficher/<string:order_by>/<int:id_couleur_sel>", methods=['GET', 'POST'])
def couleur_afficher(order_by, id_couleur_sel):
    data_couleur = []  # Initialiser la variable data_couleur à une liste vide

    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_couleur_sel == 0:
                    strsql_couleur_afficher = """select * from t_couleur ORDER BY id_couleur ASC"""
                    mc_afficher.execute(strsql_couleur_afficher)
                elif order_by == "ASC":
                    valeur_id_couleur_selected_dictionnaire = {"value_id_couleur_selected": id_couleur_sel}
                    strsql_couleur_afficher = """SELECT * FROM t_couleur WHERE id_couleur = %(value_id_couleur_selected)s """
                    mc_afficher.execute(strsql_couleur_afficher, valeur_id_couleur_selected_dictionnaire)

                else:
                    strsql_couleur_afficher = """SELECT * FROM t_couleur ORDER BY id_couleur DESC"""
                    mc_afficher.execute(strsql_couleur_afficher)

                data_couleur = mc_afficher.fetchall()
                print("data_couleur ", data_couleur, " Type : ", type(data_couleur))

                if not data_couleur and id_couleur_sel == 0:
                    flash("""La table "t_couleur" est vide. !!""", "warning")
                elif not data_couleur and id_couleur_sel > 0:
                    flash(f"La couleur demandée n'existe pas !!", "warning")
                else:
                    flash(f"Voici la liste des couleurs.", "success")

        except Exception as Exception_couleur_afficher:
            raise ExceptionCouleurAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{couleur_afficher.__name__} ; "
                                          f"{Exception_couleur_afficher}")
    return render_template("couleur/couleur_afficher.html", data=data_couleur)

@app.route("/couleur_ajouter", methods=['GET', 'POST'])
def couleur_ajouter_wtf():
    form = FormWTFAjouterCouleur()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_couleur_ajouter = form.nom_couleur_wtf.data

                valeurs_insertion_dictionnaire = {
                    "value_nom_couleur": nom_couleur_ajouter
                }

                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_couleur = """INSERT INTO t_couleur (couleur) VALUES (%(value_nom_couleur)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_couleur, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                return redirect(url_for('couleur_afficher', order_by='DESC', id_couleur_sel=0))

        except Exception as Exception_couleur_ajouter_wtf:
            raise ExceptionCouleurAjouterWTF(f"fichier : {Path(__file__).name}  ;  "
                                            f"{couleur_ajouter_wtf.__name__} ; "
                                            f"{Exception_couleur_ajouter_wtf}")

    return render_template("couleur/couleur_ajouter_wtf.html", form=form)


"""Editer(update) un film qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_update

Test : exemple: cliquer sur le menu "Films/couleurs" puis cliquer sur le bouton "EDIT" d'un "film"

Paramètres : sans

But : Editer(update) un couleur qui a été sélectionné dans le formulaire "couleurs_afficher.html"

Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""


@app.route("/couleur_update", methods=['GET', 'POST'])
def couleur_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_couleur"
    id_couleur_update = request.values['id_couleur_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateCouleur()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "couleur_update_wtf.html" après avoir cliqué sur "SUBMIT".
            nom_couleur_update = form_update.nom_couleur_update_wtf.data

            valeur_update_dictionnaire = {"value_id_couleur": id_couleur_update, "value_nom_couleur": nom_couleur_update}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_couleur = """
                UPDATE t_couleur
                SET couleur = %(value_nom_couleur)s
                WHERE id_couleur = %(value_id_couleur)s
            """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_couleur, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement la couleur modifiée, "ASC" et l'"id_couleur_update"
            return redirect(url_for('couleur_afficher', order_by="ASC", id_couleur_sel=id_couleur_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_couleur" et "couleur" de la "t_couleur"
            str_sql_id_couleur = "SELECT * FROM t_couleur WHERE id_couleur = %(value_id_couleur)s"
            valeur_select_dictionnaire = {"value_id_couleur": id_couleur_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_couleur, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "couleur" pour l'UPDATE
            data_couleur = mybd_conn.fetchone()
            print("data_couleur ", data_couleur, " type ", type(data_couleur), " couleur ", data_couleur["couleur"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "couleur_update_wtf.html"
            form_update.nom_couleur_update_wtf.data = data_couleur["couleur"]

    except Exception as Exception_couleur_update_wtf:
        raise ExceptionCouleurUpdateWtf(f"fichier : {Path(__file__).name}  ;  {couleur_update_wtf.__name__} ; {Exception_couleur_update_wtf}")

    return render_template("couleur/couleur_update_wtf.html", form_update=form_update)



"""Effacer(delete) un film qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_delete
    
Test : ex. cliquer sur le menu "film" puis cliquer sur le bouton "DELETE" d'un "film"
    
Paramètres : sans

Remarque :  Dans le champ "nom_film_delete_wtf" du formulaire "films/film_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/couleur_delete", methods=['GET', 'POST'])
def couleur_delete_wtf():
    data_films_attribue_couleur_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_couleur"
    id_couleur_delete = request.values['id_couleur_btn_delete_html']

    # Objet formulaire pour effacer le couleur sélectionné.
    form_delete = FormWTFDeleteCouleur()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("couleur_afficher", order_by="ASC", id_couleur_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "couleur/couleur_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_couleur_delete = session['data_films_attribue_couleur_delete']
                print("data_films_attribue_couleur_delete ", data_films_attribue_couleur_delete)

                flash(f"Effacer le couleur de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer couleur" qui va irrémédiablement EFFACER le couleur
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_couleur": id_couleur_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_couleur = """DELETE FROM t_couleur WHERE id_couleur = %(value_id_couleur)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_couleur_film"
                # Ensuite on peut effacer le couleur vu qu'il n'est plus "lié" (INNODB) dans la "t_couleur_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_couleur, valeur_delete_dictionnaire)

                flash(f"couleur définitivement effacé !!", "success")
                print(f"couleur définitivement effacé !!")

                # afficher les données
                return redirect(url_for('couleur_afficher', order_by="ASC", id_couleur_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_couleur": id_couleur_delete}
            print(id_couleur_delete, type(id_couleur_delete))

            # Requête qui affiche tous les films_genres qui ont le couleur que l'utilisateur veut effacer
            str_sql_couleur_delete = """SELECT * FROM t_couleur 
                                            WHERE id_couleur = %(value_id_couleur)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_couleur_delete, valeur_select_dictionnaire)
                data_films_attribue_couleur_delete = mydb_conn.fetchall()
                print("data_films_attribue_couleur_delete...", data_films_attribue_couleur_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "couleur/couleur_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_couleur_delete'] = data_films_attribue_couleur_delete

                # Opération sur la BD pour récupérer "id_couleur" et "intitule_couleur" de la "t_genre"
                str_sql_id_couleur = "SELECT * FROM t_couleur WHERE id_couleur = %(value_id_couleur)s"

                mydb_conn.execute(str_sql_id_couleur, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom couleur" pour l'action DELETE
                data_couleur = mydb_conn.fetchone()
                print("data_couleur", data_couleur, " type ", type(data_couleur), " couleur ", data_couleur)


            # Afficher la valeur sélectionnée dans le champ du formulaire "couleur_delete_wtf.html"
            form_delete.nom_couleur_delete_wtf.data = data_couleur["data_couleur"]

            # Le bouton pour l'action "DELETE" dans le form. "couleur_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_couleur_delete_wtf:
        raise ExceptionCouleurDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{couleur_delete_wtf.__name__} ; "
                                      f"{Exception_couleur_delete_wtf}")

    return render_template("couleur/couleur_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del)
