"""
    Fichier : gestion_films_genres_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les films et les produits.
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *

"""
    Nom : films_genres_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /films_genres_afficher
    
    But : Afficher les films avec les produits associés pour chaque film.
    
    Paramètres : id_Produit_sel = 0 >> tous les films.
                 id_Produit_sel = "n" affiche le film dont l'id est "n"
                 
"""


@app.route("/films_genres_afficher/<int:id_film_sel>", methods=['GET', 'POST'])
def films_genres_afficher(id_film_sel):
    print(" films_genres_afficher id_film_sel ", id_film_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_produits_films_afficher_data = """SELECT id_film, nom_film, duree_film, description_film, cover_link_film, date_sortie_film,
                                                            GROUP_CONCAT(intitule_produit) as GenresFilms FROM t_produit_film
                                                            RIGHT JOIN t_film ON t_film.id_film = t_produit_film.fk_film
                                                            LEFT JOIN t_genre ON t_genre.Produit = t_produit_film.fk_genre
                                                            GROUP BY id_film"""
                if id_film_sel == 0:
                    # le paramètre 0 permet d'afficher tous les films
                    # Sinon le paramètre représente la valeur de l'id du film
                    mc_afficher.execute(strsql_produits_films_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_film_selected_dictionnaire = {"value_id_film_selected": id_film_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_produits_films_afficher_data += """ HAVING id_film= %(value_id_film_selected)s"""

                    mc_afficher.execute(strsql_produits_films_afficher_data, valeur_id_film_selected_dictionnaire)

                # Récupère les données de la requête.
                data_produits_films_afficher = mc_afficher.fetchall()
                print("data_produits ", data_produits_films_afficher, " Type : ", type(data_produits_films_afficher))

                # Différencier les messages.
                if not data_produits_films_afficher and id_film_sel == 0:
                    flash("""La table "t_film" est vide. !""", "warning")
                elif not data_produits_films_afficher and id_film_sel > 0:
                    # Si l'utilisateur change l'id_film dans l'URL et qu'il ne correspond à aucun film
                    flash(f"Le film {id_film_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données films et produits affichés !!", "success")

        except Exception as Exception_films_genres_afficher:
            raise ExceptionFilmsGenresAfficher(f"fichier : {Path(__file__).name}  ;  {films_genres_afficher.__name__} ;"
                                               f"{Exception_films_genres_afficher}")

    print("films_genres_afficher  ", data_produits_films_afficher)
    # Envoie la page "HTML" au serveur.
    return render_template("films_genres/films_genres_afficher.html", data=data_produits_films_afficher)


"""
    nom: edit_produit_film_selected
    On obtient un objet "objet_dumpbd"

    Récupère la liste de tous les produits du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les produits contenus dans la "t_genre".
    2) Les produits attribués au film selectionné.
    3) Les produits non-attribués au film sélectionné.

    On signale les erreurs importantes

