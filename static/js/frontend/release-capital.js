$.i18n().then(function(data){
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;
  var release_capital = new Vue({
    el:"#body",
    data:{
      global:{},
      data:{},
      is_stop:false,
      is_agree:false,
      message:'',
      filename: '',
      attachment: '',
      errFile: ''
    },
    ready:function(){
      var that = this;
      var redords = [];
      var attachments = [];
      that.global  = COMMONS;
      var data = {contract_id:window.location.pathname.split('/')[3]};
      Service.get('Payment').pay_apply(data).success(function(result){
        if(result.error_code == 0){
          console.log(result)
          that.data = result.data;
          result.data.records.forEach(function(value){
            if(value.attachment_name != ''){
              redords.push(value)
            }
          })
          that.$set('records',redords)
          that.$set('record',result.data.records[0])
        }else{
          alert(result.msg)
          window.location.href='/freelancers/contracts/'+window.location.pathname.split('/')[3]
        }
      });
    },
    methods:{
      notifyFileInput:function(event){
        var file = event.target.files[0]
        if (file.size > 5 * 1024 * 1024) {
          this.errFile = '文件太大'
          return
        } else {
          this.errFile = ''
        }
        var data = new FormData()
        var that = this
        data.append('file', file)
        data.append('_xsrf', Cookies.get('_xsrf'))
        data.append('t', 'milestone')
        $.ajax({
          type: 'POST',
          url: '/api/attachment',
          cache: false,
          dataType: 'json',
          data: data,
          processData: false,
          contentType: false,
          error: function (xhr, textStatus) {
          },
          success: function (result) {
            if (result.error_code !== 0) {
              that.attachment = ''
              that.filename = ''
            } else {
              that.errFile = ''
              that.attachment = result.attachment_id
              that.filename = file.name
            }
          }
        })
      },
      agreepay:function(){
        var that = this;
        var data = {milestone_id:this.data.id,is_agree:'accept',is_stop:this.is_stop};
        Service.get('Payment').agree_pay(data).success(function(result){
            // window.location.href = "/test/project-detail/rwerwrwrew";
            if(result.error_code != 0){
              alert('付款失败');
            }else{
                if(that.is_stop == true){
                  window.location.href='/contracts/'+window.location.pathname.split('/')[3]+'/evaluate'
                }else{
                  window.location.href='/freelancers/contracts/'+window.location.pathname.split('/')[3]
                }
            }
        });
      },
      refusepay:function(){
        var data = {milestone_id:this.data.id,is_agree:'refuse',is_stop:false,message:this.message,attachment_id:this.attachment};
        Service.get('Payment').agree_pay(data).success(function(result){
            // window.location.href = "/test/project-detail/rwerwrwrew";
            if(result.error_code != 0){
              alert('付款失败');
            }else{
              window.location.href='/freelancers/contracts/'+window.location.pathname.split('/')[3]
            }
        });
      },
      releasepay:function(){
        var that = this;
        var data = {milestone_id:this.data.id,is_agree:'release',is_stop:this.is_stop};
        Service.get('Payment').agree_pay(data).success(function(result){
            // window.location.href = "/test/project-detail/rwerwrwrew";
            if(result.error_code != 0){
              alert('付款失败');
            }else{
              if(that.is_stop == true){
                window.location.href='/contracts/'+window.location.pathname.split('/')[3]+'/evaluate'
              }else{
                window.location.href='/freelancers/contracts/'+window.location.pathname.split('/')[3]
              }
            }
        });
      },
      changeAgree:function(){
        this.$set('is_agree', true)
      },
      changeRefuse:function(){
        this.$set('is_agree', false)
      }
   },
  })
})