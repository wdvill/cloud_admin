var Otherlanguage = function(fr){
			fr.save_language = function(type){
				  var that = this;
					if(!that.other_language || that.other_language == ""){
						alert("请选择语言");
						return;
					}
					if(!that.language_level || that.language_level == ""){
						alert("请选择语言等级");
						return;
					}
					if(that.other_languages.length == 0){
						that.other_languages.push({name:that.other_language,level:that.language_level})
					}else {
						var is_exist = false;
						var index;
						for(var i=0;i<that.other_languages.length;i++){
							if(that.other_language == that.other_languages[i].name){
								is_exist= true;
								index = i;
								break;
							}
						}
						if(is_exist){
								that.other_languages[index] = {name:that.other_language,level:that.language_level}
						}else{
							that.other_languages.push({name:that.other_language,level:that.language_level})
						}
						that.other_languages.sort();
					}
					that.other_language = "";
				  that.language_level = "";
					if(!type){
						$(".addlanguage").modal('hide');
					}
			}
			fr.delete_other_languages = function(index) {
				this.other_languages.splice(index, 1);
			}
			fr.edit_other_languages = function(obj) {
				this.other_language = obj.name;
			  this.language_level = obj.level;
			  $(".addlanguage").modal('show');
			}
}
