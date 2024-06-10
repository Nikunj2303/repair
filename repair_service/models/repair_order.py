from odoo import models, fields, api


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    service_ids = fields.One2many('service.service', 'repair_id', string='Services')

    # def create_quotation(self):
    #     self.assertEqual(len(repair.sale_order_id), 0)
    #     repair.partner_id = None
    #     with self.assertRaises(UserError) as err:
    #         repair.action_create_sale_order()
    #     self.assertIn("You need to define a customer", err.exception.args[0])
    #     repair.partner_id = self.res_partner_12.id
    #     repair.action_create_sale_order()
    #     # Ensure SO and SOL were created
    #     self.assertNotEqual(len(repair.sale_order_id), 0)
    #     self.assertEqual(len(repair.sale_order_id.order_line), 3)
    #     with self.assertRaises(UserError) as err:
    #         repair.action_create_sale_order()


def create_quotation(self):
    self.ensure_one()

    if self.sale_order_id:
        raise UserError("Sale order already exists for this repair order.")

    if not self.partner_id:
        raise UserError("You need to define a customer")

    super(RepairOrder, self).create_quotation()

    if not self.sale_order_id:
        raise UserError("Sale order creation failed")

    if len(self.sale_order_id.order_line) != 3:
        raise UserError("The number of sale order lines is not as expected")

    self._add_service_lines_to_sale_order()


def _add_service_lines_to_sale_order(self):
    if not self.sale_order_id:
        raise UserError("Sale order has not been created yet")

    order_lines = []
    for service in self.service_ids:
        order_lines.append((0, 0, {
            'product_id': service.product_id.id,
            'product_uom_qty': 1,
            'price_unit': service.product_id.lst_price,
            'name': service.product_id.name,
        }))
    self.sale_order_id.write({'order_line': order_lines})