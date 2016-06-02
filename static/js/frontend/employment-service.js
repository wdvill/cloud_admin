 $.i18n().then(function(data){
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;

  var creatClient = new Vue({
    el:"#body",
    data:{
      favorites:[],
    },
    ready:function(){
      var that = this;
      Service.get('WorkService').collect_list().success(function(result){
        that.favorites = result.favorites;
      });
    },
    methods:{

    },
  })

})