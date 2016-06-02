<template>
  <h3 class="modal-title text-muted text-center">撤销投标</h3>
  <div class="yzj-size-16 yzj-top-distance50" style="padding-left:100px">
    <p>你确定要撤销该投标吗?</p>
    <h4 class="text-info yzj-top-distance30"><strong>原因</strong></h4>
    <div class="text-info yzj-size-14 yzj-top-distance30 yzj-height40">
      <p v-for="item in questions"><input type="radio" name="reason" value="{[item.question_id]}" v-model="question_id">{[item.name]}</p>
    </div>
    <div class="form-group text-warning yzj-top-distance10" name="error" data-name="message" v-show="showErr">
      <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10" aria-hidden="true"></span>
      <span class="errorMsg">请选择撤销原因</span>
    </div>
    <div class="yzj-top-distance30">
      <p class="yzj-size-16"><span class="text-muted">撤销说明</span>（可选）</p>
      <textarea rows="4" class="bidTextarea yzj-top-distance20" style="width:600px" id="refuse-reason" v-model="reason" ></textarea>
    </div>
    <div class="yzj-top-distance50 yzj-size-14 col-xs-offset-2">
      <div class="col-xs-4 clear-right">
        <button type="button" :disabled="btnDisabled" class="btn btn-primary btn-block yzj-right-distance15" id="refuse-btn" v-on:click="save()">确认</button>
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
      question_service.get_question_list({qtype: 'proposal_revoke_f'})
        .success((data) => {
          this.$set('questions', data.questions)
        })
      console.log('proposal_id:' + this.proposal_id)
    },
    data () {
      return {
        questions: [],
        btnDisabled: false,
        showErr: false,
        question_id: ''
      }
    },
    props: ['proposal_id'],
    methods: {
      save () {
        // this.$dispatch('save', 'revoke')
        if (!this.question_id) {
          this.showErr = true
          return false
        }
        this.btnDisabled = true
        proposal_service.update_proposal({proposal_id: this.proposal_id, operate: 'revoke', question_id: this.question_id, message: this.reason})
          .success((data) => {
            if (data.error_code === 0) {
              this.$dispatch('show_alert', 'success', '操作提示', '恭喜你，撤销成功!', this.reload)
            } else {
              this.btnDisabled = false
              this.$dispatch('show_alert', 'danger', '错误提示', data.msg)
            }
          })
      },
      cancel () {
        this.$dispatch('cancel', 'revoke_modal')
      },
      reload () {
        setTimeout(() => {
          window.location.reload()
        }, 2000)
      }
    },
    watch: {
      question_id (value, oldval) {
        if (value) {
          this.showErr = false
        } else {
          this.showErr = true
        }
      }
    }
  }
</script>

