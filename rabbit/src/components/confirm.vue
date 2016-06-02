<template>
<div class="modal fade" id="{[modalId]}" role="dialog">
  <div class="modal-dialog modal-warning" role="document">
    <div class="modal-content confirm-content">
      <div class="modal-header confirm-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" v-text="title"></h4>
      </div>
      <div class="modal-body confirm-body">
        <h4 class="modal-title" v-text="msg">
        </h4>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-primary btn-sm" data-dismiss="modal" @click="okFn">确定</button>
        <button type="button" class="btn btn-default btn-sm" data-dismiss="modal">取消</button>
      </div>
    </div>
  </div>
</div>
</template>
<style>
  .confirm-content {
    min-width: 400px;
  }
  .confirm-header {
    background-color: #f1f1f1;
    border-bottom: 1px solid #e5e5e5;
  }
  .confirm-body {
    min-height: 100px;
  }
</style>
<script>
  export default {
    props: {
      // 容器ID
      modalId: {
        type: String,
        default: 'myModal'
      },
      // 标题
      title: {
        type: String,
        default: '提示信息'
      },
      // 内容
      msg: {
        type: String,
        default: ''
      },
      // 点击确定回调函数
      okFn: {
        type: Function
      }
    }
  }
</script>