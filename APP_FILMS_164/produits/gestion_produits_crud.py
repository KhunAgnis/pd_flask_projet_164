"""Gestion des "routes" FLASK et des données pour les produits.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask import render_template


from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.produits.gestion_produits_wtf_forms import FormWTFAjouterProduit
from APP_FILMS_164.produits.gestion_produits_wtf_forms import FormWTFUpdateProduit
from APP_FILMS_164.produits.gestion_produits_wtf_forms import FormWTFDeleteProduit


"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /produits_afficher
    
    Test : ex : http://127.0.0.1:5575/produits_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_produit_sel = 0 >> tous les produits.
                id_produit_sel = "n" affiche le produit dont l'id est "n"
"""


@app.route("/produits_afficher/<string:order_by>/<int:id_produit_sel>", methods=['GET', 'POST'])
def produits_afficher(order_by, id_produit_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_produit_sel == 0:
                    strsql_produits_afficher = """select t_produit.id_Produit,t_produit.nomProduit,t_produit.tailleProduit,t_couleur.couleur,t_categorieproduit.descCategorie
                                                from t_produit
                                                Inner join t_couleur on t_produit.fk_Couleur = t_couleur.id_couleur
                                                Inner join t_categorieproduit on t_produit.fk_Categorie = t_categorieproduit.id_categorie 
                                                ORDER BY id_Produit ASC"""

                    mc_afficher.execute(strsql_produits_afficher)
                elif order_by == "ASC":
                    valeur_id_produit_selected_dictionnaire = {"value_id_Produit_selected": id_produit_sel}
                    strsql_produits_afficher = """SELECT * FROM t_produit WHERE id_Produit = %(
                    value_id_Produit_selected)s """

                    mc_afficher.execute(strsql_produits_afficher, valeur_id_produit_selected_dictionnaire)
                else:
                    strsql_produits_afficher = """SELECT * FROM t_produit ORDER BY id_Produit DESC"""

                    mc_afficher.execute(strsql_produits_afficher)

                data_produits = mc_afficher.fetchall()
                print("data_produits ", data_produits, " Type : ", type(data_produits))

                print("data_produits ", data_produits, " Type : ", type(data_produits))
                if not data_produits and id_produit_sel == 0:
                    flash("""La table "t_produit" est vide. !!""", "warning")
                elif not data_produits and id_produit_sel > 0:
                    flash(f"Le produit demandé n'existe pas !!", "warning")
                else:
                    flash(f"Voici la liste des produits.", "success")

        except Exception as Exception_produits_afficher:
            raise ExceptionProduitsAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{produits_afficher.__name__} ; "
                                          f"{Exception_produits_afficher}")
    return render_template("produits/produits_afficher.html", data=data_produits)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /produits_ajouter
    
    Test : ex : http://127.0.0.1:5575/produits_ajouter
    
    Paramètres : sans
    
    But : Ajouter un produit pour un film
    
    Remarque :  Dans le champ "name_produit_html" du formulaire "produits/produits_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/produits_ajouter", methods=['GET', 'POST'])
