# -*- coding: utf-8 -*-
{
    'name': "app_one",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
        Long description of module's purpose
    """,

    'author': "Eng_Muhamed EL_Nayed",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','account','mail','contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'data/data.xml',
        'views/views.xml',
        'views/base_menue.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sales_order_inherit_view.xml',
        'views/res_partner_inherit_view.xml',
        'views/building_view.xml',
        'views/property_history_view.xml',
        'views/account_move_inherit_view.xml',
        'wizard/property_change_state_wizard_view.xml',
        'report/property_report.xml',
    ],
    'assets':{
      'web.assets_backend':[
          'app_one\static\src\css\property.css',
          'app_one\static\src\components\listView\listView.css',
          'app_one\static\src\components\listView\listView.js',
          'app_one\static\src\components\listView\listView.xml',

      ] ,
      'web.report_assets_common':['app_one\static\src\css\font.css']
    },


    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}

