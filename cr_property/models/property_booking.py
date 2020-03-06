from odoo import models,fields,api

class Booking(models.Model):
    _name = 'property.booking'
    _description = 'Property Bookings'
    _rec_name = 'tenant_id'

    def Confirm_booking(self):
        self.state = 'booked'
        for i in self.property_id:
            i.state = 'sold'
        return {
            'type': 'ir.actions.act_window',
            'res_model': "tenancy.details",
            'context': {'default_tenant_id':self.id, 'default_property_creation_id': self.property_creation_id,},
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }

    def Pending_booking(self):
        self.state = 'pending'
        for i in self.property_id:
            i.state = 'pending'

    def Cancel_booking(self):
        self.state = 'cancel'

    def Draft_booking(self):
        self.state = 'draft'
        for i in self.property_id:
            i.state = 'draft'





    tenant_id = fields.Many2one("tenant.info", string='Name', required=True)
    property_for = fields.Selection([('sale', 'Sale'), ('rent', 'Rent')], default="sale", required=True,
                                    string='Property For')
    email = fields.Char('Email', required=True)
    date_of_birth = fields.Date('Date Of Birth')
    maritial_status = fields.Selection([('married', 'Married'), ('unmarried', 'Unmarried')], 'Maritial Status', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'),('other','Other')], 'Gender', required=True)
    street = fields.Char(string="Street1")
    street2 = fields.Char(string="Street2")
    city = fields.Char(string="City")
    state_id = fields.Char(string="State ID")
    zip = fields.Char(string="Zip code")
    country_id = fields.Char(string="Country Code")
    owner_name = fields.Char(string='Owner Name', required=True)
    tower_name = fields.Many2one('tower.details', string='Tower Name')
    property_creation_id = fields.Many2one("property.creation", string="Property Creation Id", required=True)
    property_id = fields.Many2one('property.property', string='Property Ids', required=True)
    tenancy_id = fields.Many2one("tenancy.details")


    state = fields.Selection(
        [('draft', 'Draft'), ("pending", "Pending"), ("booked", "Booked"), ("cancel", "Cancel")],
        string="Booking Status", default="draft")

