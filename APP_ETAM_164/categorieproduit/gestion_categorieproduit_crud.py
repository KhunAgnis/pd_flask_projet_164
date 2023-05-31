"""Gestion des "routes" FLASK et des données pour les categorieproduits.
Fichier : gestion_categorieproduit_crud.py
Auteur : OM 2022.04.11
"""
from pathlib import Path


from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_ETAM_164.database.database_tools import DBconnection
from APP_ETAM_164.erreurs.exceptions import *
from APP_ETAM_164.categorieproduit.gestion_categorieproduit_wtf_forms import FormWTFAjouterCategorieProduit
from APP_ETAM_164.categorieproduit.gestion_categorieproduit_wtf_forms import FormWTFUpdateCategorieProduit
from APP_ETAM_164.categorieproduit.gestion_categorieproduit_wtf_forms import FormWTFDeleteCategorieProduit



"""Ajouter un film grâce au formulaire "categorieproduit_add_wtf.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_add

Test : exemple: cliquer sur le menu "Films/produits" puis cliquer sur le bouton "ADD" d'un "film"

Paramètres : sans


Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""

@app.route("/categorieproduit_afficher/<string:order_by>/<int:id_categorie_sel>", methods=['GET', 'POST'])
def categorieproduit_afficher(order_by, id_categorie_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_categorie_sel == 0:
                    strsql_categorieproduit_afficher = """select * from t_categorieproduit 
                                                          ORDER BY id_categorie ASC"""

                    mc_afficher.execute(strsql_categorieproduit_afficher)
                elif order_by == "ASC":
                    valeur_id_categorie_selected_dictionnaire = {"value_id_categorie_selected": id_categorie_sel}
                    strsql_categorieproduit_afficher = """SELECT * FROM t_categorieproduit WHERE id_categorie = %(
                    value_id_categorie_selected)s """

                    mc_afficher.execute(strsql_categorieproduit_afficher, valeur_id_categorie_selected_dictionnaire)
                else:
                    strsql_categorieproduit_afficher = """SELECT * FROM t_categorieproduit ORDER BY id_categorie DESC"""

                    mc_afficher.execute(strsql_categorieproduit_afficher)

                data_categorieproduit = mc_afficher.fetchall()
                print("data_categorieproduit ", data_categorieproduit, " Type : ", type(data_categorieproduit))

                print("data_categorieproduit ", data_categorieproduit, " Type : ", type(data_categorieproduit))
                if not data_categorieproduit and id_categorie_sel == 0:
                    flash("""La table "t_categorieproduit" est vide. !!""", "warning")
                elif not data_categorieproduit and id_categorie_sel > 0:
                    flash(f"La catégorie demandée n'existe pas !!", "warning")
                else:
                    flash(f"Voici la liste des catégories et de leur description.", "success")

        except Exception as Exception_categorieproduit_afficher:
            raise ExceptionCategorieProduitAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{categorieproduit_afficher.__name__} ; "
                                          f"{Exception_categorieproduit_afficher}")

    return render_template("categorieproduit/categorieproduit_afficher.html", data=data_categorieproduit)


@app.route("/categorieproduit_ajouter", methods=['GET', 'POST'])
def categorieproduit_ajouter_wtf():
    # Objet formulaire pour AJOUTER un film
    form = FormWTFAjouterCategorieProduit()

    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_categorieproduit_ajouter = form.nom_categorieproduit_ajouter_wtf.data
                desc_categorieproduit_ajouter = form.desc_categorieproduit_ajouter_wtf.data
                images_categorieproduit_ajouter = form.images_categorieproduit_ajouter_wtf.data

                valeurs_insertion_dictionnaire = {"value_nom_categorieproduit": nom_categorieproduit_ajouter}
                valeurs_insertion_dictionnaire = {"value_desc_categorieproduit": desc_categorieproduit_ajouter}
                valeurs_insertion_dictionnaire = {"value_images_categorieproduit": images_categorieproduit_ajouter}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_categorieproduit = """INSERT INTO t_categorieproduit
                                                    (id_categorie,nomCategorie, descCategorie, imagesCategorie) 
                                                    VALUES (NULL,%(value_nom_categorieproduit), %(value_desc_categorieproduit),
                                                    %(value_images_categorieproduit)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_categorieproduit, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau film (id_film_sel=0 => afficher tous les films)
                return redirect(url_for('ajouter_categorieproduit', order_by='DESC', id_categorie_sel=0))


        except Exception as Exception_categorieproduit_ajouter_wtf:
            raise ExceptionCategorieProduitAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                             f"{categorieproduit_ajouter_wtf.__name__} ; "
                                             f"{Exception_categorieproduit_ajouter_wtf}")

    return render_template("categorieproduit/categorieproduit_ajouter_wtf.html", form=form)


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


