Vue.config.delimiters = ['{[', ']}'];

var category = new Vue({
	el: "#layout",
	data: {
		categorys: [],
		cur_cate: "",
		isParent: true,
		skills:[],
		UserCategoryService:Service.get('UserCategoryService')
	},
	created: function() {
		var that= this
		$.i18n().then(function(data){
			window['CODE'] = data.CODE;
			window['COMMONS'] = data.COMMONS;
			that.get_category();
			that.user_category();
		});

	},
	methods: {
		get_category:function(){
			var that = this;
			this.UserCategoryService.get_category({
				t: "all",
				category_id: 0
			}).success(function(json){
				var categorys = {}
				if(json.error_code == 0){
					json.categorys.forEach(function(item, index, arr){
						//item.name = COMMONS[item.name];
						if(item.pid == 0){
							categorys[item.category_id] = {"name":item.name, "category_id":item.category_id, "children":[], "src":"/static/images/select-icon"+item.category_id+".png"}
						}
						else{
							categorys[item.pid]["children"].push({"name":item.name, "category_id":item.category_id});
						}
					})
				}else{
					alert(CODE[json.error_code]);
				}
				that.categorys = categorys;
			});
		},
		user_category:function(){
			var that = this;

			this.UserCategoryService.user_category({}).success(function(json){
				if(json.error_code == 0){
					json.categorys.forEach(function(item, idx, arr){
						that.skills.push(item.category_id);
					});
				}
				else{
					alert(CODE[json.error_code]);
				}
			});
		},
		select_parent: function(cid) {
			this.isParent = false;
			this.cur_cate = cid;
		},
		toggle_skill: function(value, evt) {
			var i = this.skills.indexOf(value);
			if(i >= 0){
				this.skills.splice(i, 1);
			}
			else{
				if(this.skills.length < 4){
					this.skills.push(value);
				}
			}
		},
		reselect: function() {
			this.isParent = true;
			this.cur_cate = "";
			this.skills=[];
		},
		update_user_category: function() {
			if(this.skills.length == 0){
				alert("请至少选择一个类别");
				return;
			}
			this.UserCategoryService.user_category_update({category: this.skills.join()})
			.success(function(json){
				if(json.error_code == 0){
					location.href="/users/profile/step/2";
				}else{
					alert(CODE[json.error_code]);
				}
			});
		}
	}
});
