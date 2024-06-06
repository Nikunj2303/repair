from odoo import models, fields, api

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    service_ids = fields.One2many('service.service', 'repair_order_id', string='Services')

    def create_quotation(self):
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'order_line': [(0, 0, {
                'product_id': part.product_id.id,
                'product_uom_qty': part.product_qty,
                'price_unit': part.price_unit,
            }) for part in self.repair_line_ids] + [
                (0, 0, {
                    'product_id': service.product_id.id,
                    'product_uom_qty': 1,
                    'price_unit': service.product_id.list_price,
                }) for service in self.service_ids
            ]
        })
        self.sale_id = sale_order.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quotation',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': sale_order.id,
            'target': 'current',
        }
