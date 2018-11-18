var VM = {};
var FeatureOne = function(){
    var self = this;
    self.ID = ko.observable();
    self.Title = ko.observable();
    self.client_id = ko.observable();
    self.firstname = ko.observable();
    self.Description = ko.observable();
    self.priority = ko.observable();
    self.target_date = ko.observable();
    self.area_name = ko.observable();

}



var viewModel = function(data, cl_id){ 
    var self = this;
    self.lines = ko.observableArray();
    self.sort1 = function(){
        self.lines.sort(function (left, right) { return left.priority() == right.priority() ? 0 : (left.priority() < right.priority() ? -1 : 1) }) ;
    };
    self.selectbox = ko.observableArray();

    $.each(data,function(inx,v){
        obj = new FeatureOne();
        obj.ID(v.ID); obj.Title(v.Title); obj.client_id(v.client_id);
        obj.firstname(v.firstname);obj.Description(v.Description);
        obj.priority(v.priority);obj.target_date(v.target_date); obj.area_name(v.area_name);
        self.lines.push(obj);
        self.selectbox.push(obj.priority());
    });
    self.sort1();

    $.ajax({ url:'/get_product_areas', method:'get', dataType:'json',success:function(data){
        console.log(data);
    }});

    self.addLine = function(){
        ftr_one = new FeatureOne();
        ftr_one.client_id(cl_id);
        len1 = self.lines().length ; console.log(len1);
        ftr_one.priority(len1 + 1);
        self.lines.push(ftr_one);
        self.selectbox.push(len1 + 1);
    };
    self.removeLine = function(line) {
        // selectbox remove item by priority 
        self.lines.remove(line)
        //sort lines 
    };
    self.save = function(){
        var existing = [], new_added = [];
        $.each(self.lines(), function(indx,line){ console.log(line);
            feature_one = {'ID':line.ID(),'Title':line.Title(),'Description':line.Description(), 'priority':line.priority(), 'target_date':line.target_date(), 'area_name':line.area_name()};
            if(line.ID()){
                existing.push(feature_one);
            }else{
                new_added.push(feature_one);
            }

        });
        
        var urls=['edit_feature','add_feature'];
        $(urls).each(function(indx,url){
            post_data = url == 'add_feature' ? new_added : existing;
            if(post_data.length)
             $.ajax({
                url: '/' + url,
                method: 'post',
                async:false,
                data: {'ftrs_data':post_data},
                success: function(){console.log("updated")}
            });            

        });
        


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
        while(tobe > curr){ console.log(ftrs()[curr]);
            pr = ftrs()[curr].priority();
            ftrs()[curr].priority(pr-1);
            curr = curr +1;           
        }
        ftrs.remove(ftrs()[cpos-1]);
        ftrs.splice(tobe -1,0,celem);
    }
    VM.sort1();
});




