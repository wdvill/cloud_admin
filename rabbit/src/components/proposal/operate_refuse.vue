<template>
<div class="yzj-box yzj-height30" v-if="proposal.ptype == 'D'">
  <h5 class="text-muted yzj-top-distance10 yzj-size-16">被拒绝的投标</h5>
  <p class="yzj-size-14 yzj-top-distance10">需求方：{[proposal.user.client.name]}</p>
  <p class="yzj-size-14 yzj-top-distance10" v-if="proposal.question !== ''">你被拒绝了该投标：{[proposal.question]}</p>
  <h5 class="text-muted yzj-top-distance10">投标方案</h5>
  <p class="yzj-size-14 yzj-top-distance10">投标预算：{[proposal.price * 0.9]}<unit :paymethod="proposal.job.paymethod"></unit></p>
  <p class="yzj-size-14 yzj-top-distance10">需求方收到的报价：{[proposal.price]}<unit :paymethod="proposal.job.paymethod"></unit></p>
</div>
<div class="yzj-box yzj-height30" v-if="proposal.ptype == 'I'">
  <h5 class="text-muted yzj-top-distance10 yzj-size-16"><i class="proposal-myrefuse"></i>主动拒绝的邀请</h5>
  <p class="yzj-size-14 yzj-top-distance10">需求方：{[proposal.user.client.name]}</p>
  <p class="yzj-size-14 yzj-top-distance10" v-if="proposal.question !== ''">被你拒绝：{[proposal.question]}</p>
</div>
</template>

<script>
  import unit from '../common/unit.vue'
  export default {
    created () {},
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


