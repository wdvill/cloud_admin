$.i18n().then(function(data){
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;

  var browser_index =new Vue({
    el:"#body",
    data:{
      parent_categories:[],
      one_categories:[],
      two_categories:[],
      three_categories:[],
      four_categories:[],
      skills:[],
      parentSkills:[]
    },
    ready:function(){
      var _self = this;
      Service.get('UserCategoryService').get_category({category_id:0,t:'all'}).success(function(json){

        if(json.error_code == 0){ 
          var arr = [],arr1 = [],arr2 = [],arr3 = [],arr4 = []; 
          for(var i=0; i<json.categorys.length; i++){
                var cid = json.categorys[i].category_id;
                var cname = json.categorys[i].name;
                var pid = json.categorys[i].pid;
                if(json.categorys[i].pid == 0){ 
                  arr.push({"name":cname, pid: pid, "category_id":cid});
                }else if(json.categorys[i].pid == 1){
                  arr1.push({"name":cname, pid: pid, "category_id":cid});
                }else if(json.categorys[i].pid == 2){
                  arr2.push({"name":cname, pid: pid, "category_id":cid});
                }else if(json.categorys[i].pid == 3){
                  arr3.push({"name":cname, pid: pid, "category_id":cid});
                }else{
                  arr4.push({"name":cname, "category_id":cid});
                }    
              }  
              _self.parent_categories = arr;_self.one_categories=arr1;
              _self.two_categories=arr2;_self.three_categories=arr3;_self.four_categories=arr4;
            }else{
              alert(CODE[json.error_code]);
            }

      });
    },
    methods:{

    },
  })
})