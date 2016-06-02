import Vue from 'vue'
import modal from './components/common/modal.vue'
import feedback from './components/forms/feedback.vue'
import floatWindow from './components/float_window.vue'
import mixin_modal from './mixins/modal.js'

Vue.config.delimiters = ['{[', ']}']
/* eslint-disable no-new */
new Vue({
  el: '#float_window',
  mixins: [mixin_modal],
  components: {
    modal,
    feedback,
    floatWindow
  },
  events: {
    open (float_msg) {
      this.open(float_msg)
    }
  }
})