"""


@app.route("/edit_produit_film_selected", methods=['GET', 'POST'])
def edit_produit_film_selected():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_produits_afficher = """SELECT Produit, intitule_produit FROM t_genre ORDER BY id_Produit ASC"""
                mc_afficher.execute(strsql_produits_afficher)
            data_produits_all = mc_afficher.fetchall()
            print("dans edit_produit_film_selected ---> data_produits_all", data_produits_all)

            # Récupère la valeur de "id_film" du formulaire html "films_genres_afficher.html"
            # l'utilisateur clique sur le bouton "Modifier" et on récupère la valeur de "id_film"
            # grâce à la variable "id_film_produits_edit_html" dans le fichier "films_genres_afficher.html"
            # href="{{ url_for('edit_produit_film_selected', id_film_produits_edit_html=row.id_film) }}"
            id_film_produits_edit = request.values['id_film_produits_edit_html']

            # Mémorise l'id du film dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_film_produits_edit'] = id_film_produits_edit

            # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
            valeur_id_film_selected_dictionnaire = {"value_id_film_selected": id_film_produits_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la fonction produits_films_afficher_data
            # 1) Sélection du film choisi
            # 2) Sélection des produits "déjà" attribués pour le film.
            # 3) Sélection des produits "pas encore" attribués pour le film choisi.
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "produits_films_afficher_data"
            data_produit_film_selected, data_produits_films_non_attribues, data_produits_films_attribues = \
                produits_films_afficher_data(valeur_id_film_selected_dictionnaire)

            print(data_produit_film_selected)
            lst_data_film_selected = [item['id_film'] for item in data_produit_film_selected]
            print("lst_data_film_selected  ", lst_data_film_selected,
                  type(lst_data_film_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les produits qui ne sont pas encore sélectionnés.
            lst_data_produits_films_non_attribues = [item['id_Produit'] for item in data_produits_films_non_attribues]
            session['session_lst_data_produits_films_non_attribues'] = lst_data_produits_films_non_attribues
            print("lst_data_produits_films_non_attribues  ", lst_data_produits_films_non_attribues,
                  type(lst_data_produits_films_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les produits qui sont déjà sélectionnés.
            lst_data_produits_films_old_attribues = [item['id_Produit'] for item in data_produits_films_attribues]
            session['session_lst_data_produits_films_old_attribues'] = lst_data_produits_films_old_attribues
            print("lst_data_produits_films_old_attribues  ", lst_data_produits_films_old_attribues,
                  type(lst_data_produits_films_old_attribues))

            print(" data data_produit_film_selected", data_produit_film_selected, "type ", type(data_produit_film_selected))
            print(" data data_produits_films_non_attribues ", data_produits_films_non_attribues, "type ",
                  type(data_produits_films_non_attribues))
            print(" data_produits_films_attribues ", data_produits_films_attribues, "type ",
                  type(data_produits_films_attribues))

            # Extrait les valeurs contenues dans la table "t_produits", colonne "intitule_produit"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_Produit
            lst_data_produits_films_non_attribues = [item['intitule_produit'] for item in data_produits_films_non_attribues]
            print("lst_all_produits gf_edit_produit_film_selected ", lst_data_produits_films_non_attribues,
                  type(lst_data_produits_films_non_attribues))

        except Exception as Exception_edit_produit_film_selected:
            raise ExceptionEditGenreFilmSelected(f"fichier : {Path(__file__).name}  ;  "
                                                 f"{edit_produit_film_selected.__name__} ; "
                                                 f"{Exception_edit_produit_film_selected}")

    return render_template("films_genres/films_genres_modifier_tags_dropbox.html",
                           data_produits=data_produits_all,
                           data_film_selected=data_produit_film_selected,
                           data_produits_attribues=data_produits_films_attribues,
                           data_produits_non_attribues=data_produits_films_non_attribues)


"""
    nom: update_produit_film_selected

    Récupère la liste de tous les produits du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les produits contenus dans la "t_genre".
    2) Les produits attribués au film selectionné.
    3) Les produits non-attribués au film sélectionné.

    On signale les erreurs importantes
"""


@app.route("/update_produit_film_selected", methods=['GET', 'POST'])
def update_produit_film_selected():
    if request.method == "POST":
        try:
            # Récupère l'id du film sélectionné
            id_film_selected = session['session_id_film_produits_edit']
            print("session['session_id_film_produits_edit'] ", session['session_id_film_produits_edit'])

            # Récupère la liste des produits qui ne sont pas associés au film sélectionné.
            old_lst_data_produits_films_non_attribues = session['session_lst_data_produits_films_non_attribues']
            print("old_lst_data_produits_films_non_attribues ", old_lst_data_produits_films_non_attribues)

            # Récupère la liste des produits qui sont associés au film sélectionné.
            old_lst_data_produits_films_attribues = session['session_lst_data_produits_films_old_attribues']
            print("old_lst_data_produits_films_old_attribues ", old_lst_data_produits_films_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme produits dans le composant "tags-selector-tagselect"
            # dans le fichier "produits_films_modifier_tags_dropbox.html"
            new_lst_str_produits_films = request.form.getlist('name_select_tags')
            print("new_lst_str_produits_films ", new_lst_str_produits_films)

            # OM 2021.05.02 Exemple : Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_produit_film_old = list(map(int, new_lst_str_produits_films))
            print("new_lst_produit_film ", new_lst_int_produit_film_old, "type new_lst_produit_film ",
                  type(new_lst_int_produit_film_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2021.05.02 Une liste de "id_Produit" qui doivent être effacés de la table intermédiaire "t_produit_film".
            lst_diff_produits_delete_b = list(set(old_lst_data_produits_films_attribues) -
                                            set(new_lst_int_produit_film_old))
            print("lst_diff_produits_delete_b ", lst_diff_produits_delete_b)

            # Une liste de "id_Produit" qui doivent être ajoutés à la "t_produit_film"
            lst_diff_produits_insert_a = list(
                set(new_lst_int_produit_film_old) - set(old_lst_data_produits_films_attribues))
            print("lst_diff_produits_insert_a ", lst_diff_produits_insert_a)

            # SQL pour insérer une nouvelle association entre
            # "fk_film"/"id_film" et "fk_genre"/"id_Produit" dans la "t_produit_film"
            strsql_insert_produit_film = """INSERT INTO t_produit_film (id_Produit_film, fk_genre, fk_film)
                                                    VALUES (NULL, %(value_fk_genre)s, %(value_fk_film)s)"""

            # SQL pour effacer une (des) association(s) existantes entre "id_film" et "id_Produit" dans la "t_produit_film"
            strsql_delete_produit_film = """DELETE FROM t_produit_film WHERE fk_genre = %(value_fk_genre)s AND fk_film = %(value_fk_film)s"""

            with DBconnection() as mconn_bd:
                # Pour le film sélectionné, parcourir la liste des produits à INSÉRER dans la "t_produit_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_produit_ins in lst_diff_produits_insert_a:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_produit_ins" (l'id du produit dans la liste) associé à une variable.
                    valeurs_film_sel_produit_sel_dictionnaire = {"value_fk_film": id_film_selected,
                                                               "value_fk_genre": id_produit_ins}

                    mconn_bd.execute(strsql_insert_produit_film, valeurs_film_sel_produit_sel_dictionnaire)

                # Pour le film sélectionné, parcourir la liste des produits à EFFACER dans la "t_produit_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_produit_del in lst_diff_produits_delete_b:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_produit_del" (l'id du produit dans la liste) associé à une variable.
                    valeurs_film_sel_produit_sel_dictionnaire = {"value_fk_film": id_film_selected,
                                                               "value_fk_genre": id_produit_del}

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "execute" dans la classe "DBconnection"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "DBconnection"
                    # sera interprété, ainsi on fera automatiquement un commit
                    mconn_bd.execute(strsql_delete_produit_film, valeurs_film_sel_produit_sel_dictionnaire)

        except Exception as Exception_update_produit_film_selected:
            raise ExceptionUpdateGenreFilmSelected(f"fichier : {Path(__file__).name}  ;  "
                                                   f"{update_produit_film_selected.__name__} ; "
                                                   f"{Exception_update_produit_film_selected}")

    # Après cette mise à jour de la table intermédiaire "t_produit_film",
    # on affiche les films et le(urs) produit(s) associé(s).
    return redirect(url_for('films_genres_afficher', id_film_sel=id_film_selected))


"""
    nom: produits_films_afficher_data

    Récupère la liste de tous les produits du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des produits, ainsi l'utilisateur voit les produits à disposition

    On signale les erreurs importantes
