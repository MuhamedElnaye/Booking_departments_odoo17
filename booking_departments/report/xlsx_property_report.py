from ast import literal_eval

from odoo import http
from odoo.http import request
import io
import xlsxwriter  # Library for Doing Excel Sheet

class XlsxPropertyReport(http.Controller):

    @http.route("/property/excel/report/<string:property_ids>",type="http",auth='user')
    # "<string:property_ids>" =>For Calling Record ids "property_ids" [Note there Are Two type Only (int,string)]

    # auth='user' =>Meaning the user that "Do loging" that Can Do this Action or report
    def download_property_excel_report(self,property_ids):

        print(property_ids) # print it As "String" [1,2,3,4,..] => And You Must Change It To "List"
        property_ids=request.env["property"].browse(literal_eval(property_ids))
        print(property_ids) # print it As "List"  property(1,2,3,4,...)
        # "browse(literal_eval(property_ids))" =>Using For Return "Properties record data"
        # "literal_eval(property_ids)" this Method Using To Convert "string" To "List"
                # [Note : "You Must call 'literal_eval' From 'from ast import literal_eval'"]

        output=io.BytesIO()
        # "output" =>This File saved in "Temporary Memory ذاكر موقته" For Saving reports to Download its.

        workbook=xlsxwriter.Workbook(output,{"in_memory":True})
        # "workbook" =>Workbook that I will do in it "Excel report File"
        # "{"in_memory":True}" =For Doing Save this file In Memory

        worksheet=workbook.add_worksheet("Properties")
        # "worksheet" => Meaning Do "worksheet ورقة عمل calling  'Properties'" in File "workbook ملف اكسيل

        #========= start Calling Tabel Header Names from property database =================================================#
        header_format=workbook.add_format({'bold':True,'bg_color':'#D3D3D3','border':1,'align':'center'})
        # "header_format" =>For Handling "Table" Header Format

        headers=['Name','Postcode','Selling Price','Garden Area']
        # headers =>table header name

        for col_num,header in enumerate(headers):
            worksheet.write(4,col_num+5,header,header_format)
            # "enumerate(headers)" =>'enumerate' => meaning return "headers"
               # [index Number of this Value, and Value of This index] EX:return 1-[0,"Name"], 1-[1,"Postcode"],..
            # worksheet.write(row_num,col_num,header,header_format)
            # "row_num" => Row الصفNumber that start from It In Worksheet =>For Doing It Dynamic "Rew"
            # "col_num" => column العمود Number that start from It In Worksheet =>For Doing It Dynamic "Column"
            # "header" => header[0] =>Name ,header[1] =>Postcode from "For loop" =>For Doing It Dynamic "Name"
            # "header_format" => header Format That Will tak it This Header
        #========= End Calling Tabel Header Names from property database =================================================#

        #========= Start Calling Tabel Data values from property database=================================================#
        string_format=workbook.add_format({'border':1,'align':'center'})
        price_format=workbook.add_format({"num_format":"$##,##00.00",'border':1,'align':'center'})
        # ""num_format":"$##,##.00"" => Format Of Price that will Show [1000,12.12]

        row_num=5
        col_num=5
        for property in property_ids:
            worksheet.write(row_num,col_num,property.name,string_format)
            worksheet.write(row_num,col_num+1,property.postcode,string_format)
            worksheet.write(row_num,col_num+2,property.selling_price,price_format)
            worksheet.write(row_num,col_num+3,"YES" if property.garden_area else "NO",string_format)
            row_num+=1

        #========= End Calling Tabel Data values from property database ===================================================#

        workbook.close()  # Meaning Close This File
        output.seek(0)    # Meaning read This File From Start "البداية"


        #========= Start Saving File  =================================================#
        file_name="Property Report.xlsx"  # "Excel file 'name'" that will be Created.
        return request.make_response(
            output.getvalue(),  # Return Values Of This File That Saved
            headers=[
                ("Content-type","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                ("Content-Disposition",f"attachment;filename={file_name}")
                ]
        )
        #========= End Saving File ====================================================#



