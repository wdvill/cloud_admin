<template>
  <div class="modal fade bs-example-modal-lg choose-sort" id="operate-contract" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
    <div class="modal-dialog contract-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true" class="yzj-size-30">&times;</span>
          </button>
          <h4 class="modal-title" v-text="title"></h4>
        </div>
        <div class="modal-body yzj-box yzj-height20 yzj-top-distance10">
          <p>暂停{[userName]}的合同，项目"{[projectName]}"</p>
          <p>暂停这份合同，将立即暂停对{[userName]}每小时工作日志的访问直到你重新在开启它，如果你暂停这份合同，请告诉{[userName]}为什么要这么做。</p>
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
      // 合同id
      contractId: String,
      // 服务方名称
      userName: String,
      // 项目名称
      projectName: String,
      // 状态(revoke, pause, carry)
      status: String,
      // model的标题
      title: {
        type: String,
        default: '操作合同'
      },
      // 操作完后的回调函数(非必要)
      callback: Function
    },
    methods: {
      send_message () {
        if (this.message === '') {
          this.errMsg = '请输入原因'
          return
        }
        YWORK.putJson('/api/contract', {contract_id: this.contractId, status: this.status, reason: this.message}, 'application/json').success((result) =>{
          if (result.error_code === 0) {
            $('.modal').modal('hide')
            this.message = ''
            if (this.callback) {
              this.callback()
            }
          } else {
            this.errMsg = result.msg
          }
        })
      }
    }
  }
</script>