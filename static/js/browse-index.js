$.i18n().then(function(data){
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;

  var browser =new Vue({
    el:"#layout",
    data:{
      categories:[],
    },
    ready:function(){
      var that = this;
      Service.get('UserCategoryService').user_category_update().success(function(result){
            // that.categories = result.categorys;
            alert();
      });
    },
    methods:{

    },
  })
})