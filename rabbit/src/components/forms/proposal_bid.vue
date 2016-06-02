<template>
<h3 class="modal-title text-muted text-center">重新投标</h3>
<div class="yzj-size-16 yzj-top-distance50 form-inline" style="padding:0 10%">
  <div class="row">
    <div class="col-xs-6">
      <p>网站显示</p>
      <p class="yzj-top-distance10 yzj-size-14">需求者看到的您的报价</p>
    </div>
    <div class="col-xs-6">
      <div class="form-group">
        <label>￥</label><input type="number" max-length="15" class="form-control" v-model="amount" v-on:keyup="check"/>
        <span v-if="job.paymethod === 'hour'">/小时</span><br/>
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
      <p class="yzj-top-distance10 yzj-size-14">你实际获得的回报</p>
    </div>
    <div class="col-xs-6">
      ￥<input type="text" disabled="true" class="form-control" v-model="real_amount"/>
      <span v-if="job.paymethod === 'hour'">/小时</span>
    </div>
  </div>
  <p class="yzj-top-distance30">您档案中目前的定价是{[freelancer.hourly]}元/小时</p>
  <div class="yzj-top-distance50 yzj-size-14 col-xs-offset-2">
    <div class="col-xs-4 clear-right">
      <button type="button" class="btn btn-primary btn-block yzj-right-distance15" v-on:click="save()">重新投标</button>
    </div>
    <div class="col-xs-4 clear-right">
      <button type="button" :disabled="btnDisabled" class="btn btn-default btn-block yzj-right-distance15" v-on:click="cancel()">取消</button>
    </div>
    <div class="clearfix"></div>
  </div>
</div>

</template>
<script>
  import proposal_service from '../../service/proposal_service'
  export default {
    data () {
      return {
        amount: '',
        real_amount: 0,
        btnDisabled: false,
        amountErr: false
      }
    },
    props: ['job', 'proposal_id', 'freelancer'],
    methods: {
      cancel () {
        this.$dispatch('close', 'bid_modal')
      },
      check () {
        this.real_amount = (this.amount * 0.9).toFixed(2)
      },
      save () {
        if (this.amount === '' || parseInt(this.amount, 10) < 1) {
          this.amountErr = true
          return false
        }
        this.btnDisabled = true
        proposal_service.update_proposal({proposal_id: this.proposal_id, operate: 'reactive', amount: this.amount})
          .success((data) => {
            if (data.error_code === 0) {
              this.$dispatch('show_alert', 'success', '操作提示', '恭喜你，重新投标成功!', this.reload)
            } else {
              this.btnDisabled = false
              this.$dispatch('show_alert', 'danger', '错误提示', data.msg)
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
      amount (val, oldval) {
        if (val === '' || parseInt(val, 10) < 1) {
          this.amountErr = true
        } else {
          this.amountErr = false
        }
      }
    }
  }
</script>
