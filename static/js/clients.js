
    var Client = function(){
        var self = this;
        self.client_id = ko.observable();
        self.firstname = ko.observable();
        self.lastname = ko.observable();
        self.email = ko.observable();
        self.username = ko.observable();
        self.password = ko.observable();
        self.phone = ko.observable();
        self.address = ko.observable();
        self.state = ko.observable();
        self.country = ko.observable();
        self.zipcode = ko.observable();
        self.url_ftr = ko.observable();
        self.client_url = ko.observable();
    }

    var ClientVM = function(all_clients){
        var self = this;
        self.close_mod = function(){
            $("#client_form").hide();
        };
        self.url_getftrs = function(client){
            return "/get_feature_request?cid=" + client.client_id ;
        };


        var cl_attr_setter = function(obj, cl){
            obj.client_id(cl.ID);
            obj.firstname(cl.firstname);
            obj.lastname(cl.lastname);
            obj.email(cl.email);
            obj.username(cl.username);
            obj.password(cl.password);
            obj.phone(cl.telephone);
            obj.address(cl.address);
            obj.state(cl.state);
            obj.country(cl.country);
            obj.zipcode (cl.zipcode);
            obj.url_ftr("/get_feature_request?cid=" + cl.ID);
            obj.client_url("/getclient?cid=" + cl.ID);
            return obj;            
        };

        self.clients = ko.observableArray();
        self.slctd_client = ko.observable();
        self.add_edit_txt = ko.observable("Add Client");

        $.each(all_clients, function(indx,cl){
            obj = new Client();
            obj = cl_attr_setter(obj,cl);
            self.clients.push(obj);
        });


        self.getclient = function(client){
            if(client.client_id && client) {
            $.ajax({
                url:"/getclient?cid=" + client.client_id() + "&ajxReq=1",
                type:'get',
                dataType:'json',
                success:function(json){
                    console.log(json);
                    if(json){
                        client_db = json[0];
                        cl_indx = self.clients().indexOf(client);
                        client = cl_attr_setter(client,client_db);
                        self.slctd_client(client);
                        self.add_edit_txt("Edit "+client.firstname()+" "+client.lastname()+"'s Profile");
                    }
                },
                complete:function(){
                    $("#client_form").show();                   
                }
            });
            }
            else{
                self.slctd_client(new Client());
                $("#client_form").show();                
            }

        };

        self.kojson = function(client){

        };


        self.submitClient = function(client){
            cl = ko.toJSON(client);
            console.log(cl);
            $.ajax({
                url:'/addclient',
                type:'post',
                data:cl,
                contentType: 'application/json;charset=UTF-8',
                dataType:'json',
                success:function(json){ console.log(json);
                   if(typeof(json['client_id'] !="undefined") && json['client_id']){
                        if(client.client_id !="undefined" && json['client_id'] == client.client_id()){
                            alert("client edited successfully");
                        }
                        else{
                            client.client_id(json['client_id']);
                            client.url_ftr("/get_feature_request?cid=" + json['client_id']);
                            obj.client_url("/getclient?cid=" + json['client_id']);
                            self.clients.push(client);
                            alert("client added successfully");
                        }
                    }
                },
                complete:function(){

                }
            });
        }


    }
    function apply_client_binding(all_clients){
        cvm = new ClientVM(all_clients);
        ko.applyBindings(cvm); 
    }
    
