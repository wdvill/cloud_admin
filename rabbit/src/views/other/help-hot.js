require('../../assets/sass/views/other/help.scss')

import Vue from 'vue'
import modal from '../../components/common/modal.vue'
import feedback from '../../components/forms/feedback.vue'
import contact from '../../components/other/contact-slider.vue'
import mixin_modal from '../../mixins/modal.js'

new Vue({
  el: 'body',
  mixins: [mixin_modal],
  data: {
    search_content: '',
    num_input: 0,
    num_li: 0
  },
  components: {
    modal,
    feedback,
    contact
  },
  methods: {
    onEnter () {
      window.location = '/help' + '?keyword=' + this.search_content
    }
  },
  events: {
    open (float_msg) {
      this.open(float_msg)
    }
  }
})