def produits_ajouter_wtf():
    form = FormWTFAjouterProduit()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_produits_wtf = form.nom_produits_wtf.data
                taille_produits_wtf = form.taille_produits_wtf.data
                couleur_produits_wtf = form.couleur_produits_wtf.data
                categorie_produits_wtf = form.categorie_produits_wtf.data

                valeurs_insertion_dictionnaire = {
                    "value_nom_produits": nom_produits_wtf,
                    "value_taille_produits": taille_produits_wtf,
                    "value_couleur_produits": couleur_produits_wtf,
                    "value_categorie_produits": categorie_produits_wtf
                }

                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_produits = """
                    INSERT INTO t_produit (id_produit, nomProduit, tailleProduit, fk_couleur, fk_categorie) 
                    VALUES (NULL, %(value_nom_produits)s, %(value_taille_produits)s, 
                            (SELECT couleur FROM t_couleur WHERE id_couleur = %(value_couleur_produits)s), 
                            %(value_categorie_produits)s)
                """

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_produits, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('produits_afficher', order_by='DESC', id_produit_sel=0))



        except Exception as Exception_produits_ajouter_wtf:
            raise ExceptionProduitsAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{produits_ajouter_wtf.__name__} ; "
                                            f"{Exception_produits_ajouter_wtf}")

    # Récupérer les valeurs des couleurs depuis la base de données
    with DBconnection() as mconn_bd:
        mconn_bd.execute("SELECT id_couleur, couleur FROM t_couleur")
        couleurs = mconn_bd.fetchall()

        with DBconnection() as mconn_bd:
            mconn_bd.execute("SELECT id_categorie, descCategorie FROM t_categorieproduit")
            categorieproduits = mconn_bd.fetchall()

    return render_template("produits/produits_ajouter_wtf.html", form=form, couleurs=couleurs, categorieproduits=categorieproduits)



"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /produit_update
    
    Test : ex cliquer sur le menu "produits" puis cliquer sur le bouton "EDIT" d'un "produit"
    
    Paramètres : sans
    
    But : Editer(update) un produit qui a été sélectionné dans le formulaire "produits_afficher.html"
    
    Remarque :  Dans le champ "nom_produit_update_wtf" du formulaire "produits/produit_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/produit_update", methods=['GET', 'POST'])
