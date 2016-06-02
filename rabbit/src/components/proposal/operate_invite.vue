<template>
<div class="yzj-box yzj-height30">
  <h5 class="text-muted yzj-top-distance10 yzj-size-16">投标邀请</h5>
  <p class="yzj-size-14 yzj-top-distance10">需求方：{[proposal.user.client.name]}</p>
  <p class="yzj-size-14 yzj-top-distance5">您是不是对该工作感兴趣呢？</p>
  <a class="btn btn2 btn-primary btn-lg yzj-size-14 yzj-top-distance20" v-on:click="accept">接受邀请</a>
  <p class="yzj-top-distance10 text-center" style="width:81%">
  <a class="yzj-size-14 text-warning" href="javascript:;" v-on:click="refuse">拒绝</a>
  </p>
</div>
<modal :showmodal.sync="modals.bid_modal" >
  <proposal_accept :proposal_id="proposal.proposal_id" :job="proposal.job" slot="content"></proposal_accept>
</modal>
<modal :showmodal.sync="modals.refuse_modal" >
  <proposal_refuse :proposal_id="proposal.proposal_id" slot="content"></proposal_refuse>
</modal>
</template>

<script>
  import unit from '../common/unit.vue'
  import proposal_accept from '../forms/proposal_accept.vue'
  import proposal_refuse from '../forms/proposal_refuse.vue'
  import modal from '../common/modal.vue'
  import mixin_modal from '../../mixins/modal.js'
  export default {
    mixins: [mixin_modal],
    components: {
      modal,
      proposal_accept,
      proposal_refuse,
      unit
    },
    props: ['proposal'],
    methods: {
      accept () {
        this.open('bid_modal')
      },
      refuse () {
        this.open('refuse_modal')
      }
    }
  }
</script>
