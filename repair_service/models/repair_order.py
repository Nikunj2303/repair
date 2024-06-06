from odoo import models, fields, api

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    service_ids = fields.One2many('service.service', 'repair_id', string='Services')

    def create_quotation(self):
        sale_order_obj = self.env['sale.order']
        sale_order_line_obj = self.env['sale.order.line']

        for order in self:
            sale_order = sale_order_obj.create({
                'partner_id': order.partner_id.id,
                'order_line': [(0, 0, {
                    'product_id': part.product_id.id,
                    'product_uom_qty': part.product_qty,
                    'price_unit': part.price_unit,
                }) for part in order.repair_line_ids] + [
                                  (0, 0, {
                                      'product_id': service.product_id.id,
                                      'product_uom_qty': 1,
                                      'price_unit': service.product_id.list_price,
                                  }) for service in order.service_ids
                              ]
            })
            order.sale_order_id = sale_order.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quotation',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': sale_order.id,
            'target': 'current',
        }

