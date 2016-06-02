import Vue from 'vue'
import calendar from '../../components/calendar.vue'
Vue.config.delimiters = ['{[', ']}']

new Vue({
  el: '#body',
  data: {
    show: false,
    value: '2016年5月24日',
    begin_week: '2015-12-20',
    end_week: '2015-12-25',
    x: 0,
    y: 30,
    is_week: true
  },
  components: {
    calendar
  },
  methods: {
    show_calendar () {
      this.show = true
    }
  }
})

