<template>
  <h3 class="modal-title text-muted text-center">拒绝邀请</h3>
  <div class="yzj-size-16 yzj-top-distance50" style="padding-left:100px">
    <p>我们将含蓄的告知需求方您对该项目没兴趣</p>
    <h4 class="text-info yzj-top-distance30"><strong>原因</strong></h4>
    <div class="text-info yzj-size-14 yzj-top-distance30 yzj-height40">
      <p v-for="item in questions"><input type="radio" name="reason" value="{[item.question_id]}" v-model="question_id">{[item.name]}</p>
    </div>
    <div class="yzj-top-distance30">
      <p class="yzj-size-16"><span class="text-muted">附言</span>（选填）</p>
      <textarea rows="4" class="bidTextarea yzj-top-distance20" style="width:600px" id="refuse-reason" v-model="reason"></textarea>
    </div>
    <div class="yzj-top-distance50 yzj-size-14 col-xs-offset-2">
      <div class="col-xs-4 clear-right">
        <button type="button" class="btn btn-primary btn-block yzj-right-distance15" id="refuse-btn" v-on:click="save()">拒绝邀请</button>
      </div>
      <div class="col-xs-4 clear-right">
        <button type="button" class="btn btn-default btn-block yzj-right-distance15" data-dismiss="modal" v-on:click="cancel()">取消</button>
      </div>
      <div class="clearfix"></div>
    </div>
  </div>
</template>
<script>
  import question_service from '../../service/question_service'
  import proposal_service from '../../service/proposal_service'
  export default {
    created () {
      let _self = this
      question_service.get_question_list({qtype: 'proposal_refuse_f'})
        .success((data) => {
          _self.$set('questions', data.questions)
        })
    },
    data () {
      return {
        questions: []
      }
    },
    props: ['proposal_id'],
    methods: {
      save () {
        this.$dispatch('save', 'refuse')
        proposal_service.update_proposal({proposal_id: this.proposal_id, operate: 'refuse', question_id: this.question_id, message: this.reason})
          .success((data) => {
            if (data.error_code === 0) {
              this.$dispatch('save', 'refuse_modal')
              window.location.reload()
            } else {
              alert(data.msg)
            }
          })
      },
      cancel () {
        this.$dispatch('cancel', 'refuse_modal')
      }
    },
    watch: {
      proposal_id (value) {
        console.log(value, 'created')
      }
    }
  }
</script>

