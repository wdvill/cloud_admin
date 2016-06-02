require('../../assets/sass/views/other/help.scss')

import Vue from 'vue'
import contact from '../../components/other/contact-slider.vue'

new Vue({
  el: 'body',
  data: {
    search_content: ''
  },
  components: {
    contact
  },
  methods: {
    onEnter () {
      window.location = '/help' + '?keyword=' + this.search_content
    }
  }
})
