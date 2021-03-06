import Vue from 'vue'
import $ from 'jquery'
import datetime from './filters/datetime'
import string from './filters/string'
import calendar from './components/calendar.vue'
import budget from './service/report_service'
import Cookies from 'js-cookie'

Vue.config.delimiters = ['{[', ']}']
Vue.use(datetime)
Vue.use(string)
$.ajaxPrefilter(function (options, originalOptions, jqXHR) {
  try {
    options.data = $.param($.extend(originalOptions.data, { '_xsrf': Cookies.get('_xsrf') }))
  } catch (e) {
    console.log(e)
  }
})

var vue = new Vue({
  el: '#body',
  data: {
    end_at: '',
    start_at: ''
  },
  ready () {
    // 当前日期
    let now = new Date()
    let end_year = now.getFullYear()
    let end_month = now.getMonth() + 1
    let end_date = now.getDate()
    end_month = end_month < 10 ? '0' + end_month : end_month
    end_date = end_date < 10 ? '0' + end_date : end_date
    this.end_at = end_year + '年' + end_month + '月' + end_date + '日'
    // 今天本周的第几天
    let that_time = new Date(now.getTime() - (30 * 86400000))
    let start_year = that_time.getFullYear()
    let start_month = that_time.getMonth() + 1
    let start_date = that_time.getDate()
    start_month = start_month < 10 ? '0' + start_month : start_month
    start_date = start_date < 10 ? '0' + start_date : start_date
    this.start_at = start_year + '年' + start_month + '月' + start_date + '日'
    this.get_budgets(this.start_at, this.end_at)
    console.log(this.contracts, 'contracts')
  },
  methods: {
    get_budgets (start_time, end_time) {
      start_time = start_time.replace(/年|月/g, '-').replace(/日/g, '')
      end_time = end_time.replace(/年|月/g, '-').replace(/日/g, '')
      budget.get_client_budget({start_at: start_time, end_at: end_time}).success((data) => {
        if (data.error_code === 0) {
          this.$set('contracts', data.contracts)
        }
      })
    }
  },
  components: {
    calendar
  },
  watch: {
    start_at (value) {
      this.get_budgets(value, this.end_at)
    },
    end_at (value) {
      this.get_budgets(this.start_at, value)
    }
  }
})

vue.$set('test', 'll')
