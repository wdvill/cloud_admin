$.i18n().then(function(data){
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;
  new Vue({
	 el:"body",
   data:{
     globel:{},
     works:[],
     noPage:false,
     pageObject:{itemsCount:0,pageNo:1,pageSize:10},
   },
   ready:function(){
      var that = this;
      that.globel = COMMONS;
      that.query_work_list();
   },
   methods:{
     query_work_list:function(pageNo){
       var that = this;
       var  data = {
           pagesize:10,
           pagenum:that.pageObject.pageNo,
       }
       if(pageNo){
         data.pagenum = pageNo;
       }
       Service.get('WorkService').subscribe_works(data).success(function(result){
            that.works = result.subscribes
       })
     }
   }
  });
 })