@app.route("/categorieproduit_update", methods=['GET', 'POST'])
def categorieproduit_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_film"
    id_categorie_update = request.values['id_categorie_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateCategorieProduit()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupérer la valeur du champ depuis "categorieproduit_update_wtf.html" après avoir cliqué sur "SUBMIT".
            nom_categorieproduit_update = form_update.nom_categorieproduit_update.data
            desc_categorieproduit_update = form_update.desc_categorieproduit_update.data
            images_categorieproduit_update = form_update.images_categorieproduit_update.data

            valeurs_update_dictionnaire = {
                "value_nom_categorieproduit": nom_categorieproduit_update,
                "value_desc_categorieproduit": desc_categorieproduit_update,
                "value_images_categorieproduit": images_categorieproduit_update,
                "value_id_categorieproduit": id_categorie_update
            }

            print("valeurs_update_dictionnaire ", valeurs_update_dictionnaire)

            str_sql_update_nom_categorieproduit = """
                UPDATE t_categorieproduit
                SET nomCategorie = %(value_nom_categorieproduit)s,
                    descCategorie = %(value_desc_categorieproduit)s,
                    imagesCategorie = %(value_images_categorieproduit)s
                WHERE id_Categorie = %(value_id_categorieproduit)s
            """

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_categorieproduit, valeurs_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le film modifié, "ASC" et l'"id_film_update"
            return redirect(url_for('categorieproduit_update_wtf', id_categorie_sel=id_categorie_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_film" et "intitule_produit" de la "t_genre"
            str_sql_id_categorie = "SELECT * FROM t_categorieproduit WHERE id_categorie = %(value_id_categorie)s"
            valeur_select_dictionnaire = {"value_id_categorie": id_categorie_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_categorie, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom produit" pour l'UPDATE
            data_nom_categorieproduit = mybd_conn.fetchone()
            print("data_nom_produits ", data_nom_categorieproduit, " type ", type(data_nom_categorieproduit), " nomCategorie ",
                  data_nom_categorieproduit["nomCategorie"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "categorieproduit_update_wtf.html"
            form_update.nom_categorieproduit_update.data = data_nom_categorieproduit["nomCategorie"]
            form_update.desc_categorieproduit_update.data = data_nom_categorieproduit["descCategorie"]
            form_update.images_categorieproduit_update.data = data_nom_categorieproduit["imagesCategorie"]

    except Exception as Exception_categorieproduit_update_wtf:
        raise ExceptionCategorieProduitUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                        f"{categorieproduit_update_wtf.__name__} ; "
                                        f"{Exception_categorieproduit_update_wtf}")

    return render_template("categorieproduit/categorieproduit_update_wtf.html", form_update=form_update)




"""Effacer(delete) un film qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_delete

Test : ex. cliquer sur le menu "film" puis cliquer sur le bouton "DELETE" d'un "film"

Paramètres : sans

Remarque :  Dans le champ "nom_film_delete_wtf" du formulaire "films/film_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/categorieproduit_delete", methods=['GET', 'POST'])
def categorieproduit_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_categorieproduit_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_film"
    id_categorie_delete = request.values['id_categorie_btn_delete_html']

    # Objet formulaire pour effacer le film sélectionné.
    form_delete_categorieproduit = FormWTFDeleteCategorieProduit()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_categorieproduit.submit_btn_annuler.data:
            return redirect(url_for("categorieproduit_afficher", id_categorie_sel=0))

        if form_delete_categorieproduit.submit_btn_conf_del_categorieproduit.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_categorieproduit_delete = session['data_categorieproduit_delete']
            print("data_categorieproduit_delete ", data_categorieproduit_delete)

            flash(f"Effacer la categorieproduit de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer produit" qui va irrémédiablement EFFACER le produit
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_categorieproduit.submit_btn_del_categorieproduit.data:
            valeur_delete_dictionnaire = {"value_id_categorie": id_categorie_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_categorieproduit = """DELETE FROM t_categorieproduit WHERE id_categorie = %(value_id_categorie)s"""
            # Manière brutale d'effacer d'abord la "fk_film", même si elle n'existe pas dans la "t_produit_film"
            # Ensuite on peut effacer le film vu qu'il n'est plus "lié" (INNODB) dans la "t_produit_film"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_categorieproduit, valeur_delete_dictionnaire)

            flash(f"categorieproduit définitivement effacée !!", "success")
            print(f"categorieproduit définitivement effacée !!")

            # afficher les données
            return redirect(url_for('categorieproduit_afficher', id_categorie_sel=0))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_categorie": id_categorie_delete}
            print(id_categorie_delete, type(id_categorie_delete))

            # Requête qui affiche le film qui doit être efffacé.
            str_sql_produits_categorieproduit_delete = """SELECT * FROM t_categorieproduit WHERE id_categorie = %(value_id_categorie)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_produits_categorieproduit_delete, valeur_select_dictionnaire)
                data_categorieproduit_delete = mydb_conn.fetchall()
                print("data_categorieproduit_delete...", data_categorieproduit_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_categorieproduit_delete'] = data_categorieproduit_delete

            # Le bouton pour l'action "DELETE" dans le form. "film_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_categorieproduit_delete_wtf:
        raise ExceptionCategorieProduitDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                        f"{categorieproduit_delete_wtf.__name__} ; "
                                        f"{Exception_categorieproduit_delete_wtf}")

    return render_template("categorieproduit/categorieproduit_delete_wtf.html",
                           form_delete_categorieproduit=form_delete_categorieproduit,
                           btn_submit_del=btn_submit_del,
                           data_categorieproduit_del=data_categorieproduit_delete
                           )
