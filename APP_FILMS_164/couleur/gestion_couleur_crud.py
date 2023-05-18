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


@app.route("/couleur_add", methods=['GET', 'POST'])
def couleur_add_wtf():
    # Objet formulaire pour AJOUTER un film
    form_add_couleur = FormWTFAddCouleur()
    if request.method == "POST":
        try:
            if form_add_couleur.validate_on_submit():
                nom_couleur_add = form_add_couleur.nom_couleur_add_wtf.data

                valeurs_insertion_dictionnaire = {"value_nom_couleur": nom_couleur_add}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_couleur = """INSERT INTO t_couleur (id_couleur,couleur) VALUES (NULL,%(value_nom_couleur)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_couleur, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau film (id_film_sel=0 => afficher tous les films)
                return redirect(url_for('couleur_genres_afficher', id_film_sel=0))

        except Exception as Exception_produits_ajouter_wtf:
            raise ExceptionCouleurAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{couleur_add_wtf.__name__} ; "
                                            f"{Exception_produits_ajouter_wtf}")

    return render_template("couleur/couleur_add_wtf.html", form_add_film=form_add_couleur)


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


@app.route("/couleur_update", methods=['GET', 'POST'])
def couleur_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_film"
    id_couleur_update = request.values['id_couleur_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_couleur = FormWTFUpdateCouleur()
    try:
        print(" on submit ", form_update_couleur.validate_on_submit())
        if form_update_couleur.validate_on_submit():
            # Récupèrer la valeur du champ depuis "produit_update_wtf.html" après avoir cliqué sur "SUBMIT".
            nom_couleur_update = form_update_couleur.nom_couleur_update_wtf.data

            valeur_update_dictionnaire = {"value_id_couleur": id_couleur_update,
                                          "value_nom_couleur": nom_couleur_update,
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_couleur = """UPDATE t_film SET couleur = %(value_nom_couleur)s,"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_couleur, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le film modifié, "ASC" et l'"id_film_update"
            return redirect(url_for('films_genres_afficher', id_film_sel=id_film_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_film" et "intitule_produit" de la "t_genre"
            str_sql_id_couleur = "SELECT * FROM t_film WHERE id_film = %(value_id_film)s"
            valeur_select_dictionnaire = {"value_id_couleur": id_couleur_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_couleur, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom produit" pour l'UPDATE
            data_film = mybd_conn.fetchone()
            print("data_film ", data_film, " type ", type(data_film), " produit ",
                  data_film["nom_film"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "film_update_wtf.html"
            form_update_couleur.nom_couleur_update_wtf.data = data_film["nom_couleur"]
            # Debug simple pour contrôler la valeur dans la console "run" de PyCharm
            print(f" duree film  ", data_film["duree_film"], "  type ", type(data_film["duree_film"]))

    except Exception as Exception_couleur_update_wtf:
        raise ExceptionCouleurUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{couleur_update_wtf.__name__} ; "
                                     f"{Exception_couleur_update_wtf}")

    return render_template("couleur/couleur_update_wtf.html", form_update_couleur=form_update_couleur)


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
    # Pour afficher ou cacher les boutons "EFFACER"
    data_couleur_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_film"
    id_couleur_delete = request.values['id_couleur_btn_delete_html']

    # Objet formulaire pour effacer le film sélectionné.
    form_delete_couleur = FormWTFDeleteCouleur()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_couleur.submit_btn_annuler.data:
            return redirect(url_for("couleur_afficher", id_couleur_sel=0))

        if form_delete_couleur.submit_btn_conf_del_couleur.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_couleur_delete = session['data_couleur_delete']
            print("data_couleur_delete ", data_couleur_delete)

            flash(f"Effacer la couleur de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer produit" qui va irrémédiablement EFFACER le produit
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_couleur.submit_btn_del_couleur.data:
            valeur_delete_dictionnaire = {"value_id_couleur": id_couleur_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_couleur = """DELETE FROM t_couleur WHERE id_couleur = %(value_id_couleur)s"""
            # Manière brutale d'effacer d'abord la "fk_film", même si elle n'existe pas dans la "t_produit_film"
            # Ensuite on peut effacer le film vu qu'il n'est plus "lié" (INNODB) dans la "t_produit_film"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_couleur, valeur_delete_dictionnaire)

            flash(f"Couleur définitivement effacée !!", "success")
            print(f"Couleur définitivement effacée !!")

            # afficher les données
            return redirect(url_for('couleur_afficher', id_couleur_sel=0))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_couleur": id_couleur_delete}
            print(id_couleur_delete, type(id_couleur_delete))

            # Requête qui affiche le film qui doit être efffacé.
            str_sql_produits_couleur_delete = """SELECT * FROM t_couleur WHERE id_couleur = %(value_id_couleur)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_produits_couleur_delete, valeur_select_dictionnaire)
                data_couleur_delete = mydb_conn.fetchall()
                print("data_couleur_delete...", data_couleur_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_couleur_delete'] = data_couleur_delete

            # Le bouton pour l'action "DELETE" dans le form. "film_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_couleur_delete_wtf:
        raise ExceptionCouleurDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{couleur_delete_wtf.__name__} ; "
                                     f"{Exception_couleur_delete_wtf}")

    return render_template("couleur/couleur_delete_wtf.html",
                           form_delete_couleur=form_delete_couleur,
                           btn_submit_del=btn_submit_del,
                           data_couleur_del=data_couleur_delete
                           )