def produits_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_produit"
    id_produit_update = request.values['id_produit_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateProduit()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "produit_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            nom_produits_update = form_update.nom_produits_update_wtf.data
            taille_produits_essai = form_update.taille_produits_wtf_essai.data
            couleur_produits_update = form_update.couleur_produits_update_wtf.data
            categorie_produits_update = form_update.categorie_produits_update_wtf.data

            valeur_update_dictionnaire = {"value_id_produit": id_produit_update,
                                          "value_tailleProduit_essai": taille_produits_essai,
                                          "value_nomproduit": nom_produits_update,
                                          "couleur_produits_update": couleur_produits_update,
                                          "categorie_produits_update": categorie_produits_update
                                          }

            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_produits = """
                UPDATE t_produit SET tailleProduit = %(value_tailleProduit_essai)s, 
                nomProduits = %(value_nomproduit)s, 
                fk_Couleur = %(couleur_produits_update)s, 
                fk_Categorie = %(categorie_produits_update)s
                WHERE id_Produit = %(value_id_produit)s
            """

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_produits, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_produit_update"
            return redirect(url_for('produits_afficher', order_by="ASC", id_produit_sel=id_produit_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_Produit" et "intitule_produit" de la "t_genre"
            str_sql_id_produit = "SELECT * FROM t_produit " \
                               "WHERE id_produit = %(value_id_produit)s"
            valeur_select_dictionnaire = {"value_id_produit": id_produit_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_produit, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom produit" pour l'UPDATE
            data_nom_produit = mybd_conn.fetchone()
            print("data_nom_produits ", data_nom_produit, " type ", type(data_nom_produit), " produits ",
                  data_nom_produit["tailleProduit"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "produit_update_wtf.html"
            form_update.taille_produits_wtf_essai.data = data_nom_produit["tailleProduit"]
            form_update.nom_produits_update_wtf.data = data_nom_produit["nomProduit"]
            form_update.couleur_produits_update_wtf.data = data_nom_produit["fk_Couleur"]
            form_update.categorie_produits_update_wtf.data = data_nom_produit["fk_Categorie"]

    except Exception as Exception_produit_update_wtf:
        raise ExceptionProduitsUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{produits_update_wtf.__name__} ; "
                                      f"{Exception_produit_update_wtf}")

    return render_template("produits/produits_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /produit_delete
    
    Test : ex. cliquer sur le menu "produits" puis cliquer sur le bouton "DELETE" d'un "produit"
    
    Paramètres : sans
    
    But : Effacer(delete) un produit qui a été sélectionné dans le formulaire "produits_afficher.html"
    
    Remarque :  Dans le champ "nom_produit_delete_wtf" du formulaire "produits/produit_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/produit_delete", methods=['GET', 'POST'])
def produits_delete_wtf():
    data_films_attribue_produit_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_Produit"
    id_produit_delete = request.values['id_produit_btn_delete_html']

    # Objet formulaire pour effacer le produit sélectionné.
    form_delete = FormWTFDeleteProduit()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("produits_afficher", order_by="ASC", id_produit_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "produits/produit_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_produit_delete = session['data_films_attribue_produit_delete']
                print("data_films_attribue_produit_delete ", data_films_attribue_produit_delete)

                flash(f"Effacer le produit de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer produit" qui va irrémédiablement EFFACER le produit
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                nom_produit_delete = form_delete.nom_produit_delete_wtf.data
                taille_produits_delete = form_delete.taille_produits_delete_wtf.data
                couleur_produits_delete = form_delete.couleur_produits_delete_wtf.data
                categorie_produits_delete = form_delete.categorie_produits_delete_wtf.data

                valeur_delete_dictionnaire = {"value_id_produit": id_produit_delete,
                                              "value_tailleProduit_essai": taille_produits_delete,
                                              "value_nomproduit": nom_produit_delete,
                                              "couleur_produits_update": couleur_produits_delete,
                                              "categorie_produits_update": categorie_produits_delete
                                              }

                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_produit = """DELETE FROM t_produit WHERE id_produit = %(value_id_produit)s"""
                str_sql_delete_fk_couleur = """DELETE FROM t_produit WHERE fk_Couleur = %(value_id_couleur)s"""
                str_sql_delete_fk_categorie = """DELETE FROM t_produit WHERE fk_Categorie = %(value_id_categorie)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_produit_film"
                # Ensuite on peut effacer le produit vu qu'il n'est plus "lié" (INNODB) dans la "t_produit_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_produit, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_fk_couleur, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_fk_categorie, valeur_delete_dictionnaire)

                flash(f"Produit définitivement effacé !!", "success")
                print(f"Produit définitivement effacé !!")

                # afficher les données
                return redirect(url_for('produits_afficher', order_by="ASC", id_produit_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_produit": id_produit_delete}
            print(id_produit_delete, type(id_produit_delete))

            # Requête qui affiche tous les films_genres qui ont le produit que l'utilisateur veut effacer
            str_sql_produits_delete = """SELECT * FROM t_produit 
                                            WHERE id_produit = %(value_id_produit)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_produits_delete, valeur_select_dictionnaire)
                data_films_attribue_produit_delete = mydb_conn.fetchall()
                print("data_films_attribue_produit_delete...", data_films_attribue_produit_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "produits/produit_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_produit_delete'] = data_films_attribue_produit_delete

                # Opération sur la BD pour récupérer "id_Produit" et "intitule_produit" de la "t_genre"
                str_sql_id_produit = "SELECT * FROM t_produit WHERE id_Produit = %(value_id_produit)s"

                mydb_conn.execute(str_sql_id_produit, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom produit" pour l'action DELETE
                data_nom_produit = mydb_conn.fetchone()
                print("data_nom_produit ", data_nom_produit, " type ", type(data_nom_produit), " produit ",
                      data_nom_produit["nomProduit"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "produit_delete_wtf.html"
            form_delete.nom_produit_delete_wtf.data = data_nom_produit["nomProduit"]
            form_delete.taille_produits_delete_wtf.data = data_nom_produit["tailleProduit"]
            form_delete.couleur_produits_delete_wtf.data = data_nom_produit["fk_Couleur"]
            form_delete.categorie_produits_delete_wtf.data = data_nom_produit["fk_Categorie"]

            # Le bouton pour l'action "DELETE" dans le form. "produit_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_produit_delete_wtf:
        raise ExceptionProduitsDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{produits_delete_wtf.__name__} ; "
                                      f"{Exception_produit_delete_wtf}")

    return render_template("produits/produits_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_produit_delete)
