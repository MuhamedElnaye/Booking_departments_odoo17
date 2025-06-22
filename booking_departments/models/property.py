from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta
import requests

class Property(models.Model):
    _name = "property"
    # _description = "Property"  # that show in chatter during create new property
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # default => default Name that will show when you do new property
    # Size   => Meaning the Number Of Letters That will Enter Only
    ref = fields.Char(default='New',readonly=True) #For Create Sequence
    # name = fields.Char(required=1, default='New', size=40,translate=True)
    name = fields.Char(required=1, default='New', size=40)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=True)
    data_availability = fields.Date(tracking=1)

    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()

    # expected_price=fields.Float(digits=(0,5))=> digits=(0,5) using to can control in number of digits after and before ',' in float number
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff', store=1, readonly=0)
    # diff=fields.Float(compute='_compute_diff')
    # store=1 default:0 =>for storing this value in Database
    # readonly=0  " default : readonly=1 " =>using to can edit it and update it "default='readonly=1'"
    # Note :by doing "compute" only don't store this compute or Value in DB to do this you Should use:
    # the parameter " store=1" To store In Database
    # compute='_compute_diff' for doing function "_compute_diff"

    # def _compute_diff(self):
    #     for rec in self:
    #         rec.diff = rec.expected_price - rec.selling_price
    bedrooms = fields.Integer()
    Living_area = fields.Integer()
    garage = fields.Boolean(groups="app_one.property_manager_group")
    garden_area = fields.Boolean()
    active = fields.Boolean(default=True)
    ### video (53) task 2 ########
    #make default(create_time) data and time during create new record and add 6 hours
    create_time=fields.Datetime(default=fields.datetime.now())
    next_time=fields.Datetime(compute="_compute_next_time")
    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time=rec.create_time+timedelta(hours=6)
            else:
                rec.next_time=False
    ############  Relation Fields ##############################
    line_ids = fields.One2many('property.line', 'property_id')
    tag_ids = fields.Many2many("tags")
    owner_id = fields.Many2one("owner")
    # owner_address=fields.Char(related='owner_id.address',readonly=0,store=1)
    # owner_phone=fields.Char(related='owner_id.phone',readonly=0,store=1)
    owner_address = fields.Char(compute='_compute_diff', store=1, readonly=0)
    owner_phone = fields.Char(compute='_compute_diff', store=1, readonly=0)

    grand_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')],
        default='north'
        # Note [North,South,East,West] =>this Values that show in the app
        # default="north"  or [south,east,west] =>using to show the default selection during create new student
        # and saved or Set  in DataBase
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is Exist')
    ]

    @api.depends('expected_price', 'selling_price', 'owner_id.phone', 'owner_id.address')
    def _compute_diff(self):
        for rec in self:
            print(rec)
            print("inside  _compute_diff Method")
            rec.diff = rec.expected_price - rec.selling_price
            rec.owner_address = rec.owner_id.address
            rec.owner_phone = rec.owner_id.phone

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print(rec)
            print("Inside  _onchange_expected_price Method")
            return {
                'warning': {'title': 'warning', 'message': 'This is a Negative value', "type": 'notification'}
            }

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                # print("Not Valid Value")
                raise ValidationError("PLease add a valid number of bedrooms!")

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state,'draft')#'rec.state' the Old state ,'draft'=> the new state
            print("inside Draft Action")
            rec.state = 'draft'
            # you can write this (rec.state='draft' ) by another way :
            # rec.write({
            #     'state':'draft'
            # })

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state,'pending')#'rec.state' the Old state ,'draft'=> the new state
            print("inside Pending Action")
            # rec.state='pending'
            # you can write this (rec.state='draft' ) by another way :
            rec.write({
                'state': 'pending'
            })

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')  # 'rec.state' the Old state ,'draft'=> the new state
            print("inside Sold Action")
            # rec.state='sold'
            # you can write this (rec.state='draft' ) by another way :
            rec.write({
                'state': 'sold'
            })

    ### Server_Actions ##############
    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')  # 'rec.state' the Old state ,'draft'=> the new state
            print("Inside Closed Action")
            rec.state = 'closed'

    ### Automated_Actions ##############
    def check_expected_selling_date(self):
        print(self)
        # property_id=self.env['property'].search([('name','!=','property1')])
        # property_id=self.search([('name','!=','property1')])
        property_id = self.search([])
        print(property_id)
        for rec in property_id:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True
            # This if condition meaning: If "expected_selling_date" found and less than "date.today()"
            # make "is_late" True

    def action(self):
        # print(self.env['owner'].create({
        #     'name':'name Four',
        #     'phone':'01111000000'
        # }))  # by doing this you can access "owner" model and create New owner
        # print(self.env['owner'].search([])) #will return "owner_id" that created "owner(1, 2, 3, 4, 5, 6, 7)"

        #######video [56] search domain #############
        # print(self.env['property'].search([('name','=','property1')])) #will return 'property(1,)'
        # print(self.env['property'].search([('name','!=','property1')])) #will return 'property(2, 3, 4, 5, 6, 7, 8, 14, 16, 22, 23, 26, 28, 29, 30, 31, 32)'
        # print(self.env['property'].search([('name','in',('property1','property2'))])) #will return 'property(1, 3)'
        # print(self.env['property'].search([('name','in',['property1','property2'])])) #will return 'property(1, 3)'
        # print(self.env['property'].search([('name','like','property1')])) #will return 'property(16, 22, 23, 28, 30)' not return 'Property1'
            #like =>its return identical value only
        # print(self.env['property'].search([('name','ilike','property1')])) #will return 'property(1, 16, 22, 23, 28, 30)'
                # return small and capital words

        ##### Logical Operators [! Not,| OR ,& and]
        # print(self.env['property'].search([('name','=','Property1'),('postcode','=','123131')])) #',' refer to [and] will return 'property(1,)'
        # print(self.env['property'].search([('name','=','Property1'),('postcode','=','123131')])) #',' refer to [and] will return 'property()'
        #[| OR Operator] only one condition should be Found
        print(self.env['property'].search(['|',('name','=','Property1'),('postcode','!=','123131')])) #will return 'property(1, 2, 3, 4, 5, 6, 7, 8, 14, 16, 22, 23, 26, 28, 29, 30, 31, 32)'
        #[& And Operator] =>default Must be two Condition found
        print(self.env['property'].search(['&',('name','=','Property1'),('postcode','!=','123131')])) #will return 'property()'
        #[! Not Operator] not condition on and condition 2
        print(self.env['property'].search(['!',('name','=','Property1'),('postcode','!=','123131')])) #will return 'property(2, 3, 4, 5, 6, 7, 8, 14, 16, 22, 23, 26, 28, 29, 30, 31, 32)'

    ##### Create Method For "Sequence" #########
    @api.model
    # @api.model_create_multi (any one of them good)
    def create(self, vals):
        res=super(Property,self).create(vals)
        # 'Property' => Class name
        if res.ref=='New':
            res.ref=self.env['ir.sequence'].next_by_code("property_seq")
            #  next_by_code("property_seq")=>method the used to add +1 for sequence
            # 'property_seq' =>found in 'data/sequence.xml' File
        return res

    #### Task video (51) History Record ############
    def create_history_record(self,old_state,new_state,reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id':rec.env.uid,#'rec.env.uid' meaning return 'user_id'that Found in "odoo base"
                'property_id':rec.id,
                'old_state':old_state,
                'new_state':new_state,
                'reason':reason or '', #coming from 'property_change_state_wizard.py' file
                'line_ids':[(0,0,{'description':line.description,'area':line.area})for line in rec.line_ids]
                # 'line_ids':[(0,0,{'property_id':rec.id,'description':line.description,'area':line.area} for line in rec.line_ids)]
                # this line above calling (magic or command Tuples)
                # first "0" for create Method
                # second '0' for create record not found and if found will write "ids" of records if you Write it Give Error
                #('property_id':rec.id) this record create automatically default record that will create it
                #('description':line.description) =>description of "property.history" Model
                #('area':line.area) =>area of "property.history" Model
            })
    #########  Wizard video(53) ####################
    def action_open_property_change_state_wizard(self):
        action=self.env['ir.actions.actions']._for_xml_id('app_one.property_change_state_wizard_action')
        # 'ir.actions.actions' =>the Model that we use it to call wizard actions
        # '_for_xml_id('app_one.property_change_state_wizard_action') ' =>The method that will show
            # bubbles of wizard Action where we call from 'app_one' action 'property_change_state_wizard_action'
        # "property_change_state_wizard_action " =>Found in 'property_change_state_wizard_view.xml' File
        action['context']={'default_property_id':self.id}
        # action['context']={'default_property_id':self.id}=>its using to make a default value For "property_id"
            #where this value will be the property that I Found in it 'self.id'
        return action
    ########### video(60) Smart button #########
    def action_open_related_owner(self):
        action=self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        # _for_xml_id('app_one.owner_action')=>built in method that can calling action with id => 'app_one.owner_action' inside
            # "owner_view.xml" file  by 'ir.actions.actions' model that found in 'odoo base'

        view_id=self.env.ref('app_one.owner_view_form').id
        print()
        # # ref('app_one.property_view_form')=>built in method using to call form view with id  'app_one.owner_view_form' from
        #     # "owner_view.xml" file
        action['res_id']=self.owner_id.id
        action['views']=[[view_id,'form']] # For calling From view Only
        return action

    #### video (74) Integrate with another app => using Endpoint ############
    def get_properties(self):
        # print("inside get_properties method")
        payload=dict({})
        try:
            response=requests.get("http://localhost:8066//v1/properties",data=payload)
            # "http://localhost:8066//v1/properties" the "endpoint" that will be dealing with it to can access data
            if response.status_code==200:
                print("Successfully")
                print(response) #<Response [200]>
                print(response.content) #for showing Content in this URL(Endpoint)
                print(response.status_code) #for showing status_code in this URL(Endpoint) =>200 in case Successfully
            else:
                print("Fail")
        except Exception as error:
            raise ValidationError(str(error))
    #========== Start Excel Report =============================#
    def property_xlsx_report(self):
        # print("inside property_xlsx_report Method")
        return {
            "type":"ir.actions.act_url",
            "url":f"/property/excel/report/{self.env.context.get('active_ids')}",
            # "{self.env.context.get('active_ids')}" =>meaning Return active Records That "User"
                    # identified it From "Properties" Record
            "target":"new"
        }
    #========== End Excel Report =============================#
########################   class Or Model of Property_Line #####################################################
class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    # area = fields.Float()
    # description = fields.Char()


    area = fields.Integer()
    description = fields.Text()
    price = fields.Float()

    # property2_id = fields.One2many('property', 'line2_id')
    # area = fields.Integer(related='property2_id.living_area')
    # description = fields.Text(related='property2_id.description')
    # price = fields.Float(related='property2_id.selling_price')

    #############################################################
    # @api.model_create_multi
    # def create(self,vals):
    #     # result=super(Property,self).create(vals)
    #     result=super().create(vals)
    #     print("Inside Create  Method") #will show in terminal
    #     return result
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res=super()._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     print("Inside search  Method") #will show in terminal
    #     return res
    # def write(self, vals):
    #     res=super().write(vals)
    #     print("Inside Write  Method")  # will show in terminal
    #     return res
    # def unlink(self):
    #     res=super().unlink()
    #     print("Inside Unlink  Method")  # will show in terminal
    #     return res
