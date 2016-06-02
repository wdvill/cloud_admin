var jcrop_api, boundx, boundy,profile;
$(document).ready(function(){
  $("#photo").change(function(){
    var file = this.files[0];
    if(file.size > 1024 * 1024 * 5){
      alert("图片不能超过5M");
      return;
    }
    var objUrl = getObjectURL(this.files[0]) ;
    if(objUrl) {
      $("#sourceImg").attr("src", objUrl) ;
      $("#cutImg").attr("src", objUrl) ;
      jcrop_api.setImage(objUrl);
    }
  });
  function getObjectURL(file) {
    var url = null ;
    if (window.createObjectURL!=undefined) { // basic
      url = window.createObjectURL(file) ;
    } else if (window.URL!=undefined) { // mozilla(firefox)
      url = window.URL.createObjectURL(file) ;
    } else if (window.webkitURL!=undefined) { // webkit or chrome
      url = window.webkitURL.createObjectURL(file) ;
    }
    return url ;
  }
  var $preview = $('#preview-pane'),
  $pcnt = $('#preview-pane .preview-container'),
  $pimg = $('#preview-pane .preview-container img'),
  xsize = $pcnt.width(),
  ysize = $pcnt.height();

  $('#sourceImg').Jcrop({
    onChange: updatePreview,
    onSelect: updatePreview,
    aspectRatio: 1,
  },function(){
    var bounds = this.getBounds();
    boundx = bounds[0];
    boundy = bounds[1];
    jcrop_api = this;
    $preview.appendTo(jcrop_api.ui.holder);
  });
  function updatePreview(c)
  {
    if (parseInt(c.w) > 0)
    {
      var rx = xsize / c.w;
      var ry = ysize / c.h;
      $pimg.css({
        width: Math.round(rx * boundx) + 'px',
        height: Math.round(ry * boundy) + 'px',
        marginLeft: '-' + Math.round(rx * c.x) + 'px',
        marginTop: '-' + Math.round(ry * c.y) + 'px'
      });
    profile.x = c.x;
    profile.y = c.y;
    profile.w = c.w;
    profile.h = c.h;
    }
  };
});
$.i18n().then(function(data){
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;
  profile = Service.load('Profile');
	var otherlanguage = Otherlanguage(profile);
})
