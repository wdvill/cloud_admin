Vue.config.delimiters = ['{[', ']}'];
var notice=new Vue({
	el:"#notice",
	data:{
		notices_unread:[],
		unread_num:0,
		is_null:true
	},
	ready:function(){
		var that=this
		get_unread_list(that)	
	}
})
var noticelist=new Vue({
	el:"#noticelist",
	data:{
		notices:[],
		unread_num:0,
		all_count:0,
		page_current_all:1,
		page_current_unread:1,
		current_status:0,
		pageObject:{itemsCount:0,pageNo:1,pageSize:20},
		is_null:true
	},
	ready:function(){
		var that=this
		get_all_list(that,20,1)
	},
	methods:{
		get_all:function(){
			var that=this
			get_all_list(that,that.pageObject.pageSize,that.page_current_all)	
		},
		get_unread:function(){
			var that=this
			get_unread_lists(that,that.pageObject.pageSize,that.page_current_unread)	
		},
		pageChange:function(){
				var that=this
				if(noticelist.$data.current_status==0){
					get_all_list(that,that.pageObject.pageSize,that.pageObject.pageNo)
				}else{
					get_unread_lists(that,that.pageObject.pageSize,that.pageObject.pageNo)
				}
		}
	}
})
function putNotice(id){
			Service.get('notify').put_notify({notify_id:id}).success(function(){
				get_unread_list(notice.$data)
				if(noticelist.$data.current_status==1){
					get_unread_lists(noticelist.$data,noticelist.$data.pageObject.pageSize,noticelist.$data.page_current_unread)
				}else{
					get_all_list(noticelist.$data,noticelist.$data.pageObject.pageSize,noticelist.$data.page_current_all)
				}
			});	
}
function seeNotice(id,href){
	Service.get('notify').put_notify({notify_id:id}).success(function(){
		window.location.href = href
		get_unread_list(notice.$data)
		if(noticelist.$data.current_status==1){
			get_unread_lists(noticelist.$data,noticelist.$data.pageObject.pageSize,noticelist.$data.page_current_unread)
		}else{
			get_all_list(noticelist.$data,noticelist.$data.pageObject.pageSize,noticelist.$data.page_current_all)
		}
	})		
}
function deleteNotice(id){
	var id=parseInt(id.substring(4))
	Service.get('notify').delete_notify({notify_id:id}).success(function(){
		if(noticelist.$data.current_status==0){
			get_all_list(noticelist.$data,noticelist.$data.pageObject.pageSize,noticelist.$data.page_current_all)
		}else{
			Service.get('notify').get_notify({rtype:'unread',pagesize:20,pagenum:noticelist.$data.page_current_unread}).success(function(data){
				get_unread_lists(noticelist.$data,noticelist.$data.pageObject.pageSize,noticelist.$data.page_current_unread)
				noticelist.$data.all_count=noticelist.$data.all_count-1
				get_unread_list(notice.$data)
			});
		}
	})
}
function get_all_list(obj,psize,page){
	Service.get('notify').get_notify({rtype:'all',pagesize:psize,pagenum:page}).success(function(data){
				if(data.error_code==0){
					obj.notices=data.notify
					obj.all_count=data.count
					obj.pageObject={itemsCount:data.count,pageNo:data.pagenum,pageSize:20}
					obj.page_current_all=page
					obj.current_status=0
					obj.unread_num=data.count_unread
					if(obj.all_count==0){
						obj.is_null=true
					}else{
						obj.is_null=false
					}
					console.log(data,'data');
				}
			});
}
function get_unread_list(obj){
	Service.get('notify').get_notify({rtype:'unread',pagesize:5,pagenum:1}).success(function(data){
				obj.notices_unread=data.notify
				obj.unread_num=data.count
				noticelist.$data.unread_num=data.count
				if(obj.unread_num==0){
						obj.is_null=true
					}else{
						obj.is_null=false
					}
			});
}
function get_unread_lists(obj,psize,page){
	Service.get('notify').get_notify({rtype:'unread',pagesize:psize,pagenum:page}).success(function(data){
				obj.notices=data.notify
				obj.unread_num=data.count
				obj.pageObject={itemsCount:data.count,pageNo:data.pagenum,pageSize:20}
				obj.page_current_unread=page
				obj.current_status=1
				if(obj.unread_num==0){
						obj.is_null=true
					}else{
						obj.is_null=false
					}
				console.log(data)
			});
}