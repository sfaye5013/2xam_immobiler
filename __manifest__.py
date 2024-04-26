# -*- coding: utf-8 -*-
{
    'name': "2xam immobiler ",

    'summary': """
        C'est l'immobilier de 2xam """,

    'description': """
        2xam est une entreprise spécialisée dans le développement d'applications
        visant à faciliter le travail des Sénégalais
        dans divers domaines. Le projet 2xam Immobilier
        vise à aider les courtiers en leur offrant 
        la possibilité d'enregistrer des maisons, de répertorier les appartements
        et les locataires, ainsi que d'envoyer les factures par e-mail apres chaque payment.
        Je souhaite continuer à améliorer ce projet, donc après la correction, 
        pouvez-vous me donner des suggestions pour l'améliorer davantage


        Voici un schéma simplifié de votre base de données avec les relations entre les différentes entités :
        Propriétaire 1 ---- * Maison
        Maison 1 ---- * Appartement
        Appartement * ---- 1 Locataire
        Locataire * ---- * Appartement
        Paiement * ---- 1 Locataire
        Paiement * ---- 1 Appartement
    """,

    'author': "souleymane FAYE",
    'website': "https://play.google.com/console/u/0/developers/6575005299020771739/app/4972168384102857196/app-dashboard?timespan=thirtyDays",
    'application':True,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
     
         'views/etudiant_views.xml',
         'views/payment_report_template.xml'
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
