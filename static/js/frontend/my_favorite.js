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
       Service.get('WorkService').collect_list(data).success(function(result){
            if(result.favorites.length < data.pagesize ){
                that.noPage = true;
            }
            that.pageObject = {itemsCount:result.count,pageNo:result.pagenum,pageSize:data.pagesize};
            for(var i=0;i<result.favorites.length;i++){
                that.works.push(result.favorites[i].job);
            }
       })
     },
     del_collect:function(item,$index){
       var that = this;
       data = {
         target_id:item.uuid
       }
       Service.get('WorkService').del_collect(data).success(function(result){
            if(result.error_code == 0){
                that.works.splice($index,1);
            }
       });
     }
   }
  });
 })
