from odoo.tests.common import TransactionCase
from odoo import fields

class TestProperty(TransactionCase):

    # setUp() => Saved Method That Using For Testing
    def setUp(self, *args, **kwargs):
        # Doing Overriding
        super(TestProperty, self).setUp()
        self.property_01_record = self.env['property.history'].create({
            'old_state': 'PRT10001',
            'new_state': 'property 1000',
            'reason': 'property 1000 description',
        })

    def test_01_property_values(self):
        property_id = self.property_01_record

        # assertRecordValues() =>Method That Using For Test values
        self.assertRecordValues(property_id, [{
              'old_state': 'PRT1000',
            'new_state': 'property 1000',
            'reason': 'property 1000 description',
        }])
    #----------------------------------------------------------------------------------------------------------
    # # setUp() => Saved Method That Using For Testing
    # def setUp(self, *args, **kwargs):
    #     #Doing Overriding
    #     super(TestProperty, self).setUp()
    #     self.property_01_record = self.env['property'].create({
    #         'ref':'PRT1000',
    #         'name':'property 1000',
    #         'description':'property 1000 description',
    #         'postcode':'1010',
    #         'data_availability':fields.Date.today(),
    #         'bedrooms':4,
    #         'expected_price':1000.3,
    #     })
    #
    # def test_01_property_values(self):
    #     property_id=self.property_01_record
    #
    #     # assertRecordValues() =>Method That Using For Test values
    #     self.assertRecordValues(property_id,[{
    #         'ref': 'PRT1000',
    #         'name': 'property 1000',
    #         'description': 'property 1000 description',
    #         'postcode': '1010',
    #         'data_availability': fields.Date.today(),
    #         'bedrooms': 4,
    #         'expected_price': 1000.3,
    #     }])
# odoo -d app_one --test-enable --init=app_one