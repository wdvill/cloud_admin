<template>
<h3 class="modal-title text-muted text-center" v-if="is_agree == 'accept'">同意验收</h3>
<h3 class="modal-title text-muted text-center" v-else>结束合同</h3>
<div class="yzj-size-16 yzj-top-distance50 form-inline">
  <div class="text-info yzj-height30" v-if="is_agree == 'accept'">
    <p class="text-muted text-center" v-if="weekstone.calculate_amount != weekstone.amount">释放资金 ¥ {[weekstone.calculate_amount]} 至服务方账户，剩余预付款 ¥ {[weekstone.amount - weekstone.calculate_amount]} 将返还至您的账户余额。</p>
    <p class="text-muted text-center" v-else>释放资金 ¥ {[weekstone.amount]} 至服务方账户。</p>
    <div style="padding:0 20%">
      <p class="yzj-top-distance40"><input type="radio" name="status" v-model="status" value="pause" checked="true">同意验收，保留合同，但暂时不用开启下周工作。</p>
      <p class="yzj-top-distance20"><input type="radio" name="status" v-model="status" value="continue">同意验收，保留合同，并马上开启下周工作。</p>
      <p class="yzj-top-distance20"><input type="radio" name="status" v-model="status" value="stop">同意验收，并结束合同。</p>
    </div>
  </div>
  <div class="text-info yzj-height30 text-center" v-else>拒绝支付服务方本周工作费用 ¥ {[weekstone.calculate_amount]}，结束合同并进入争议流程，申请客服介入。</div>
  <div class="yzj-top-distance50 yzj-size-14 col-xs-offset-2">
    <div class="col-xs-4 clear-right">
      <button type="button" class="btn btn-primary btn-block yzj-right-distance15" v-on:click="accept">确定</button>
    </div>
    <div class="col-xs-4 clear-right">
      <button type="button" class="btn btn-default btn-block yzj-right-distance15" v-on:click="cancel">取消</button>
    </div>
    <div class="clearfix"></div>
  </div>
</div>
</template>
<script>
  import weekstoneService from '../../service/weekstone_service'
  export default {
    data () {
      return {
        status: 'pause'
      }
    },
    props: ['weekstone', 'contract_id', 'is_agree'],
    methods: {
      cancel () {
        this.$dispatch('close', 'weekstone_agree_modal')
      },
      accept () {
        if (this.status !== 'continue') {
          weekstoneService.update_weekstone({weekstone_id: this.weekstone.weekstone_id, status: this.status, is_agree: this.is_agree}).success((data) => {
            let that = this
            if (data.error_code === 0) {
              window.location.href = '/freelancers/contracts/' + that.contract_id
            } else {
              this.$dispatch('close', 'weekstone_agree_modal')
              alert(data.msg)
            }
          })
        } else {
          weekstoneService.update_weekstone({weekstone_id: this.weekstone.weekstone_id, status: this.status, is_agree: this.is_agree}).success((data) => {
            if (data.error_code === 0) {
              window.location.href = '/contracts/' + data.contract_id + '/' + 'weekstone' + '/' + data.trade_no
            } else {
              this.$dispatch('close', 'weekstone_agree_modal')
              alert(data.msg)
            }
          })
        }
      }
    }
  }
</script>
