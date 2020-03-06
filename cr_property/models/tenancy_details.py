from odoo import models,fields,api,_
from datetime import datetime
from dateutil import relativedelta
import calendar
import datetime


class TenancyDetails(models.Model):
    _name = "tenancy.details"
    _description = "Tenancy Details"
    # _rec_name = 'tenant_id'

    @api.onchange('tenant_id')
    def onchange_property(self):
        self.property_creation_id = self.tenant_id.property_creation_id.name
        self.property_id = self.tenant_id.property_id.properties

    @api.onchange('start_date', 'expiration_date')
    def onchange_month(self):
        if self.start_date and self.expiration_date and self.tenancy_rent:
            if self.expiration_date > self.start_date:
                x = self.expiration_date.month - self.start_date.month + 12 * (self.expiration_date.year - self.start_date.year)
                # print("\n\n\n\n\================x=================",x)
                self.total_rent = x * self.tenancy_rent
                print('=======elf====================',self.total_rent)
            else:
                warning_mess = {
                    'title': _('Warning!'),
                    'message': _(
                        'expiration_date must Be greter than start_date !!'),
                }
                return {'warning': warning_mess}

    def create_rent_record(self):
        # print("context----------", self, self._context.get('active_id'), self._context)
        record_ids = self.env['property.booking'].browse(self._context.get('active_id'))
        for record in record_ids:
            record.write({
                'tenancy_id': self.id
            })
        if self.start_date and self.expiration_date and self.tenancy_rent:
            x = self.expiration_date.month - self.start_date.month + 12 * (self.expiration_date.year - self.start_date.year)
            lst_of_date = []
            y = self.start_date
            for i in range(x):
                days = calendar.monthrange(self.start_date.year, self.start_date.month)[1]
                lst_of_date.append(str(self.start_date + datetime.timedelta(days=days)))
                self.start_date = self.start_date + datetime.timedelta(days=days)
            # print(lst_of_date)
            self.start_date = y
            for i in lst_of_date:
                vals = {'date': i, 'amount': self.tenancy_rent,'tenancy_detail_id':self.id,'pending_amount':self.tenancy_rent,
                        'tenant_id':self.tenant_id.tenant_id.name,'property_creation_id':self.tenant_id.property_creation_id.id,'property_id':self.tenant_id.property_id.id}
                print("===============vals=======================",vals)
                tenancy = self.env['rent.schedule'].create(vals)


    name = fields.Char("Name")
    tenant_id = fields.Many2one('property.booking',string='Tenant Id', required=True)
    property_creation_id = fields.Char(string='Property Creation Id')
    property_id = fields.Char(string="Property Id")
    tenancy_rent = fields.Integer(string='Tenancy Rent', required=True)
    tenancy_deposit = fields.Integer(string='Tenancy Deposit')
    start_date = fields.Date(string='Start Date', required=True)
    expiration_date = fields.Date(string='Expiration Date', required=True)
    total_rent = fields.Integer(string='Total Rent')
    month = fields.Char()
    rent_type = fields.Selection([('monthly','Monthly'),('quarterly','Quarterly')], required=True)
    rent_schedule_line_ids = fields.One2many('rent.schedule', 'tenancy_detail_id', string='Rent Schedule')
    state = fields.Selection(
        [('new', 'New'), ("in_progress", "In Progress"), ("cancel", "Closed")],
        string="Tenancy State", default="new")


class RentScheduleDetail(models.Model):
    _name = 'rent.schedule'
    _description = 'Rent Schedule Details'

    def amount_paid(self):
        self.paid = True
        self.pending_amount = self.pending_amount - self.amount
        self.tenancy_detail_id.state = 'in_progress'

    tenant_id = fields.Char(string='Tenant Id')
    property_creation_id = fields.Many2one('property.creation',string='Property Creation Id')
    property_id = fields.Many2one('property.property',string = 'Booking')
    date = fields.Char(string='Date')
    amount = fields.Integer(string='Amount')
    pending_amount = fields.Integer(string='Pending Amount')
    paid = fields.Boolean(string='Paid')
    tenancy_detail_id = fields.Many2one('tenancy.details')