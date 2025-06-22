import json
import math #in pagination
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request


#======== Start Response [Valid, invalid] structure ============#
def valid_response(data,status,pagination_info):
    response_body={
        "Message":"Successfully",
        "data":data
    }
    if pagination_info:
        response_body["pagination_info"]=pagination_info
    return request.make_json_response(response_body, status=status)

def invalid_response(error,status):
    response_body={
        "Error":f"there are error Found ' {error}'"
    }
    return request.make_json_response(response_body, status=status)
#======== End Response [Valid, invalid] structure ============#

class PropertyApi(http.Controller):

    #============== Start Creation Using HTTP Type =====================================#
    # @http.route('/v1/property', methods=["POST"], type="http", auth="none", csrf=False)
    # def post_property(self):
    #     # print("Inside post_property Method")
    #
    #     args = request.httprequest.data.decode()
    #     # "args=request.httprequest.data.decode()"=> this line using to calling data from "postman body OR From UI"
    #     # Note : you Must Call "request" From "from odoo.http import request"
    #     vals = json.loads(args)
    #     # "vals=json.loads(args)" =>This Line Using For Convert to "Json data" To "Dictionary data"
    #     # Note : you Must Call "json" From "import json"
    #     # print(vals)
    #
    #     if not vals.get("name"):  # meaning If Name record not Enter Return This Message
    #         return request.make_json_response({
    #             # "request.make_json_response" this using in case we use "type="http"" to response with "json" data
    #             "Message": "Name Is Required!",
    #         }, status=400)
    #
    #     try:
    #         res = request.env['property'].sudo().create(vals)
    #         # "request.env['property']" =>using To can Access "property" table
    #         # "sudo()" =>To can do access by "Suber User" for avoid "authentication" and can access any Thing
    #         # "create(vals)" => Using To can Create 'property' in database that calling "property"
    #         # print(res)
    #
    #         # For Return Response in "Postman"
    #         if res:
    #             return request.make_json_response({
    #                 # "request.make_json_response" this using in case we use "type="http"" to response with "json" data
    #                 "Message": "Property hase Been created Successfully",
    #                 "Id": res.id,
    #                 "Name": res.name
    #             }, status=200)
    #         # This "If" will return Json Message In case This property Are Created
    #     except Exception as error:
    #         return request.make_json_response({
    #             # "request.make_json_response" this using in case we use "type="http"" to response with "json" data
    #             "Message": error,
    #         }, status=400)
    #============== End Creation Using HTTP Type =======================================#

    #============== Start Creation Using HTTP Type Using "SQL Query" =====================================#
    @http.route('/v1/property', methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        # "args=request.httprequest.data.decode()"=> this line using to calling data from "postman body OR From UI"
        # Note : you Must Call "request" From "from odoo.http import request"
        vals = json.loads(args)
        # "vals=json.loads(args)" =>This Line Using For Convert to "Json data" To "Dictionary data"
        # Note : you Must Call "json" From "import json"
        # print(vals)

        if not vals.get("name"):  # meaning If Name record not Enter Return This Message
            return request.make_json_response({
                # "request.make_json_response" this using in case we use "type="http"" to response with "json" data
                "Message": "Name Is Required!",
            }, status=400)

        try:
            cr=request.env.cr
            # "cr=request.env.cr" => this Line For you Can Deal with "Queries"

            #========== Start Static columns and Values ===============#
            # after deleting "translate=True"
            query="""INSERT INTO property(name,postcode) VALUES ('PROPERTY 00 FROM SQL','123455') RETURNING id,name,postcode"""
            # "query" =>SQL Query line
            cr.execute(query)   # For Static Values
            #========== End Static columns and Values ===============#

            #========== Start dynamic  columns and Values From End User ===============#
            # columns =",".join(vals.keys())       # --> name,postcode,.....    # Access all Keys from body in "Postman"
            # values =",".join(["%s"] * len(vals))  # -->  '%s' , '%s',.....   # Access all Values from body in "Postman"

            # # after deleting "translate=True"
            # # convert dictionary from to => json String
            # # for column in vals:
            # #     vals[column]=json.dumps(vals[column])
            #
            # query=f"""INSERT INTO property({columns}) VALUES ({values}) returning id,name,postcode"""
            # # "query" =>SQL Query line
            #
            # cr.execute(query,tuple(vals.values()))
            # # "cr.execute(query)" =>using To can Access Table From SQL Query
            #========== Start dynamic  columns and Values From End User ===============#

            res=cr.fetchone()
            # "res=cr.fetchone()" =>For Calling or Return Data From Query
            # Note: res return as list,
            print(res)  # output => (54, 'PROPERTY 6 FROM SQL', '123455')

            # For Return Response in "Postman"
            if res:
                return request.make_json_response({
                    # "request.make_json_response" this using in case we use "type="http"" to response with "json" data
                    "Message": "Property hase Been created Successfully",
                    "Id": res[0],
                    "Name": res[1],
                    "postcode": res[2]
                }, status=200)
            # This "If" will return Json Message In case This property Are Created
        except Exception as error:
            return request.make_json_response({
                # "request.make_json_response" this using in case we use "type="http"" to response with "json" data
                "Message": error,
            }, status=400)
    #============== End Creation Using HTTP Type Using "SQL Query" =======================================#

    #============== Start Creation Using Json Type =====================================#
    @http.route('/v1/property/json', methods=["POST"], type="json", auth='none', csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        # "args=request.httprequest.data.decode()"=> this line using to calling data from "postman body OR From UI"
        # Note : you Must Call "request" From "from odoo.http import request"
        vals = json.loads(args)
        # "vals=json.loads(args)" =>This Line Using For Convert to "Json data" To "Dictionary data"
        # Note : you Must Call "json" From "import json"
        # print(vals)
        res = request.env['property'].sudo().create(vals)
        # "request.env['property']" =>using To can Access "property" table from database
        # "sudo()" =>To can do access by "Suber User" for avoid "authentication" and can access any Thing
        # "create(vals)" => Using To can Create 'property' in database that calling "property"
        # print(vals)
        # For Return Response in "Postman"
        if res:
            return ({
                # "request.make_json_response" and "status=200", you don't need these For "type="json"
                "Message": "Property hase Been created Successfully"
            })
        # This "If" will return Json Message In case This property Are Created
    #============== End Creation Using Json File =====================================#

    #============== start Doing Update using Put =====================================#
    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth='none', csrf=False)
    # <int:property_id >  =>For Making "ID" automatic ID and you can chang it as you like
    def update_property(self, property_id):
        try:
            property_id = request.env["property"].sudo().search([("id", "=", property_id)])
            if not property_id:
                return request.make_json_response({
                    "Message": "This ID Not Existed"
                }, status=400)
            # "request.env['property']" =>using To can Access "property" table from database
            # "sudo()" =>To can do access by "Suber User" for avoid "authentication" and can access any Thing
            # search([("id","=",property_id)]) =>For Searching About the ID
            print(property_id)

            args = request.httprequest.data.decode()
            args = request.httprequest.data.decode()
            # "args=request.httprequest.data.decode()"=> this line using to calling data from "postman body OR From UI"
            # Note : you Must Call "request" From "from odoo.http import request"

            vals = json.loads(args)
            # "vals=json.loads(args)" =>This Line Using For Convert to "Json data" To "Dictionary data"
            # Note : you Must Call "json" From "import json"
            print(vals)

            # Doing Update For This Data
            property_id.write(vals)
            # Write( vals) =>meaning Do Update For this data(bedrooms in Odoo UI) and database
            print(property_id.bedrooms)

            # Response For End User
            return request.make_json_response({
                # "request.make_json_response" this using in case we use "type="http"" to response with "json" data
                "Message": "Property hase Been Updated Successfully",
                "ID": property_id.id,
                "Name": property_id.name,
                "Bedrooms": property_id.bedrooms
            }, status=200)  # status=200 =>status Must be 200 in case update
        except Exception as error:
            return request.make_json_response({
                "Message": f"there are error Found ' {error}'",
            }, status=400)
    #============== End Doing Update using Put =====================================#

    #============== Start Doing Read using Get =====================================#
    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def read_property(self, property_id):
        try:
            property_id = request.env["property"].sudo().search([("id", '=', property_id)])
            if not property_id:
                # return request.make_json_response({
                #     "Error": "This ID Not Existed"
                # }, status=400)
                # ==== Tests invalid response structure ==========#
                return invalid_response("This ID Not Existed", status=400)
            return valid_response({
                "ID": property_id.id,
                "Name": property_id.name,
                "postcode": property_id.postcode,
                "Bedrooms": property_id.bedrooms,
                "ref": property_id.ref,
                "description": property_id.description,
                "owner_Name": property_id.owner_id.name,
                "owner_Phone": property_id.owner_id.phone,
                "grand_orientation": property_id.grand_orientation,
            },status=200)
        except Exception as error:
            return request.make_json_response({
                "Error": f"there are error Found ' {error}'"
            }, status=400)
    #============== End Doing Read using Get =====================================#

    #============== start Doing Delete using DELETE  =====================================#
    @http.route("/v1/property/<int:property_id>",methods=["DELETE"],type="http",auth="none",csrf=False)
    def delete_property(self,property_id):
        try:
            property_id=request.env['property'].sudo().search([('id',"=",property_id)])
            if not property_id:
                return request.make_json_response({
                    "Error": "This ID Not Existed"
                },status=400)
            property_id.unlink() # For Deleting Property
            return request.make_json_response({
                "Message": "Property hase Been Deleted Successfully",
            },status=200)
        except Exception as error:
            return request.make_json_response({
                "Error":f"there are error Found ' {error}'"
            },status=400)
    #============== End Doing Delete using DELETE  =====================================#

    #============== Start Doing Read using Get For List =====================================#
    @http.route("/v1/properties", methods=["GET"], type="http", auth="none", csrf=False)
    def read_property_list(self):
        try:

            #================================== start Filtration==========================================#
            # For doing Filtration about something you want To return
            # Note :you must be calling "parse_qs" from "from urllib.parse import parse_qs"
            # "parse_qs" for Can deal with "params" in third part "Postman" app
            # "params" that found in "Postman"
            params=parse_qs(request.httprequest.query_string.decode("utf-8"))
            # print(params)
            property_domain=[] #will return all domains [sold,draft,closed,pending]
            if params.get("state"): #get params with "state"
                property_domain+=[("state","=",params.get("state")[0])]
                # property_domain+=[("state","=",params.get("state")[0])] =>will specify نحدد "property_domain" that
                    # must be the like "key and value" that found in"params"
                    # params.get("state")[0] =>[0] we write This As its list [0,1,2,3]
            # print(property_domain)

            #================================= start Pagination ===========================================#
            # ==start Making "page or(offset)" and "limit" dynamic and taking from user ====#
            page=offset=None
            limit=5
            if params:
                if params.get("page"):  # get params with "page" offset
                    # print(params.get("page"))
                     page=int(params.get("page")[0])

                if params.get("limit"):  # get params with "limit" number OF Record
                    # print(params.get("limit"))
                   limit=int(params.get("limit")[0])
            if page:
                offset=(page*limit) - limit  # for Count the offset of this page [page=3,limit=4] then offset =8

            print(offset)
            print(page)
            print(limit)
            # ==End Making "page or(offset)" and "limit" dynamic and taking from user ====#

            property_ids = request.env["property"].sudo().search(property_domain,offset=offset,limit=limit,order="id desc")
            # offset=50 =>meaning start from "property " number 50
            # offset=3 =>meaning start from "property " number 3
            # order="id desc" =>default(asc تصاعدي) meaning order "property list" by "ID" "desc" تنازلي لكي يعرض الاحدث اولا
            # limit=3 =>meaning number of records that should be return
            print(property_ids)
            property_count = request.env["property"].sudo().search_count(property_domain)
            #"search_count" =>using to count number of records in "property" table
            print(property_count) # output =>26
            #================================= End  Pagination ===========================================#

            #==================================== End Filtration ===========================================#

            # property_ids = request.env["property"].sudo().search([])
            # [] For Calling All record in property table
            if not property_ids:
                # return request.make_json_response({
                #     "Error": "Empty Properties"
                # }, status=400)

                # ==== Tests invalid response structure ==========#
                return invalid_response("Empty Properties", status=400)
            # return request.make_json_response([{
            #     "ID": property_id.id,
            #     "Name": property_id.name,
            #     "State": property_id.state,
            # }for property_id in property_ids],status=200)
            # "[{"ID": property_id.id,"Name": property_id.name,}for property_id in property_ids]" => this Line return all records in property table

            #==== Tests valid response structure ==========#
            return valid_response([{
                "ID": property_id.id,
                "Name": property_id.name,
                "State": property_id.state,
            } for property_id in property_ids],pagination_info={
                "page":page if page else 1,
                "Limit":limit,
                "Pages":math.ceil(property_count/limit) if limit else 1,
                # import math you must import this
                # ceil =>to do integer number for the above number in case float number 7.1 => 8 pages or 7.5=>8 pages
                "Count":property_count
            }, status=200)

        except Exception as error:
            # return request.make_json_response({
            #     "Error": f"there are error Found ' {error}'"
            # }, status=400)
            #==== Tests invalid response structure ==========#
            return invalid_response( f"there are error Found ' {error}'",status=400)
    #============== End Doing Read using Get For List =====================================#
