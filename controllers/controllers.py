# -*- coding: utf-8 -*-
# from odoo import http


# class Ucad(http.Controller):
#     @http.route('/ucad/ucad', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ucad/ucad/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ucad.listing', {
#             'root': '/ucad/ucad',
#             'objects': http.request.env['ucad.ucad'].search([]),
#         })

#     @http.route('/ucad/ucad/objects/<model("ucad.ucad"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ucad.object', {
#             'object': obj
#         })
