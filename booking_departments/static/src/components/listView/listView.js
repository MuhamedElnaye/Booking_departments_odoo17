/* @odoo-module */

import {Component,useState,onWillUnmount} from "@odoo/owl";
// "onWillUnmount" =>this Hook using when we are End the work in this Component and you want to cancel
    // any Operation doing automatically during work this operation
    // EX: this.interval=setInterval(()=>{this.loadRecords()},3000) // meaning  do "this.loadRecords()" function every "3 seconds"
        //onWillUnmount(()=>{clearInterval(this.interval)})
        // Meaning in case "User" closed Or Cancel Component of "this.loadRecords()" cancel all lines or
        //operation inside this function
import {registry} from "@web/core/registry";

import {useService} from "@web/core/utils/hooks";
// "import {useService} from "@web/core/utils/hooks";" => This Line Using Fo Calling "ORM" methods To I can
        // dealing With Records in table "property" that Found in "property.py" [or Any another tables]
        // I can Calling any Records form Any Tables by Using "ORM" methods By this "hooks"

//export class ListViewAction extends Component{ } =>Inheritance Class
export class ListViewAction extends Component{
    static template="app_one.ListView" ;
    // "app_one.ListView" =>its Coming From "listView.xml" File

    // "setup()" =>It Like Constructor
    setup(){
        this.state=useState({
            "records":[]
        });
        // [{"id":1,"name":"property1","postcode":"P1001","data_availability":"16/6/2025"},
        // {"id":2,"name":"property2","postcode":"P1002","data_availability":"16/6/2025"}]
        // "this.records=[{"id":1},{"id":2}]" => this Line connect with "Qweb" templet and doing
            //  "t-foreach="records"" line in "listView.xml" file
        this.orm=useService("orm");// Note :You Must Call it In "setup()" method before using or calling it in any Methods.
        this.rpc=useService("rpc");// Note :You Must Call it In "setup()" method before using or calling it in any Methods.
        this.loadRecords() ;  // Note:You Must Call "loadRecords() " or any Method For Doing it in this App.
        // setInterval(function,time ) =>this Function will repeat doing any (function) every (time) you set it
        // setInterval(()=>{console.log("Test this")},3000)
        this.interval=setInterval(()=>{this.loadRecords()},3000) // meaning  do "this.loadRecords()" function every "3 seconds"
        onWillUnmount(()=>{clearInterval(this.interval)})
        // "onWillUnmount(()=>{clearInterval(this.interval)})" This hook will cancel operation when user Cancel Component.

  };
//============================Start ORM Service ============================================
//    async loadRecords(){
//       const result= await this.orm.searchRead("property",[],[]);
//        // "this.orm.searchRead()"=>this Method using To return "records" and Read "Data" From this Records
//        // "property" => table Name from "property.py" file, [first] =>fields []
//        // "async" and "await"=> For doing Asynchronous programming
//        // "const " => meaning make This Variable const ثابت and can't change it after Showing in Console
//        console.log(result);  // Show this result in console of UI
//        this.state.records =result; // THis Line For Storing(تخزين) "result" =>property record in "records" that Found in
//                     // "setup()"  method
//    };
//============================Start ORM Service ============================================

//============================Start RPC Service ============================================
      async loadRecords(){
            const result= await this.rpc("/web/dataset/call_kw/",
               // In Odoo's web client, "/web/dataset/call_kw " is an "API endpoint" used for calling methods on Python models.
                    //secifically,it's how the web client interacts with
                    //the server-side ORM (Object-Relational Mapper) to perform actions	like creating,reading,
                    //updating, or deleting data
                // "/web/dataset/call_kw/" =>it's a const ثابت endpoint(URL) in Odoo app
                {
                model:"property",// table name in "property.py" file
                method:"search_read", //"search_read" =>THis Function saved in Odoo structure
                args:[[]],//Domain That Will return from table records =>[] empty list meaning all records
                kwargs:{fields:["id","name","postcode","data_availability"]},
                });
            console.log(result);  // Show this result in console of UI
            this.state.records=result; // THis Line For Storing(تخزين) "result" =>property record in "records" that Found in
                    // "setup()"  method.
      };
//=========================== End RPC Service ============================================
//=========================== Start Create record Function ============================================
      async createRecord(){
         await this.rpc("/web/dataset/call_kw/",
              // In Odoo's web client, "/web/dataset/call_kw " is an "API endpoint" used for calling methods on Python models.
                        //secifically,it's how the web client interacts with
                        //the server-side ORM (Object-Relational Mapper) to perform actions	like creating,reading,
                        //updating, or deleting data
                       // "/web/dataset/call_kw/" =>it's a const ثابت endpoint(URL) in Odoo app
                    {
                    model:"property",// table name in "property.py" file
                    method:"create",//"create" =>THis Function saved in Odoo structure
                    args:[{
                        name:"Property OWL Create Function",
                        postcode:"PO1234",
                        data_availability:"2025-6-18"
                    }],
                    kwargs:{},
              });
         this.loadRecords(); //Calling this Function For Update records in view
      };
//=========================== End Create record Function ==============================================
//=========================== start Delete record Function ==============================================
      async deleteRecord(recordID){
          await this.rpc("/web/dataset/call_kw/",{
                    model:"property",
                    method:"unlink",
                    args:[recordID],
                    kwargs:{},
          });
          this.loadRecords(); //Calling this Function For Update records in view

      };
//=========================== End Delete record Function ==============================================

}

registry.category("actions").add("app_one.action_list_view",ListViewAction);

// "app_one.action_list_view" =>this action Found in "listView.xml" File
// "ListViewAction " =>Class name above