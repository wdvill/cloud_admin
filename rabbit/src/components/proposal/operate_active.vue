<template>
<div class="yzj-box yzj-height30">
  <h5 class="text-muted yzj-size-16">已提交投标</h5>
  <p class="yzj-size-14 yzj-top-distance10">需求方：{[proposal.user.client.name]}</p>
  <h5 class="text-muted yzj-top-distance10">投标方案</h5>
  <p class="yzj-size-14 yzj-top-distance10">投标预算：{[(proposal.price * 0.9).toFixed(2)]}<unit :paymethod="proposal.job.paymethod"></unit></p>
  <p class="yzj-size-14 yzj-top-distance10">需求方收到的报价：{[proposal.price]}<unit :paymethod="proposal.job.paymethod"></unit></p>
  <a class="btn btn2 btn-primary btn-lg yzj-size-14 yzj-top-distance10" v-on:click="bid()">重新投标</a>
  <p class="yzj-top-distance10 text-center" style="width: 180px;">
  <a class="yzj-size-14 text-center text-warning" href="javascript:;" v-on:click="pop()">撤销该投标</a>
  <a class="yzj-size-14 text-center text-warning" href="javascript:;" v-show="proposal.status === 'interview'" v-on:click="freeze()">&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;冻结</a>
  </p>
</div>
<modal :showmodal.sync="modals.revoke_modal" >
  <proposal_revoke :proposal_id="proposal.proposal_id" slot="content"></proposal_revoke>
</modal>
<modal :showmodal.sync="modals.freeze_modal" >
  <proposal_archive :proposal_id="proposal.proposal_id" slot="content"></proposal_archive>
</modal>
<modal :showmodal.sync="modals.bid_modal" >
  <proposal_bid :proposal_id="proposal.proposal_id" :job="proposal.job" :freelancer="proposal.user.freelancer" slot="content"></proposal_bid>
</modal>
</template>

<script>
  import proposal_revoke from '../forms/proposal_revoke.vue'
  import proposal_archive from '../forms/proposal_archive.vue'
  import unit from '../common/unit.vue'
  import proposal_bid from '../forms/proposal_bid.vue'
  import modal from '../common/modal.vue'
  import mixin_modal from '../../mixins/modal.js'
  export default {
    mixins: [mixin_modal],
    created () { },
    data () {
      return {
        showModal: false,
        freezemodal: false
      }
    },
    props: ['proposal'],
    components: {
      modal,
      proposal_revoke,
      proposal_bid,
      proposal_archive,
      unit
    },
    methods: {
      pop () {
        console.log('test pop modal', this.showModal)
        this.open('revoke_modal')
      },
      freeze () {
        this.open('freeze_modal')
      },
      bid () {
        this.open('bid_modal')
      }
    },
    events: {
    }
  }
</script>


