from odoo import models,api, fields
from datetime import datetime

class Etudiant(models.Model):
    _name = 'ucad.etudiant1'
    _description = 'Description de votre modèle Etudiant'

    matricule = fields.Char("Matricule", required=True, unique=True)
    nom = fields.Char("Nom")
    prenom = fields.Char("Prénom")
    date_naissance = fields.Date("Date de Naissance")
    
class Proprietair(models.Model):
    _name = 'ucad.proprietair'
    _description = 'Les proprietaires de la maison'
    _rec_name ="nom"
    
    nom = fields.Char("prenom nom")
    prenom =fields.Char("prenom")
    numero_card = fields.Char("numero de carte d'identite")
    photo = fields.Binary("photo")

    
    
class Maison(models.Model):
    _name = 'ucad.maison'
    _description = 'la table des maison'
    _rec_name ="nom"
    
    years = [(str(year), str(year)) for year in range(datetime.now().year - 3, datetime.now().year + 3)]
    ARRONDISSEMENTS_DAKAR = [
    ('plateau', 'Dakar Plateau'),
    ('medina', 'Medina'),
    ('fann', 'Fann-Point E-Amitié'),
    ('gueule-tapee', 'Gueule Tapée-Fass-Colobane'),
    ('hann-bel-air', 'Hann-Bel-Air'),
    ('hlm', 'HLM'),
    ('parcelles-assainies', 'Parcelles Assainies'),
    ('patte-doie', 'Patte d\'Oie'),
    ('grand-dakar', 'Grand Dakar'),
    ('dieuppeul-derkle', 'Dieuppeul-Derklé'),
    ('liberte', 'Liberté'),
    ('ngor', 'Ngor'),
    ('ouakam', 'Ouakam'),
    ('yoff', 'Yoff'),
        ]
    
    nom = fields.Char("numero de la maison")
    garage = fields.Boolean(string='Garage')
    gardien = fields.Boolean(string='gardien')
    photo1 = fields.Binary("photo1")
    photo2 = fields.Binary("photo2")
    photo3 = fields.Binary("photo3")
    appartement_ids = fields.One2many(
        'ucad.appartement',
        'maison',
        string='.'
        )
    factures= fields.One2many(
        'ucad.payment',
        'maison',
        string='.'
        )
    year = fields.Selection(selection=years, string='Année', default=str(datetime.now().year))
    arrondissement = fields.Selection(ARRONDISSEMENTS_DAKAR, string='quartier')
    proprietair = fields.Many2one('ucad.proprietair', string='proprietaire')
    locataires = fields.Many2many(
        'ucad.loact',
        string='.',
        compute='_compute_locataires',
        store=True
    )
    @api.depends('appartement_ids.locataire')
    def _compute_locataires(self):
        for maison in self:
            locataires = maison.appartement_ids.mapped('locataire')
            maison.locataires = [(6, 0, locataires.ids)]

class Appartement(models.Model):
    _name = 'ucad.appartement'
    _description = 'apart'
    _rec_name ="appartemment"
    
    
    nombre_chambre = fields.Integer("chambre")
    appartemment =fields.Char('nummero appartement')
    photo1 = fields.Binary("photo")
    photo2 = fields.Binary("photo")
    photo3 = fields.Binary("photo")
    prix = fields.Integer("prix de l'appartement par moi")
    maison = fields.Many2one('ucad.maison', string='maison')
    locataire = fields.Many2one('ucad.loact',string="locataire")
    #quartier = fields( string="quarier" , related='maison.arrondissement', readonly=True)
    
class Locat(models.Model):
    _name = 'ucad.loact'
    _description = 'la locat'
    _rec_name ='prenom'
    
    nom = fields.Char("nom")
    prenom = fields.Char("prenom")
    numero_tel = fields.Char("numero de telephone  ")
    photo_loca = fields.Binary("profile")
    photo_id_card_1 = fields.Binary("cart recto")
    photo_id_card_2 = fields.Binary("carte verso")
    appartement = fields.One2many('ucad.appartement', 'locataire', string='Appartements')
    maison = fields.Many2one('ucad.maison', string='Maison', related='appartement.maison', readonly=True)
    email = fields.Char("Email")
    payements= fields.One2many(
        'ucad.payment',
        'locataire',
        string='.'
        )

    
