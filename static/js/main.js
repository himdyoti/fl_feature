var FeatureOne = function(data){
    var self = this;
    self.ID = ko.observable(data.ID);
    self.Title = ko.observable(data.Title);
    self.client_id = ko.observable(data.client_id);
    self.firstname = ko.observable(data.firstname);
    self.Description = ko.observable(data.Description);
    self.priority = ko.observable(data.priority);
    self.target_date = ko.observable(data.target_date);
    self.area_name = ko.observable(data.area_name);
};

var ClientFeature = function(data){ 
    var self = this;
    var tempobj= {ID:'', Description: "spelling and grammer", Title:"spelling", client_id: 18, firstname:"abc", area_name:"grammer", priority: 1,target_date: "Thu, 29 Nov 2018 00:00:00 GMT" };

    self.lines = ko.observableArray();
    $.each(data,function(inx,val){ console.log(val);
        self.lines.push(new FeatureOne(val));
    }); 

    self.addLine = function(){self.lines.push(new FeatureOne(tempobj))};
    self.removeLine = function(line) { self.lines.remove(line) };
    self.save = function(){
        var existing = [], new_added = [];
        $.each(self.lines, function(indx,line){
            feature_one = {'ID':line.ID(),'Title':line.Title(),'Description':line.Description(), 'priority':line.priority(), 'target_date':line.target_date(), 'area_name':line.area_name()};
            if(line.id()){
                exising.push(feature_one);
            }else{
                new_added.push(feature_one);
            }

        });
        var urls=['edit_feature','add_feature'];
        $(urls).each(function(indx,url){
            data = url == 'add_feature' ? new_added : existing;
            if(data.length)
             $.ajax({
                url: '/' + url,
                method: 'post',
                data: {'data':existing},
                success: function(){console.log("updated")}
            });            

        });


    };

};

function apply_binding(data){
    ko.applyBindings(new ClientFeature(data));
}