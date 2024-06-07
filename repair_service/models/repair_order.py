from odoo import models, fields, api

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    service_ids = fields.One2many('service.service', 'repair_id', string='Services')

    def create_quotation(self):
        # Call the base method first
        res = super(RepairOrder, self).create_quotation()

        sale_order_id = res.get('res_id')

        if not sale_order_id:
            return res

        sale_order = self.env['sale.order'].browse(sale_order_id)

        for order in self:
            sale_order_lines = []

            for part in order.repair_line_ids:
                sale_order_lines.append((0, 0, {
                    'product_id': part.product_id.id,
                    'product_uom_qty': part.product_qty,
                    'price_unit': part.price_unit,
                }))

            for service in order.service_ids:
                sale_order_lines.append((0, 0, {
                    'product_id': service.product_id.id,
                    'product_uom_qty': 1,
                    'price_unit': service.product_id.list_price,
                }))

            sale_order.write({'order_line': sale_order_lines})

        return res