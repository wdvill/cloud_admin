var getValueByName = function(name) {
  var paramArr = location.search.substr(1).split('&'),
    parameter = {};
  for (var i = 0, len = paramArr.length; i < len; i++) {
    var param = paramArr[i].split('=');
    parameter[param[0]] = param[1];
  }
  return parameter[name] ? parameter[name]: ''
};
$.i18n().then(function(data){
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;

  var findperson_list =new Vue({
    el:"#body",
    data:{
      users:[],
      pageObject:{itemsCount:0,pageNo:1,pageSize:10},
      keyword:"",
      category:'',
      hourly_range: 0,
      categorys:''
    },
    ready:function(){
      var that = this;
      that.keyword = decodeURI(getValueByName('q'));
      var data = {
        keyword:that.keyword,
        hourly_range:that.hourly_range,
        categorys:that.categorys,
        pagenum:that.pageObject.pageNo,
        pagesize:that.pageObject.pageSize,
      }

      that.get_person(data)
      Service.get('CommonService').category({category_id: 0}).success(function(result){
        if(result.error_code == 0){
          that.category = result.categorys
        }
      });
    },
    methods:{
      searchperson: function () {
        var that = this
        var data = {
          keyword:that.keyword,
          hourly_range:that.hourly_range,
          categorys:that.categorys,
          pagenum:that.pageObject.pageNo,
          pagesize:that.pageObject.pageSize,
        }
        this.get_person(data)
      },
      get_person:function(data){
        var that = this;
        Service.get('client').search_freelancer(data).success(function(result){
          that.users = result.users;
          that.pageObject = {itemsCount:result.count,pageNo:result.pagenum,pageSize:data.pagesize};
        });
      },
      searchkeyword:function(){
        var that = this;
        that.pageObject = {itemsCount:0,pageNo:1,pageSize:10};
        var data = {
          keyword:that.keyword,
          hourly_range:that.hourly_range,
          categorys:that.categorys,
          pagenum:that.pageObject.pageNo,
          pagesize:that.pageObject.pageSize,
        }
        this.get_person(data);
      },
      show_person_detail:function(id){
        window.open('/freelancers/' + id);
      },
      collect_person:function(id){
        var that = this;
        Service.get('WorkService').collect({target_id:id}).success(function(result){
        if(result.error_code == 0){
          that.searchperson()
        }
        else{
          alert(result.msg);
        }
      });
      },
    },
    watch: {
      categorys:function(){
        var that = this;
        that.pageObject = {itemsCount:0,pageNo:1,pageSize:10};
        var data = {
          keyword:that.keyword,
          hourly_range:that.hourly_range,
          categorys:that.categorys,
          pagenum:that.pageObject.pageNo,
          pagesize:that.pageObject.pageSize,
        }
        this.get_person(data);
      },
      hourly_range:function(){
        var that = this;
        that.pageObject = {itemsCount: 0, pageNo: 1, pageSize: 10};
        var data = {
          keyword:that.keyword,
          hourly_range:that.hourly_range,
          categorys:that.categorys,
          pagenum:that.pageObject.pageNo,
          pagesize:that.pageObject.pageSize,
        }
        that.get_person(data)
      }
    }
  })
})