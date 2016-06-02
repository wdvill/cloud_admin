<template>
    <div role="alert" class="alert-transition alert-{[showType]}" v-show="showAlert">
      <button type="button" class="close alert_close" @click="showAlert=false"><span>×</span></button>
      <span class="glyphicon {[infoIcon]} alert-icon-float-left"></span>
      <strong v-text="title"></strong>
      <p v-text="msg"></p>
    </div>
</template>

<script>
  export default {
    props: {
      showType: {
        type: String,
        default: 'success' // success info warning danger
      },
      title: {
        type: String,
        default: '操作提示'
      },
      msg: {
        type: String,
        default: ''
      },
      showAlert: {
        type: Boolean,
        default: false
      },
      callback: Function,
      timer: ''
    },
    computed: {
      // 设置显示图标样式
      infoIcon () {
        if (this.showType === 'danger') {
          return 'glyphicon-info-sign'
        }
        return 'glyphicon-ok-sign'
      }
    },
    watch: {
      showAlert (val, oldval) {
        if (val) {
          this.timer = setTimeout(() => {
            this.showAlert = false
          }, 3000)
          // 如果有回调函数，则执行。
          if (this.callback) {
            this.callback()
          }
        } else {
          clearTimeout(this.timer)
        }
      }
    },
    components: {
      alert
    }
  }
</script>