"""


def produits_films_afficher_data(valeur_id_film_selected_dict):
    print("valeur_id_film_selected_dict...", valeur_id_film_selected_dict)
    try:

        strsql_film_selected = """SELECT id_film, nom_film, duree_film, description_film, cover_link_film, date_sortie_film, GROUP_CONCAT(id_Produit) as GenresFilms FROM t_produit_film
                                        INNER JOIN t_film ON t_film.id_film = t_produit_film.fk_film
                                        INNER JOIN t_genre ON t_genre.id_Produit = t_produit_film.fk_genre
                                        WHERE id_film = %(value_id_film_selected)s"""

        strsql_produits_films_non_attribues = """SELECT id_Produit, intitule_produit FROM t_genre WHERE id_Produit not in(SELECT id_Produit as idGenresFilms FROM t_produit_film
                                                    INNER JOIN t_film ON t_film.id_film = t_produit_film.fk_film
                                                    INNER JOIN t_genre ON t_genre.id_Produit = t_produit_film.fk_genre
                                                    WHERE id_film = %(value_id_film_selected)s)"""

        strsql_produits_films_attribues = """SELECT id_film, id_Produit, intitule_produit FROM t_produit_film
                                            INNER JOIN t_film ON t_film.id_film = t_produit_film.fk_film
                                            INNER JOIN t_genre ON t_genre.id_Produit = t_produit_film.fk_genre
                                            WHERE id_film = %(value_id_film_selected)s"""

        # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
        with DBconnection() as mc_afficher:
            # Envoi de la commande MySql
            mc_afficher.execute(strsql_produits_films_non_attribues, valeur_id_film_selected_dict)
            # Récupère les données de la requête.
            data_produits_films_non_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("produits_films_afficher_data ----> data_produits_films_non_attribues ", data_produits_films_non_attribues,
                  " Type : ",
                  type(data_produits_films_non_attribues))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_film_selected, valeur_id_film_selected_dict)
            # Récupère les données de la requête.
            data_film_selected = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_film_selected  ", data_film_selected, " Type : ", type(data_film_selected))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_produits_films_attribues, valeur_id_film_selected_dict)
            # Récupère les données de la requête.
            data_produits_films_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_produits_films_attribues ", data_produits_films_attribues, " Type : ",
                  type(data_produits_films_attribues))

            # Retourne les données des "SELECT"
            return data_film_selected, data_produits_films_non_attribues, data_produits_films_attribues

    except Exception as Exception_produits_films_afficher_data:
        raise ExceptionGenresFilmsAfficherData(f"fichier : {Path(__file__).name}  ;  "
                                               f"{produits_films_afficher_data.__name__} ; "
                                               f"{Exception_produits_films_afficher_data}")
