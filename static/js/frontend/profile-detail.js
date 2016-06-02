$.i18n().then(function(data){
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;
  var resume = Service.load('Resume');
	var otherlanguage = Otherlanguage(resume);

  resume.edit_intro = function(){
    this.overview = this.profile.overview;
    $(".editresume").modal('show');
  }

  resume.save_intro = function(){
    var that  = this;
    var data = {overview:that.overview}
      Service.get('ResumeService').put_profile(data).success(function(result){
        if(result.error_code == 0){
            that.profile.overview = that.overview;
              $(".editresume").modal('hide');
        }
    })
  }

  resume.edit_hourly = function(){
      var that = this;
      that.hourly = that.profile.hourly;
      $(".price").modal('show');
  }


  resume.save_hourly = function(){
    var that  = this;
    var data = {hourly:that.hourly}
      Service.get('ResumeService').put_profile(data).success(function(result){
        if(result.error_code == 0){
            that.profile.hourly = that.hourly;
              $(".price").modal('hide');
        }
    })
  }

  resume.edit_location = function(){
    var that = this;
    Service.get('CommonService').address({address_id:that.profile.location.parent_id}).success(function(result){
        that.child_address = result.addresses;
        that.address_pid = that.profile.location.parent_id;
        $(".edit_location").modal('show');
    });
  }
  resume.save_location = function(){
    var that  = this;
    var data = {location:that.profile.location.location_id,title:that.profile.title}
    Service.get('ResumeService').put_profile(data).success(function(result){
      if(result.error_code == 0){
        Service.get("ResumeService").get_profile().success(function(result){
            that.profile.location  = result.profile.location;
            that.profile.title = result.profile.title;
            $(".edit_location").modal('hide');
        })
      }
    });
  }

})
