var VM = {};
var FeatureOne = function(){
    var self = this;
    self.ID = ko.observable();
    self.Title = ko.observable();
    self.client_id = ko.observable();
    self.Description = ko.observable();
    self.priority = ko.observable();
    self.target_date = ko.observable();
    self.area_name = ko.observable();
    self.product_area_id = ko.observable();
    self.product_area_id.subscribe(function(nv){
        if(nv && !isNaN(parseInt(nv))){
            self.product_area_id(nv);
        }
        else
        console.log("not ...");
    });
    self

}



var viewModel = function(data, client_id){
    var self = this;
    self.lines = ko.observableArray();
    self.sort1 = function(){
        self.lines.sort(function (left, right) { return left.priority() == right.priority() ? 0 : (left.priority() < right.priority() ? -1 : 1) }) ;
    };

    self.selectbox = ko.observableArray();
    self.select_pa = ko.observableArray();

    if(data.length >0){ 
        $.each(data,function(inx,v){ 
            date_compute(v.target_date);
            obj = new FeatureOne();
            obj.ID(v.ID);
            obj.Title(v.Title);
            obj.client_id(v.client_id);
            obj.Description(v.Description);
            obj.priority(v.priority);
            obj.target_date(date_compute(v.target_date));
            obj.area_name(v.area_name);
            obj.product_area_id(v.product_area_id); console.log(obj.target_date());
            self.lines.push(obj);
            self.selectbox.push(obj.priority());
        });
    }
    self.sort1();

    $.ajax({ url:'/get_product_areas', method:'get', dataType:'json',success:function(data){
        $.each(data, function(inx,v){console.log(v);
           self.select_pa.push(v);
        });
    }});

    self.addLine = function(){
        ftr_one = new FeatureOne();
        ftr_one.client_id(client_id);
        len1 = self.lines().length ;
        ftr_one.priority(len1 + 1);
        self.lines.push(ftr_one);
        self.selectbox.push(len1 + 1);
    };
    
    self.removeLine = function(line) {
        if(line == self.lines()[self.lines.length - 1]){
            if(ajax_remove_feature(line))
                self.lines.remove(line);
        }   
        else{
            indx = self.lines.indexOf(line)
            for(i=self.lines().length - 1; i>indx ; i--){
                self.lines()[i].priority(self.lines()[i].priority() - 1);
            }
            if(ajax_remove_feature(line))
                self.lines.remove(line);
        }
    };


    self.save = function(){
        dts = ko.toJSON(self.lines());
        console.log(dts);
        console.log(JSON.parse(dts));
        //dts = dts.replace(/^(\[)(.*)(\])$/,"{$2}");
        //console.log(dts);
        
        $.ajax({
            url:'/update_feature_request',
            type:'post',
            data:JSON.stringify(dts),
            contentType: 'application/json;charset=UTF-8',
            success:function(){
                alert("features updated successfully");
            }
        });
        /*
        var existing = [], new_added = [];
        $.each(self.lines(), function(indx,line){
            feature_one = {'ID':line.ID(),'Title':line.Title(),'Description':line.Description(), 'priority':line.priority(), 'target_date':line.target_date(), 'area_name':line.area_name()};
            if(line.ID()){
                existing.push(JSON.stringify(feature_one));
            }else{
                new_added.push(JSON.stringify(feature_one));
            }

        });
        
        var urls=['edit_feature_request','add_feature_request'];
        $(urls).each(function(indx,turl){
            post_data = (turl == 'add_feature_request') ? new_added : existing;
            if(post_data.length){
                console.log('/'+turl);
             $.ajax({
                url: '/' + turl,
                method: 'post',
                async:true,
                data: {'ftrs_data':JSON.stringify(post_data)},
                contentType: 'application/json;charset=UTF-8',
                dataType:'json',
                success: function(json){console.log(json);},
                error: function (jqXHR, exception) {console.log(jqXHR.responseText);console.log(exception)}
            });
            }            

        }); */

    };

};

function apply_binding(data,client_id){
    VM = new viewModel(data,client_id);
    ko.applyBindings(VM);
}


$('tbody').on('change','.pr_opt',function(){
    tobe = parseInt(this.value); //n
    if(isNaN(tobe))
        return;
    curr = parseInt($(this).prev().val()); //p
    console.log(tobe, curr);
    ftrs = VM.lines;
    celem = ftrs()[curr -1];
    celem.priority(tobe);
    if(Math.abs(tobe-curr) ==1){
       ftrs()[tobe -1].priority(curr) ;
    }
    if ((curr-tobe)>1){ //curr=5, tobe=2
        while(tobe<curr){ //2 < 5
            pr = ftrs()[tobe-1].priority();
            ftrs()[tobe-1].priority(pr+1);
            tobe = tobe +1; 
        }
        ftrs.remove(ftrs()[curr-1]);
        ftrs.splice(tobe -1,0,celem);

    }
    if((tobe - curr) > 1){ cpos = curr;//curr = 2, tobe=5
        while(tobe > curr){
            pr = ftrs()[curr].priority();
            ftrs()[curr].priority(pr-1);
            curr = curr +1;           
        }
        ftrs.remove(ftrs()[cpos-1]);
        ftrs.splice(tobe -1,0,celem);
    }
    VM.sort1();
});



function ajax_remove_feature(line){
    status=false;
    if (!line.ID())
        return true;

    $.ajax({
        url:'/remove_feature_request',
        method:'post',
        data:{'feature':ko.toJSON(line)},
        success: function(){
            status=true;
        },
        error:function(jqXHR){
            status = false;
        }
    });
    return status;
}

function date_compute(dts){ 

    dt = new Date(dts);
    mm = dt.getMonth() + 1;
    mm = mm < 10 ? '0'+ mm : mm ;
    dd = dt.getDate() < 10 ? '0'+ dt.getDate():dt.getDate();
    yyyy = dt.getFullYear();
    ft_date = yyyy + "-" + mm + "-" + dd  ;
    return ft_date;

}




