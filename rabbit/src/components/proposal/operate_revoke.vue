<template>
<div class="yzj-box yzj-height30">
  <h5 class="text-muted yzj-size-16">撤回的投标</h5>
  <p class="yzj-size-14 yzj-top-distance10">需求方：{[proposal.user.client.name]}</p>
  <p class="yzj-size-14" v-if="proposal.question !== ''">你撤回了该投标：{[proposal.question]}</p>
  <p class="yzj-size-14" v-if="proposal.reason !== ''">撤回说明：{[proposal.reason]}</p>
  <h5 class="text-muted yzj-top-distance10">投标方案</h5>
  <p class="yzj-size-14 yzj-top-distance10">投标预算：{[(proposal.price * 0.9).toFixed(2)]}<unit :paymethod="proposal.job.paymethod"></unit></p>
  <p class="yzj-size-14 yzj-top-distance10">需求方收到的报价：{[proposal.price]}<unit :paymethod="proposal.job.paymethod"></unit></p>
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


