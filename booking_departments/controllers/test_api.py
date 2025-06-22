from odoo import http



class TestApi(http.Controller):

    @http.route("/api/test", type='http', auth='none', methods=['GET'], csrf=False)
    def test_endpoint(self):
        print("Inside test_endpoint method")










# from odoo.exceptions import ValidationError, AccessError, AccessDenied
# from odoo.custom_addons.app_one.controllers.common import invalid_response
# from odoo.http import request, _logger

# class TestApi(http.Controller):
#
#     @http.route("/api/test", type='http', auth='none', methods=['GET'], csrf=False)
#     def test_endpoint(self):
#         print("Inside test_endpoint method")
        # params=['db','login','password']
        # params={key:kwargs.get(key) for key in params if kwargs.get(key)}
        # db,username,password=(
        #     params.get('db'),
        #     kwargs.get('login'),
        #     kwargs.get('password')
        # )
        # _credentials_include_in_body=all([db,username,password])
        # if not _credentials_include_in_body:
        #         headers=request.httprequest.headers
        #         username=headers.get('login')
        #         password=headers.get('password')
        #         db=headers.get('db')
        #         _credentials_include_in_headers=all([db,username,password])
        #         if not _credentials_include_in_headers:
        #             print("Inside test_endpoint method")
        #             return invalid_response(
        #             "Missing Error","Either of the Following is Missing [db,username,password]",403
        #             )
        #             # raise ValidationError("Either of the Following is Missing [db,username,password]")
        #
        # try:
        #     request.session.authenticate(db,username,password)
        # except AccessError as aee:
        #     return invalid_response('Access Error','Error: %s'% aee.name)
        # except AccessDenied as ade:
        #     return invalid_response('Access Denied','Login, password or db invalid')
        # except Exception as e:
        #     info=f'The database name is Not Invalid{e}'
        #     error="Invalid Database"
        #     _logger.error(info)
        #     return invalid_response("Wrong Database name",error,403)
        #
        # uid=request.session.uid
        # if not uid:
        #     info="authentication Failed"
        #     error="authentication Failed"
        #     _logger.error(info)
        #     return invalid_response(401,error,info)


        # return "Inside test_endpoint method"
