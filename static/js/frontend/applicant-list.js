Vue.config.delimiters = ['{[', ']}'];
var ve = new Vue({
  el: "body",
  data: {
  	job_id:"",
  	pagesize:5,
  	pagenum:1,
  	count:"",
  	freelancers:[], 	
  	job_name:"",
  	refuse_questions:[],
  	archive_questions:[],
  	archive_question:"",
  	refuse_question:"",
  	reason:"",
  	proposal_id:""
  },
  ready: function() {
  	var $this = this;
  	$this.load();
  	Service.get("CommonService").question({qtype:"proposal_refuse_c"}).success(function(result){
	    if(result.error_code==0){
	      $this.refuse_questions = result.questions;
	    }
	  });
	  Service.get("CommonService").question({qtype:"proposal_refuse_c"}).success(function(result){
	    if(result.error_code==0){
	      $this.archive_questions = result.questions;
	    }
	  });
  },
  methods: {
  	load:function(){
			var $this = this;
			$this.job_id = location.href.split("/")[location.href.split("/").length-1];
	  	var datas={
	  		job_id:$this.job_id,
	  		operate:"active",
	  		pagesize:$this.pagesize,
	  		pagenum:$this.pagenum
	  	};
	  	$.i18n().then(function(data){
		    window['CODE'] = data.CODE;
		    window['COMMONS'] = data.COMMONS;
			  Service.get("BidService").select_bid(datas).success(function(result){
			    if(result.error_code==0 && result.proposals.length>0){
			    	for(var i=0;i<result.proposals.length;i++){
			    		result.proposals[i].user.freelancer.proposal_id = result.proposals[i].proposal_id;		    				    		
			    		for(var j=0;j<result.proposals[i].user.freelancer.categorys.length;j++){
								result.proposals[i].user.freelancer.categorys[j].name = COMMONS[result.proposals[i].user.freelancer.categorys[j].name];	
			    		}
			    		$this.freelancers.push(result.proposals[i].user.freelancer);
			    	}   
			    	$this.job_name = result.proposals[0].job.name;
			    	$this.pagenum = result.pagenum;
			    	if($this.pagenum == Math.ceil(result.count/$this.pagesize)){
			  			$("#loadMore").hide();
			  		}
			    }else{
			    	$("#loadMore").hide();
			    	$(".applicant-list-blank").show();
			    }   	
			  });
			});
  	},
  	loadMore:function(){
  		this.pagenum +=1;
			this.load();
  	},
  	showBtns:function(event){
  		if($(event.target).find("i").hasClass("btn-arrow-down")){
  			$(event.target).next().show();
  			$(event.target).find("i").removeClass("btn-arrow-down");
  			$(event.target).find("i").addClass("btn-arrow-up");
  		}else{
				$(event.target).next().hide();
  			$(event.target).find("i").removeClass("btn-arrow-up");
  			$(event.target).find("i").addClass("btn-arrow-down");
  		}
  	},
  	hideList:function(){
			$(".operates").hide();
  		$(".operates").prev().find("i").removeClass("btn-arrow-up");
  		$(".operates").prev().find("i").addClass("btn-arrow-down");
  	},
  	sendOffer:function(id){
  		window.location.href="/clients/proposal/"+id+"/offer";
  	},
  	modalShow:function(name,id){
			this.proposal_id=id;
			$('#'+name).modal('show');
  	},
  	updateOffer:function(data){
  		var $this = this;
  		$this.freelancers=[];
  		Service.get("BidService").update_bid(data).success(function(result){
  			$('.modal').modal('hide');
        if(result.error_code==0){
        	$this.load();
        	$(".alert").html("发送成功啦！").show();
        	$(".alert").removeClass("alert-danger");
          $(".alert").addClass("alert-success");
        	$(".alert").delay(3000).hide(0);
        }else{
        	$(".alert").html("发送失败了，再试一次吧！").show();
          $(".alert").removeClass("alert-success");
          $(".alert").addClass("alert-danger");
        	$(".alert").delay(3000).hide(0);
        }
      });
  	},
  	refuseOffer:function(){
  		if(this.refuse_question==""){
        return;
      }
      var data={
      	proposal_id:this.proposal_id,
				operate:"refuse",
				question_id:this.refuse_question,
				message:this.reason
      };
      this.updateOffer(data);
  	},
  	archiveOffer:function(){
  		if(this.archive_question==""){
        return;
      }
      var data={
      	proposal_id:this.proposal_id,
				operate:"archive",
				question_id:this.archive_question
      };
      this.updateOffer(data);
  	}
  }
});