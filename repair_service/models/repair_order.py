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

    if len(self.sale_order_id) != 0:
        raise UserError("Sale order already exists for this repair order.")

    if not self.partner_id:
        raise UserError("You need to define a customer")

    super(RepairOrder, self).create_quotation()

    if len(self.sale_order_id) == 0 or len(self.sale_order_id.order_line) != 3:
        raise UserError("Sale order or sale order lines were not created correctly")

    with self.assertRaises(UserError) as err:
        self.action_create_sale_order()


def action_create_sale_order(self):
    if not self.partner_id:
        raise UserError("You need to define a customer")

    sale_order = self.env['sale.order'].create({
        'partner_id': self.partner_id.id,
        'repair_id': self.id,
    })

    self._add_service_lines(sale_order)

    self.sale_order_id = sale_order


def _add_service_lines(self, sale_order):
    order_lines = []
    for service in self.service_ids:
        order_lines.append((0, 0, {
            'product_id': service.product_id.id,
            'product_uom_qty': 1,
            'price_unit': service.product_id.lst_price,
        }))
    sale_order.write({'order_line': order_lines})