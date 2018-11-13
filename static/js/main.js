var VM = {};
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
    self.oldval = false;
    self.priority.subscribe(function(preval){
        self.oldval = preval;
    },null,'beforeChange');

    self.priority.subscribe(function(newval){
        sort_priority(newval,self.oldval);
    });
}



var viewModel = function(data){ 
    var self = this;
    var tempobj= {ID:'', Description: "spelling and grammer", Title:"spelling", client_id: 18, firstname:"abc", area_name:"grammer", priority: 1,target_date: "Thu, 29 Nov 2018 00:00:00 GMT" };

    self.lines = ko.observableArray();
    $.each(data,function(inx,val){
        self.lines.push(new FeatureOne(val));
    });

    $.ajax({ url:'/get_product_areas', method:'get', dataType:'json',success:function(data){
        console.log(data);
    }});

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
    VM = new viewModel(data)
    ko.applyBindings(VM);
}

function sort_priority(n,o){
    console.log(n,o);
    if(Math.abs(n-o) == 1){
    for (i=0;i<VM.lines().length;i++){
        if(VM.lines()[i].priority() == n && VM.lines()[i].oldval != o )
             VM.lines()[i].priority(o);
         else
            VM.lines()[i].oldval = false;
    }
    }
//pull start from prio(n) downward upto prio(o) when prion(n) >> prio(o) change elem will sit to prio(n)
//or lift upward prio(n) upto prio(o) when prio(n) << prio(o), changed elem will sit at prio(n)
//priority no decreased means ranking improved

    else if(Math.abs(n-o) > 1){ 
     for (i=0;i<VM.lines().length;i++){
        if(VM.lines()[i].priority() == n && VM.lines()[i].oldval != o )
             VM.lines()[i].priority(o);
         else
            VM.lines()[i].oldval = false;       
    }
    }

    VM.lines = VM.lines.sort(function (left, right) { return left.priority() < right.priority() ? -1 : 1 })

}