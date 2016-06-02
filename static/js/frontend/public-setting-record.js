Vue.config.delimiters = ['{[', ']}'];

var obj = new Vue({
  el:"#layout",
  data:{
    parent_categories:[],
    one_categories:[],
    two_categories:[],
    three_categories:[],
    four_categories:[],
    skills:[],
    parentSkills:[],
    skills_selected:[],
    num:0
  },
  ready:function(){
    _self=this;
    $.i18n().then(function(data){
        window['CODE'] = data.CODE;
        window['COMMONS'] = data.COMMONS;
      $.ajax({
          type: "get",
          url: "/api/user/category",
          cache: false,
          dataType: "json",
          //async:false,
          data: {
            _xsrf: Cookies.get("_xsrf")
          },
          success: function (json) {
            if(json.error_code == 0){
              var parent_ids="";
              for(var i=0; i<json.categorys.length; i++){
                if(parent_ids.indexOf(json.categorys[i].parent_id)==-1){
                  parent_ids+=json.categorys[i].parent_id;
                 _self.parentSkills.push({"pname":json.categorys[i].parent_name, "pid":json.categorys[i].parent_id});
                }
                _self.skills.push({"pid":json.categorys[i].parent_id,"name":json.categorys[i].name, "category_id":json.categorys[i].category_id});
              }
              console.log(_self.skills)
            }else{
              alert(CODE[json.error_code]);
            }
          }
        });

      $.ajax({
        type: "post",
          url: "/api/category",
          cache: false,
          dataType: "json",
          //async:false,
          data: {
            t: "all",
            category_id: 0,
            _xsrf: Cookies.get("_xsrf")
          },   
          success: function (json) {
            if(json.error_code == 0){ 
              var arr = [],arr1 = [],arr2 = [],arr3 = [],arr4 = []; 
              for(var i=0; i<json.categorys.length; i++){
                //json.categorys[i].name = COMMONS[json.categorys[i].name];
                var cid = json.categorys[i].category_id;
                var cname = json.categorys[i].name;
                if(json.categorys[i].pid == 0){ 
                  arr.push({"name":cname, "category_id":cid});
                }else if(json.categorys[i].pid == 1){
                  arr1.push({"name":cname, "category_id":cid});
                }else if(json.categorys[i].pid == 2){
                  arr2.push({"name":cname, "category_id":cid});
                }else if(json.categorys[i].pid == 3){
                  arr3.push({"name":cname, "category_id":cid});
                }else{
                  arr4.push({"name":cname, "category_id":cid});
                }    
              }  
              _self.parent_categories = arr;_self.one_categories=arr1;
              _self.two_categories=arr2;_self.three_categories=arr3;_self.four_categories=arr4;
            }else{
              alert(CODE[json.error_code]);
            }
          }   
      });



      });
  },  
  methods:{
    cateCheck:function(){
      if(this.num==0){
        for(var i=0;i<this.skills.length;i++){
          $("#cate-" + this.skills[i].category_id).click();
        }
        this.num=this.num+1
      } 
    },
    change_level:function(level){
      $.ajax({
        type: "POST",
        url: "/api/user/resume",
        dataType: "json",
        data: {
          "_xsrf":Cookies.get("_xsrf"),
          "level":level
        },
        success: function(json){
          if(json.error_code == 0){ 
            location.reload();
          }else{
            alert(CODE[json.error_code]);
          }
        }
      });
    },
    update_user_category:function(){
      var _category = "";
      $('input[type=checkbox]:checked').each(function(){
        _category+=$(this).val()+",";
      });
      $.ajax({
        type: "PUT",
        url: "/api/user/category",
        dataType: "json",
        data: {
          "category":_category.substring(0,_category.length-1),
          "_xsrf":Cookies.get("_xsrf")
        },
        success: function(json){
          if(json.error_code == 0){ 
            location.reload();
          }else{
            alert(CODE[json.error_code]);
          }
        }
      });
    }
  },
  watch:{
    skills_selected: function(val,oldval){
      if(val.length >= 10){
        $('#modal-cate input[type=checkbox]').not("input:checked").attr('disabled',true)
      }else{
        $('#modal-cate input[type=checkbox]').not("input:checked").attr('disabled',false)
      }
    }
  }
});

