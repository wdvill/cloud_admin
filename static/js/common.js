(function(plug){
  plug.getParameterByName = function(name, url){
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
  };
  plug.i18n = function(){
    var lang = Cookies.get("_lang");
    if(!lang){
      lang = (navigator.language || navigator.browserLanguage).toLowerCase();
      if(lang == "zh-cn"){
        var p = "/static/locale/locale-zh-cn.json";
      }else{
        var p = "/static/locale/locale-en.json";
      }
      return this.getJSON(p);
    }
  };
})(jQuery);


(function($){
  $.get_year_list = function(begin, end){
    var year_list = [];
    if(!begin){
      begin = 1949;
    }
    if(!end){
      end = 2016;
    }
    for(var i=end; i>=begin; i--){
      year_list.push({'text': i.toString(), 'value': i.toString()});
    }
    return year_list;
  };

  $.get_month_list = function(){
    var month_list = [];
    for(var i=1; i<=12; i++){
      var j = i.toString();
      if(j.length == 1){
        j = '0' + j
      }
      month_list.push({'text': j, 'value': j})
    }
    return month_list;
  };
})(jQuery);
