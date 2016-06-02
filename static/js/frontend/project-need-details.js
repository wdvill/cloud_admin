$.i18n().then().function(data){
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;
  var projectDetail = new vue({
    el:"#body",
    data:{

    },
    ready:function(){
      
    },
  })
}