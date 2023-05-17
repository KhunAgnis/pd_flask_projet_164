"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterProduit(FlaskForm):
    """
        Dans le formulaire "produits_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_produits_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_produits_wtf = StringField("Clavioter le nom ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_produits_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    taille_produits_regexp = r"^([A-Z]|[0-9])+$"
    taille_produits_wtf = StringField("Clavioter la taille", validators=[
                                                                Length(min=1, max=20, message="Min 1 max 20"),
                                                                Regexp(taille_produits_regexp, message="Chiffre et lettre uniquement (pas de caractères spéciaux)")
                                                                    ])
    couleur_produits_regexp = r"^([A-Z]|[0-9])+$"
    couleur_produits_wtf = StringField("Clavioter la couleur ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                        Regexp(couleur_produits_regexp,
                                                                               message="Chiffre et lettre uniquement (pas de caractères spéciaux)")
                                                                        ])
    categorie_produits_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    categorie_produits_wtf = StringField("Clavioter la catégorie ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                        Regexp(categorie_produits_regexp,
                                                                               message="Chiffre et lettre uniquement (pas de caractères spéciaux)")
                                                                        ])
    submit = SubmitField("Enregistrer ce produit")



class FormWTFUpdateProduit(FlaskForm):
    """
        Dans le formulaire "produit_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_produit_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_produit_update_wtf = StringField("Clavioter le produit ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_produit_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    date_produits_wtf_essai = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update produit")


class FormWTFDeleteProduit(FlaskForm):
    """
        Dans le formulaire "produit_delete_wtf.html"

        nom_produit_delete_wtf : Champ qui reçoit la valeur du produit, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "produit".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_produit".
    """
    nom_produit_delete_wtf = StringField("Effacer ce produit")
    submit_btn_del = SubmitField("Effacer produit")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
