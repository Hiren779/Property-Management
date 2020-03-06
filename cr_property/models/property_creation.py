from odoo import api, fields, models
from openerp.exceptions import UserError, ValidationError


class PropertyCreation(models.Model):
    _name = "property.creation"
    _description = "Property Details"

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id and self.country_id != self.state_id.country_id:
            self.state_id = False

    @api.onchange('state_id')
    def _onchange_state(self):
        if self.state_id.country_id:
            self.country_id = self.state_id.country_id

    def delete_property(self):
        self.state = 'cancel'
        property_object = self.env["property.property"]
        all_property = property_object.search([('property_creation_id','=',self.id)])
        print("\n\n\n\n\n===========================",all_property)
        for property in all_property:
            if property.state != 'draft':
                raise UserError(('You cannot Delete this property Beacause you have already sold one of its subproperty'))
            else:
                property.unlink()

        return True

    def create_property(self):
        self.state = 'in_progress'
        for p in self:
            towers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
            tower = []
            for i in range(p.no_of_tower):
                tower.append(towers[i])
            floor = []
            for i in range(p.no_of_floor):
                floor.append(i + 1)
            l3 = []
            for i in (tower):
                for j in (floor):
                    l3.append(i + str(j))
            property = []
            for j in (l3):
                for k in range(p.no_of_property):
                    property.append(j + '0' + str(k + 1))
            # print(property)
            Tower = []
            for pro in property:
                Tower.append(pro[0])
            x = list(set(Tower))
            for i in x:
                vals1 = {'property_creation_id': self.id, 'name': i}
                tower_id = self.env['tower.details'].create(vals1)
            for pro in property:
                # print("=======================pro=====================", pro)
                # print("=======================self=====================", self)
                tower_id = self.env['tower.details'].search([('property_creation_id', '=', self.id), ('name', '=', pro[0])])
                # print('===============================tower===========', tower_id)
                vals = {'property_creation_id': self.id, 'properties': pro, 'tower_name': tower_id.id}
                # print("\n\n\n\n\n======================vals=========================", vals)
                property_id = self.env["property.property"].create(vals)

    # Smart Button

    @api.multi
    def button_property(self):
        return {
            'name': ('Property Creation'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': "property.property",
            'type': 'ir.actions.act_window',
            'domain': [('property_creation_id', '=', self.id)],
        }

    def compute_count(self):
        for property in self:
            property.property_count = self.env["property.property"].search_count(
                [('property_creation_id', '=', self.id)])

    # smart Button

    def button_contract(self):
        return {
            'name': ('Tenancy Details'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'tenancy.details',
            'type': 'ir.actions.act_window',
            'domain': [('tenant_id.property_creation_id.id', '=', self.id)],
        }

    def compute_count_contract(self):
        for contract in self:
            contract.contract_count = self.env["tenancy.details"].search_count(
                [('tenant_id.property_creation_id.id', '=', self.id)])



    # DASHBOARD

    def _get_action(self, action_xmlid):
        # print("\n\n\n\===========self==================",self)
        # print("\n\n\n\===========action_xmlid==================",action_xmlid)
        # TDE TODO check to have one view + custo in methods
        action = self.env.ref(action_xmlid).read()[0]
        print("\n\n\n\===========action==================", action)
        if self:
            action['domain'] = [('property_creation_id','=',self.id)]
        return action

    def get_property_type(self):
        return self._get_action('cr_property.action_property_listing_details')

    def _get_rent_action(self, action_xmlid):
        # print("\n\n\n\===========self==================",self)
        # print("\n\n\n\===========action_xmlid==================",action_xmlid)
        # TDE TODO check to have one view + custo in methods
        action = self.env.ref(action_xmlid).read()[0]
        print("\n\n\n\===========action==================", action)
        if self:
            action['domain'] = [('property_creation_id','=',self.id),('property_for','=', 'rent')]
        return action

    @api.one
    def compute_rent(self):
        for property in self:
            a = self.env["property.property"].search([('property_for','=', 'rent'),('property_creation_id','=',self.id)])
            property.rent_count = len(a.ids)
            # print('\n\n\n====count===', property.rent_count)

    def get_rent_details(self):
        return self._get_rent_action('cr_property.action_property_new_listing_details')

    def _get_sale_action(self, action_xmlid):
        action = self.env.ref(action_xmlid).read()[0]
        if self:
            action['domain'] = [('property_creation_id','=',self.id),('property_for','=', 'sale')]
        return action

    @api.one
    def compute_sale(self):
        for property in self:
            a = self.env["property.property"].search(
                [('property_for', '=', 'sale'), ('property_creation_id', '=', self.id)])
            property.sale_count = len(a.ids)
            # print('\n\n\n====sale===', property.rent_count)

    def get_sale_details(self):
        return self._get_sale_action('cr_property.action_property_listing_details')

    def change_colore_on_kanban(self):
        for record in self:
            color = 0
            if record.state == 'in_progress':
                color = 2
            elif record.state == 'sold':
                color = 5

            else:
                color = 5
            record.color = color
#=======================================================

    name = fields.Char(string="Name", required=True)
    street = fields.Char(string="Street1", required=True)
    street2 = fields.Char(string="Street2", required=True)
    city = fields.Char(string="City", required=True)
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]", required=True)
    zip = fields.Char(string="Zip code")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    email = fields.Char(string="Email", required=True)
    date = fields.Date(stinrg="Date", required=True)
    gfa = fields.Integer(string="GFA", help="Gross Floor Area(sqft)", required=True)
    property_type = fields.Char(string="Property Type", required=True)
    builder_name = fields.Char(string="Builder Name", required=True)
    no_of_tower = fields.Integer(string="No Of Tower", required=True)
    no_of_floor = fields.Integer(string="No Of Floor", required=True)
    no_of_property = fields.Integer(string="No Of Property", required=True)
    property_status = fields.Selection([('new','New'),('resale','ReSale')], default="new", required=True)

    property_aminities_ids = fields.Many2many("property.aminities")
    state = fields.Selection(
        [('draft', 'Draft'), ("in_progress", "In Progress"), ("sold", "Sold"), ("cancel", "Cancel")], string="Property Status", default="draft")
    property_count = fields.Integer(compute='compute_count')
    rent_count = fields.Integer(compute='compute_rent')
    sale_count = fields.Integer(compute='compute_sale')
    contract_count = fields.Integer(compute="compute_count_contract")
    color = fields.Integer('Color Index', compute="change_colore_on_kanban")
    property_elevation = fields.Binary()
    image = fields.Binary()
    property_image_ids = fields.One2many('property.image','property_creation_id',string='Property Images')


class PropertyProperty(models.Model):
    _name = "property.property"
    _description = "Property Listing"
    _rec_name = "properties"

    @api.multi
    def write(self, values):
        res = super(PropertyProperty, self).write(values)
        print('\n\n\n\n\n\n', res)
        temp = self.search([('state', '=', 'draft'), ('property_creation_id', '=', self.property_creation_id.id)])
        if not temp:
            # print(">>>xxx>>>>>>teSTE>>>>>>>>>", temp)
            self.property_creation_id.state = 'sold'
        return res

    def button_rent_contract(self):
        return {
            'name': ('Tenancy rent Details'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'rent.schedule',
            'type': 'ir.actions.act_window',
            'domain': [('property_id','=',self.properties),('property_creation_id', '=', self.property_creation_id.id)],
        }

    property_creation_id = fields.Many2one("property.creation", string="Property Creation Id", required=True)
    properties = fields.Char(string="Properties")
    property_for = fields.Selection([('sale', 'Sale'), ('rent', 'Rent')], default="sale", required=True,
                                    string='Property For')
    carpet_area = fields.Char()
    tower_name = fields.Many2one('tower.details', string='Tower Name')
    facing = fields.Selection([('east', 'East'), ('west', 'West'), ('north', 'North'), ('south', 'South')], default='south')
    flat_type = fields.Selection([('1bhk', '1BHK'), ('2bhk', '2BHK'), ('3bhk', '3BHK'), ('4bhk', '4BHK'), ('penthouse', 'PentHouse')])
    bathroom = fields.Integer()
    furnished = fields.Boolean(string="Furnished")
    property_price = fields.Integer(string="Property Price")
    rent_schedule_contract = fields.Many2one('rent.schedule',string='RentScheduleContract')

    state = fields.Selection(
        [('draft', 'Draft'), ("pending", "Pending"), ("sold", "Sold")],
        string="Property State", default="draft")

    

class TowerDetails(models.Model):
    _name = 'tower.details'
    _description = "Tower Details"


    property_creation_id = fields.Many2one('property.creation', string='Property Creation Id')
    name = fields.Char(string="Tower Name")

class PropertyAminities(models.Model):
    _name = "property.aminities"
    _description = "Aminities of Property"

    name = fields.Char()

class Property_Images(models.Model):
    _name = 'property.image'

    images1 = fields.Binary()
    name = fields.Char()
    property_creation_id = fields.Many2one('property.creation')