class Payment(models.Model):
    _name = 'ucad.payment'
    _description = 'pay'

    
    mois_de_l_annee = [
    ('Janvier','Janvier'),
    ('Février','Février'),
    ('Mars','Mars'),
    ('Avril','Avril'),
    ('Mai','Mai'),
    ('Juin','Juin'),
    ('Juillet','Juillet'),
    ('Aout','Août'),
    ('Septembre','Septembre'),
    ('Octobre','Octobre'),
    ('Novembre','Novembre'),
    ('Décembre','Novembre')
    ]
    years = [(str(year), str(year)) for year in range(datetime.now().year - 3, datetime.now().year + 3)]

    
    mois = fields.Selection(mois_de_l_annee, string='selectionner le mois a payer ')
    year = fields.Selection(selection=years, string='Année', default=str(datetime.now().year))
    #month = fields.Char(string='le mois a paye', default=lambda self: datetime.now().month)
    date = fields.Date(string='Date de payement ',default=lambda self: datetime.now())
    appartement = fields.Many2one('ucad.appartement', string='appartement ')
    locataire = fields.Many2one('ucad.loact',string="locataire" , related='appartement.locataire', readonly=True)
    prix = fields.Integer(string='prix ',related='appartement.prix', readonly=True)
    maison = fields.Many2one('ucad.maison',string="maison" , related='appartement.maison', readonly=True)
    email = fields.Char(string='email ',related='locataire.email', readonly=True)
    numero_tel = fields.Char(string='numero de telephone ',related='locataire.numero_tel', readonly=True)
    verif = fields.Char(string='Vérification', compute='_compute_verif', store=True)
 

    @api.depends('mois', 'locataire', 'year','appartement')
    def _compute_verif(self):
        for record in self:
            record.verif = f"{record.mois}-{record.locataire.nom}-{record.year}-{record.appartement.appartemment}"
    
    @api.model
    def create(self, vals):
        # Appel à la méthode originale pour créer le paiement
        payment = super(Payment, self).create(vals)
        
        # Envoi de l'e-mail au locataire
        payment.send_payment_email()
        
        return payment

    def send_payment_email(self):
        # Récupération des informations nécessaires pour l'e-mail
        locataire = self.locataire
        appartement =self.appartement
        maison = self.maison
        subject = "Confirmation de paiement 2xam imobilier "
        body = "Bonjour {0} {1}, votre paiement de {2} du mois de {3} de l'annees {4} pour l'appartement {5} de la maison {6} a bien été enregistré.".format(locataire.prenom ,locataire.nom ,appartement.prix,self.mois,self.year,appartement.appartemment,maison.nom)
        email_from = "sfaye5013@gmail.com"  # L'adresse e-mail de l'expéditeur
        
        # Envoi de l'e-mail
        self.env['mail.mail'].create({
            'subject': subject,
            'body_html': body,
            'email_from': email_from,
            'email_to': locataire.email,
        }).send()
    _sql_constraints = [
        ('unique_verif', 'UNIQUE(verif)', 'Ce paiement existe déjà.'),
        ('appartement_requis', 'CHECK(appartement IS NOT False)', 'L\'appartement est requis le paiement.'),
        ('appartement_requis', 'CHECK(date IS NOT False)', 'La date est requis le paiement.'),
        ('appartement_requis', 'CHECK(mois IS NOT False)', 'Le mois est requis le paiement.'),
        ('appartement_requis', 'CHECK(year IS NOT False)', 'L\'annee est requis le paiement.'),
    ]
    
        
   
    
    

    
    
    
    


    
    
