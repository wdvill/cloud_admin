<template>
<h3 class="modal-title text-muted text-center">结束合同</h3>
<div class="yzj-size-16 yzj-top-distance50 form-inline" style="padding:0 10%">
  <div v-if="is_freelancer">
    <p class="text-info yzj-height30" v-if="is_carray">当前合同已还有未完成的工作:【{[stone.name]}】（{[stone.amount]}元），结束合同意味着您主动放弃报酬，请谨慎操作。
    </p>
    <p class="text-info yzj-height30" v-if="!is_carray">当前合同已无未完成工作，您确定要结束合同么？
    </p>
  </div>
  <div v-if="!is_freelancer">
    <div class="text-info yzj-height30" v-if="is_carray">
    <p class="text-muted">当前合同已还有未完成的工作，您需要决定是否支付当前进行中的里程碑的钱给服务方（未开始的里程碑的钱将退还到您的账户）。
    </p>
    <p class="yzj-top-distance30"><input type="radio" name="is_pay" v-model="is_pay" value="true" checked="true">支付里程碑【{[stone.name]}】{[stone.amount]}元，并结束合同</p>
    <p class="yzj-top-distance20"><input type="radio" name="is_pay" v-model="is_pay" value="false">不支付里程碑【{[stone.name]}】{[stone.amount]}元，并结束合同，由客服处理已托管费用。</p>
    </div>
    <p class="text-info yzj-height30" v-if="!is_carray">当前合同已无未完成工作，您确定要结束合同么？
    </p>
  </div>
  <div class="yzj-top-distance50 yzj-size-14 col-xs-offset-2">
    <div class="col-xs-4 clear-right">
      <button type="button" class="btn btn-primary btn-block yzj-right-distance15" v-on:click="finish">结束合同</button>
    </div>
    <div class="col-xs-4 clear-right">
      <button type="button" class="btn btn-default btn-block yzj-right-distance15" v-on:click="cancel">取消</button>
    </div>
    <div class="clearfix"></div>
  </div>
</div>
</template>
<script>
  import contractService from '../../service/contract_service'
  export default {
    data () {
      return {
        is_pay: true
      }
    },
    props: ['stone', 'contract_id', 'is_carray', 'is_freelancer'],
    methods: {
      cancel () {
        this.$dispatch('close', 'finish_modal')
      },
      finish () {
        contractService.update_contract({contract_id: this.contract_id, status: 'finish', is_pay: this.is_pay}).success((data) => {
          let that = this
          if (data.error_code === 0) {
            window.location.href = '/contracts/' + that.contract_id + '/evaluate'
          } else {
            this.$dispatch('close', 'finish_modal')
            alert(data.msg)
          }
        })
      }
    }
  }
</script>
