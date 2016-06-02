<template>
<h3 class="modal-title text-info text-center" id="myModalLabel">意见反馈</h3>
<form id="feedback" class="form-horizontal yzj-top-distance50 col-xs-11 col-xs-offset-1">
  <div class="row">
    <div class="col-xs-2 clear-both yzj-size-14">
      留言
    </div>
    <div class="col-xs-8">
      <textarea class="form-control feedback" v-model="feed"></textarea>
      <p class="text-warning yzj-size-14 yzj-top-distance10">{[feederror]}</p>
    </div>
  </div>
  <div class="row yzj-top-distance20">
    <div class="col-xs-2 clear-both yzj-size-14 yzj-top-distance10">
      手机号/邮箱
    </div>
    <div class="col-xs-8">
      <input class="form-control" type="text" v-model="tel">
      <p class="text-warning yzj-size-14 yzj-top-distance10">{[telerror]}</p>
    </div>
  </div>
  <div class="clearfix"></div>
  <div class="row">
    <div class="yzj-top-distance70 col-xs-offset-2 col-xs-8">
      <button type="button" class="btn btn-primary btn-lg yzj-right-distance30" v-on:click="submit_msg()">提交反馈</button>
      <button type="button" class="btn btn-default btn-lg yzj-right-distance15" v-on:click="close()">取消</button>
    </div>
  </div>
  <div class="yzj-top-distance70"></div>
</form>
</template>

<script>
import feedbackService from '../../service/feedback_service'
import $ from 'jquery'

export default {
  data () {
    return {
      feed: '',
      tel: '',
      feederror: '',
      telerror: '',
      is_submit: false
    }
  },
  props: ['current'],
  watch: {
    feed (val) {
      if (val.length === 0) {
        console.log(this.is_submit)
        this.feederror = '反馈意见不能为空！'
        this.is_submit = false
      } else {
        this.feederror = ''
        this.is_submit = true
      }
    },
    tel (val) {
      let regEmail = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/
      let regTel = /^1\d{10}$/
      if (!regEmail.test(val) && !regTel.test(val)) {
        this.telerror = '您输入的手机号或邮箱格式不正确！'
        this.is_submit = false
      } else {
        this.telerror = ''
        this.is_submit = true
      }
    }
  },
  methods: {
    submit_msg () {
      let data = {
        t: 'suggest',
        content: this.feed,
        contract: this.tel
      }
      feedbackService.send_feedback(data).success((result) =>{
        if (result.error_code === 0) {
          let _self = this
          _self.$dispatch('close', 'float_msg')
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    },
    close () {
      let _self = this
      _self.$dispatch('close', 'float_msg')
    }
  }
}
</script>