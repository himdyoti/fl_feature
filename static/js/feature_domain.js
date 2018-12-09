
var FeatureDomain = function(){
    var self = this;
    self.ID = ko.observable();
    self.area_name = ko.observable();
    self.description = ko.observable();
}

var viewModel = function(data){
    var self = this;
    self.lines = ko.observableArray();
    /*
    $.ajax({ url:'/product_areas', method:'get', async:false, dataType:'json',success:function(data){
        $.each(data, function(inx,v){
           self.lines.push(v);
        });
    }}); */

    if(data.length >0){ 
        $.each(data,function(inx,v){ console.log(v);
            obj = new FeatureDomain();
            obj.ID(v.ID);
            obj.area_name(v.area_name);
            obj.description(v.description);
            self.lines.push(obj);
        });
    }

    self.status_txt = ko.observable();


    self.addLine = function(){
        ftr_dm = new FeatureDomain();
        self.lines.push(ftr_dm);
    };

    self.removeLine = function(line) {  console.log(line.description());       
        indx = self.lines.indexOf(line)
        dm_name = line.area_name();
        if(ajax_remove_ftr_domain(line)){
            self.lines.remove(line);
            self.status_txt(dm_name + " deleted successfully");
        }
        
    };


    self.submitDomain = function(FeatureDomain){
        fd = ko.toJSON(self.lines());
        status = false;
        console.log(fd);
        $.ajax({
            url:'/product_areas',
            type:'post',
            data:JSON.stringify(fd),
            contentType: 'application/json;charset=UTF-8',
            dataType:'json',
            success:function(json){
                status = json['status']
            },
            complete:function(){
               self.status_txt(" updated successfully: "+status); 
            }
        });
    }

}

function apply_binding(data){
    pareaVm = new viewModel(data);
    ko.applyBindings(pareaVm); 
}


function ajax_remove_ftr_domain(line){
    console.log(ko.toJSON(line));
    status=false;
    if (!line.ID())
        return true;

    $.ajax({
        url:'/remove_parea',
        method:'post',
        data:ko.toJSON(line),
        contentType: 'application/json;charset=UTF-8',
        dataType:'json',
        success: function(json){
            status=json['status'];
        },
        error:function(jqXHR){
            status = false;
        }
    });
    return status;
}
