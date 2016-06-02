<template>
<h3 class="modal-title text-muted text-center">接受邀请</h3>
<div class="yzj-size-16 yzj-top-distance50 form-inline" style="padding:0 10%">
  <p class="text-info yzj-height30">您可以通过给出您的报价来接受邀请。当您确定投标之后，这个邀请状态将变为“沟通中”。你将和需求方进行沟通，并最终确定是否被雇佣</p>
  <h4 class="text-info yzj-top-distance50">附言（必填）</h4>
  <div class="yzj-top-distance20">
    <textarea class="form-control" max-length="100" rows="7" style="width:80%" v-model="message"></textarea>
  </div>
  <div class="form-group text-warning yzj-top-distance10" name="error" data-name="message" v-show="messageErr">
      <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10" aria-hidden="true"></span>
      <span class="errorMsg">附言必填</span>
  </div>
  <h4 class="text-muted yzj-top-distance30 yzj-bot-distance30"><strong>报价</strong></h4>
  <div class="row">
    <div class="col-xs-6">
      <p>网站显示</p>
      <p class="yzj-top-distance10">需求者看到的您的报价</p>
    </div>
    <div class="col-xs-6">
      <div class="form-group">
        <label>￥</label><input type="number" max-length="15" class="form-control" v-model="amount"/>
        <span v-if="job.paymethod === 'hour'">/小时</span>
        <div class="form-group text-warning yzj-top-distance10" name="error" data-name="message" v-show="amountErr">
          <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10" aria-hidden="true"></span>
          <span class="errorMsg">报价必填且大于0</span>
        </div>
      </div>
    </div>
  </div>
  <div class="row yzj-top-distance20">
    <div class="col-xs-6">
      <p>实际收益</p>
      <p class="yzj-top-distance10">你实际获得的回报</p>
    </div>
    <div class="col-xs-6">
      ￥<input type="text" readonly class="form-control" v-model="amount*0.9"/>
      <span v-if="job.paymethod === 'hour'">/小时</span>
    </div>
  </div>
  <div class="yzj-top-distance50 yzj-size-14 col-xs-offset-2">
    <div class="col-xs-4 clear-right">
      <button type="button" :disabled="btnDisabled" class="btn btn-primary btn-block yzj-right-distance15" v-on:click="save()">接受邀请</button>
    </div>
    <div class="col-xs-4 clear-right">
      <button type="button" class="btn btn-default btn-block yzj-right-distance15" v-on:click="cancel()">取消</button>
    </div>
    <div class="clearfix"></div>
  </div>
</div>
</template>
<script>
  import strapAlert from '../strap_alert.vue'
  import proposal_service from '../../service/proposal_service'
  export default {
    data () {
      return {
        amount: '',
        message: '',
        btnDisabled: false,
        amountErr: false,
        messageErr: false
      }
    },
    props: ['job', 'proposal_id'],
    methods: {
      cancel () {
        this.$dispatch('close', 'bid_modal')
      },
      save () {
        if (this.message === '') {
          this.messageErr = true
          return false
        }
        if (this.amount === '' || parseInt(this.amount, 10) < 1) {
          this.amountErr = true
          return false
        }
        this.btnDisabled = true
        proposal_service.update_proposal({proposal_id: this.proposal_id, operate: 'accept', amount: this.amount, message: this.message})
          .success((data) => {
            if (data.error_code === 0) {
              this.$dispatch('show_alert', 'success', '操作提示', '恭喜你，已接受邀请', this.reload)
              // this.showRAlert('操作提示', '恭喜你，已接受邀请', 'success')
            } else {
              this.btnDisabled = false
              this.$dispatch('show_alert', 'danger', '错误提示', data.msg)
              // this.showRAlert('错误提示', data.msg, 'danger')
            }
          })
      },
      reload () {
        setTimeout(() => {
          window.location.reload()
        }, 2000)
      }
    },
    watch: {
      message (val, oldval) {
        if (val) {
          this.messageErr = false
        } else {
          this.messageErr = true
        }
      },
      amount (val, oldval) {
        if (val === '' || parseInt(val, 10) < 1) {
          this.amountErr = true
        } else {
          this.amountErr = false
        }
      }
    },
    components: {
      strapAlert
    }
  }
</script>
