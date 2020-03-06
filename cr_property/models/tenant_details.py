from odoo import models,fields,api
from dateutil.relativedelta import relativedelta

class TenantInformation(models.Model):
    _name = "tenant.info"
    _description = "Tenant Details"

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id and self.country_id != self.state_id.country_id:
            self.state_id = False

    @api.onchange('state_id')
    def _onchange_state(self):
        if self.state_id.country_id:
            self.country_id = self.state_id.country_id

    @api.multi
    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth <= fields.Date.today():
                record.age = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.date_of_birth)).years
            else:
                record.age = 0

    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string='Age',compute="_compute_age")
    date_of_birth = fields.Date(string='Date Of Birth')
    email = fields.Char(string="Email", required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], 'Gender', required=True)
    occupation = fields.Char(string='Occupation')
    contact_no = fields.Char(string='Contact No.', required=True)
    property_for = fields.Selection([('sale', 'Sale'), ('rent', 'Rent')], default="sale", required=True,
                                    string='Property For')
    street = fields.Char(string="Street1", required=True)
    street2 = fields.Char(string="Street2", required=True)
    city = fields.Char(string="City", required=True)
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]", required=True)
    zip = fields.Char(string="Zip code")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')


