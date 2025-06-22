# import datetime
# import json
# import werkzeug

# def invalid_response(typ,message='None',status=401):
#     return werkzeug.wrappers.Response(
#         status=status,
#         content_type='application/json;charset=utf-8',
#         response=json.dump(
#             {"type":typ,'message':str(message) if str(message) else "Wrong Argument(Missing Validation)",},
#             default=datetime.datetime.isoformat,
#         ),
#     )