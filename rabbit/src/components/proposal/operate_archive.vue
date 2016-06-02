<template>
<div class="yzj-box yzj-height30">
  <h5 class="text-muted yzj-top-distance10 yzj-size-16"><i class="proposal-freeze"></i>冻结的投标</h5>
  <p class="yzj-size-14 yzj-top-distance10">需求方：{[proposal.user.client.name]}</p>
  <h5 class="text-muted yzj-top-distance10 yzj-size-16">投标方案</h5>
  <p class="yzj-size-14 yzj-top-distance10">投标预算：{[(proposal.price * 0.9).toFixed(2)]}<unit :paymethod="proposal.job.paymethod"></unit></p>
  <p class="yzj-size-14 yzj-top-distance10">需求方收到的报价：{[proposal.price]}<unit :paymethod="proposal.job.paymethod"></unit></p>
  <a class="btn btn2 btn-primary btn-lg yzj-size-14 yzj-top-distance20" v-on:click="unfreeze(proposal.proposal_id)">激活</a>
  <a class="btn btn2 btn-primary btn-lg yzj-size-14 yzj-top-distance20" style="padding: 0px 39px;" v-on:click="pop">撤销该投标</a>
</div>
<modal :showmodal.sync="modals.revoke_modal" >
  <proposal_revoke :proposal_id="proposal.proposal_id" slot="content"></proposal_revoke>
</modal>
</template>

<script>
  import $ from 'jquery'
  import unit from '../common/unit.vue'
  import proposal_revoke from '../forms/proposal_revoke.vue'
  import modal from '../common/modal.vue'
  import proposal_service from '../../service/proposal_service'
  import mixin_modal from '../../mixins/modal.js'
  export default {
    mixins: [mixin_modal],
    created () { },
    data () {
      return {
      }
    },
    components: {
      modal,
      proposal_revoke,
      unit
    },
    props: ['proposal'],
    methods: {
      pop () {
        this.open('revoke_modal')
      },
      unfreeze (id) {
        proposal_service.update_proposal({'proposal_id': id, 'operate': 'unfreeze'}).success((result) =>{
          if (result.error_code === 0) {
            $('.alert').eq(0).html('激活成功')
            $('.alert').eq(0).show()
            setTimeout(() =>{
              location.reload()
            }, 1000)
          }
        })
      }
    }
  }
</script>
