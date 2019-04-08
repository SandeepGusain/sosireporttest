# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _, tools
import random


class PosBarcode(models.Model):
    _inherit = 'pos.order'

    barcode = fields.Char(string='Barcode')
    
    #def barcode_create(self):
        #barcode = (random.randrange(1111111111111,9999999999999))
        #print "bbbbbbbbbbbbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa----------------", barcode
        #return barcode
    
    @api.model
    def create_from_ui(self, orders):
        order_ids = super(PosBarcode, self).create_from_ui(orders)
        for order_id in order_ids:
            pos_order_id = self.browse(order_id)
            if pos_order_id:
                ref_order = [o['data'] for o in orders if o['data'].get('name') == pos_order_id.pos_reference]
                for order in ref_order:
                    print "--------------------------order---------------------------------", order
                    barcode = (random.randrange(1111111111111,9999999999999)) #barcode = (random.randrange(1111111111111,9999999999999)) #order.get('barcode', False)
                    pos_order_id.write({'barcode': barcode})
        #print "---------------order_ids---------------------------------", order_ids, pos_order_id
        return order_ids

