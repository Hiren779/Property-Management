# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Property Management',
    'version': '1',
    'summary': 'Management Of Property',
    'sequence': 1,
    'description': """Management Of Property""",

    'category': 'Property Management',
    'website': 'https://www.candidroot.com/page/property',
    'images': [],
    'depends': [],
    'data': [

        'security/ir.model.access.csv',
        'views/property_creation_details.xml',
        'views/property_listing.xml',
        'views/property_booking.xml',
        'views/tower_details.xml',
        'views/property_dashboard.xml',
        'views/tenant_details.xml',
        'views/tenancy_details.xml',
        'views/rent_schedule.xml',
        'views/property_image.xml',

    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
