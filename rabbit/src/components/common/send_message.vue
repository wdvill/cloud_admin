<template>
  <div class="modal fade bs-example-modal-lg choose-sort" id="send_message" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
    <div class="modal-dialog contract-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true" class="yzj-size-30">&times;</span>
          </button>
        </div>
        <div class="modal-body yzj-box yzj-height20 yzj-top-distance10">
          <h3 class="modal-title text-muted text-center">发送消息</h3>
          <div class="yzj-size-16 text-center yzj-top-distance50 yzj-bot-distance50">
            <div class="text-info yzj-size-14 yzj-height40">
              <textarea class="bidTextarea" rows="7" v-model="message"></textarea>
            </div>
            <p class="text-warning yzj-size-14 yzj-top-distance10">{[errMsg]}</p>
            <div class="yzj-top-distance50 yzj-size-14">
              <button type="button" class="btn btn-primary btn-lg yzj-right-distance15" v-on:click.stop="send_message">提交</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import $ from 'jquery'
  import YWORK from '../../utils/ywk.js'

  export default {
    data () {
      return {
        errMsg: '',
        message: ''
      }
    },
    props: {
      // 投标id
      proposalId: [String, Number],
      // 合同Id
      contractId: [String, Number],
      load: Function,
      selectCount: Function
    },
    methods: {
      send_message () {
        if (this.message === '') {
          this.errMsg = '请输入消息内容'
          return
        }
        YWORK.postJson('/api/proposal/message', {proposal_id: this.proposalId, contract_id: this.contractId, content: this.message}, 'application/json').success((result) =>{
          if (result.error_code === 0) {
            $('.modal').modal('hide')
            this.message = ''
            if (this.load) {
              this.load()
            }
            if (this.selectCount) {
              this.selectCount()
            }
          } else {
            this.errMsg = result.msg
          }
        })
      }
    }
  }
</script>