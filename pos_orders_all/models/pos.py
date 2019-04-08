# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2015-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from openerp import fields, models, api, _
from openerp.exceptions import Warning
import random
from datetime import date, datetime



class pos_create_sales_order(models.Model):
    _name = 'pos.create.sales.order'


    @api.multi
    def create_sales_order(self, partner_id, orderlines):
    	sale_object = self.env['sale.order']
    	sale_order_line_obj = self.env['sale.order.line']
    	order_id = sale_object.create({'partner_id': partner_id})
    	for dict_line in orderlines:
    		product_obj = self.env['product.product'] 
    		product_dict  = dict_line.get('product')	
    		product_name =product_obj.browse(product_dict .get('id')).name	
    		vals = {'product_id': product_dict.get('id'),
    				'name':product_name,
    				'customer_lead':7,
    									'product_uom_qty': product_dict.get('quantity'),
    									'price_unit':product_dict.get('price'),
    									'product_uom':product_dict.get('uom_id'),
    									'order_id': order_id.id}
    		sale_order_line_obj.create(vals)					
    	
    						
    	return True
    	
    	
class pos_order(models.Model):
    _inherit = 'pos.order'
    
    
    def return_new_order(self):
       lines = []
       for ln in self.lines:
           lines.append(ln.id)
       vals = {
            'amount_total': self.amount_total,
            'date_order': self.date_order,
            'id': self.id,
            'name': self.name,
            'partner_id': [self.partner_id.id, self.partner_id.name] or '',
            'lines': lines,
            'pos_reference': self.pos_reference,
            'state': self.state,
            'session_id': [self.session_id.id, self.session_id.name],
            'company_id': [self.company_id.id, self.company_id.name],
            'barcode': self.barcode,
       }
       
       return vals
       
    def return_new_order_line(self):
       
       orderlines = self.env['pos.order.line'].search([('order_id.id','=', self.id)])
       
       final_lines = []
       #for ln in self.lines:
           #lines.append(ln.id)
       
       for l in orderlines:
           vals1 = {
                'discount': l.discount,
                'id': l.id,
                'order_id': [l.order_id.id, l.order_id.name],
                'price_unit': l.price_unit,
                'product_id': [l.product_id.id, l.product_id.name],
                'qty': l.qty,
           }
           final_lines.append(vals1)
           
       return final_lines


    @api.multi
    def print_pos_report(self):
    	return  self.env['report'].get_action(self, 'point_of_sale.report_receipt')



    @api.multi
    def print_pos_receipt(self):
        output = []
        discount = 0
        order_id = self.search([('id', '=', self.id)], limit=1)
        orderlines = self.env['pos.order.line'].search([('order_id', '=', order_id.id)])
        payments = self.env['account.bank.statement.line'].search([('pos_statement_id', '=', order_id.id)])
        paymentlines = []
        change = 0
        for payment in payments:
            if payment.amount > 0:
                temp = {
                    'amount': payment.amount,
                    'name': payment.journal_id.name
                }
                paymentlines.append(temp)
            else:
                change += payment.amount
        for orderline in orderlines:
            new_vals = {
                'product_id': orderline.product_id.name,
                'qty': orderline.qty,
                'price_unit': orderline.price_unit,
                'discount': orderline.discount,
                }
            discount += (orderline.price_unit * orderline.qty * orderline.discount) / 100
            output.append(new_vals)

        return [output, discount, paymentlines, change]	


class pos_config(models.Model):
    _inherit = 'pos.config'

    auto_check_invoice = fields.Boolean(string='Invoice Auto Check') 
    pos_bag_category_id = fields.Many2one('pos.category','Bag Charges Category') 
    allow_bag_charges = fields.Boolean('Allow Bag Charges')
    
    
    
