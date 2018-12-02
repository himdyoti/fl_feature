
    var Client = function(){
        var self = this;
        self.client_id = ko.observable();
        self.firstname = ko.observable();
        self.lastname = ko.observable();
        self.email = ko.observable();
        self.password = ko.observable();
        self.phone = ko.observable();
        self.address = ko.observable();
        self.url_ftr = ko.observable();
        self.client_url = ko.observable();
    }

    var ClientVM = function(all_clients){
        var self = this;
        self.close_mod = function(){
            $("#client_form").hide();
        };
        self.url_getftrs = function(client){ console.log(client);
            return "/get_feature_request?cid=" + client.client_id ;
        };


        var cl_attr_setter = function(obj, cl){
            obj.client_id(cl.ID);
            obj.firstname(cl.firstname);
            obj.lastname(cl.lastname);
            obj.email(cl.email);
            obj.password(cl.password);
            obj.phone(cl.phone);
            obj.address(cl.address);
            obj.url_ftr("/get_feature_request?cid=" + cl.ID);
            obj.client_url("/getclient?cid=" + cl.ID);
            return obj;            
        };

        self.clients = ko.observableArray();
        self.slctd_client = ko.observable();

        $.each(all_clients, function(indx,cl){
            obj = new Client();
            obj = cl_attr_setter(obj,cl);
            self.clients.push(obj);
        });


        self.getclient = function(client){
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
                        self.slctd_client = client;
                        $("#client_form").show();
                    }
                }
            });
            console.log(self.slctd_client.firstname());
        };


    }
    function apply_client_binding(all_clients){
        cvm = new ClientVM(all_clients);
        ko.applyBindings(cvm); 
    }
    
