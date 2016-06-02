<template>
<div class="yzj-box yzj-height30">
  <p class="text-muted yzj-size-16"><img src="/static/images/check-mark.png"/>&nbsp;被雇佣</p>
  <p class="yzj-size-14 yzj-top-distance10">需求方：{[proposal.user.client.name]}</p>
  <p class="text-muted yzj-top-distance10 yzj-size-16">投标方案</p>
  <p class="yzj-size-14 yzj-top-distance10">投标预算：{[(proposal.price * 0.9).toFixed(2)]}<unit :paymethod="proposal.job.paymethod"></unit></p>
  <p class="yzj-size-14 yzj-top-distance10">需求方收到的报价：{[proposal.price]}<unit :paymethod="proposal.job.paymethod"></unit></p>
  <a class="btn btn2 btn-primary btn-lg yzj-size-14 yzj-top-distance10" href="/freelancers/offer/{[proposal.contract_id]}">查看offer</a>
</div>
</template>

<script>
  import unit from '../common/unit.vue'
  export default {
    created () { },
    data () {
      return {
      }
    },
    components: {
      unit
    },
    props: ['proposal']
  }
</script>


