from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class ServiceService(models.Model):
    _name = 'service.service'
    _description = 'Service for Repairs'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', compute='_compute_end_date', store=True)
    repair_id = fields.Many2one('repair.order', string='Repair Order')

    @api.depends('start_date')
    def _compute_end_date(self):
        for record in self:
            if record.start_date:
                record.end_date = record.start_date + relativedelta(months=3)
            else:
                record.end_date = False
