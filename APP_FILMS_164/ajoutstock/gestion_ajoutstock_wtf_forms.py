"""Gestion des formulaires avec WTF pour les films
Fichier : gestion_films_wtf_forms.py
Auteur : OM 2022.04.11

"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Length
from wtforms.validators import Regexp
from wtforms import IntegerField
from wtforms import SelectField
from wtforms.validators import DataRequired


class FormWTFAjouterStock(FlaskForm):
    lieu_stock_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    lieu_stock_wtf = StringField("Insérer le lieu du stock ",
                                           validators=[Length(min=2, max=200, message="Nom valide attendu"),
                                                       Regexp(lieu_stock_regexp,
                                                        message="Lettre uniquement")
                                                       ])

    quantite_ajouter_regexp = "^[0-9]+$"
    quantite_ajouter_wtf = StringField("Inscrire la quantité ",
                                       validators=[Length(min=1, max=200, message="Quantité attendue"),
                                                   Regexp(quantite_ajouter_regexp,
                                                          message="Veuillez entrer un nombre entre 0 et 9")])


produit_id = SelectField("Produit", coerce=int, validators=[DataRequired()])

    submit = SubmitField("Enregistrer dans le stock")
