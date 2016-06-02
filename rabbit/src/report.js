import $ from 'jquery'
import Vue from 'vue'
/* 引用组件 */
import page from './directives/page.js'
import alertdiv from './components/alert.vue'
import reportService from './service/report_service'
import accountService from './service/account_service'
import datetime from './filters/datetime'
import string from './filters/string'

Vue.config.delimiters = ['{[', ']}']
Vue.use(page)
Vue.use(datetime)
Vue.use(string)
new Vue({
  el: '#report',
  data: {
    reports: [],
    error_msg: '',
    amount_carry: 0,
    amount_carry_pay: 0,
    record_count: 0,
    total_times: 0,
    total_amount: 0,
    manual_times: 0,
    total_amount_stones: 0,
    balance: 0,
    pageObject: {itemsCount: 0, pageNo: 1, pageSize: 10},
    select_value: '',
    records: []
  },
  ready () {
    this.get_report_working()
    this.get_record_list()
  },
  components: {
    alertdiv,
    page
  },
  methods: {
    /* 计算总数表格 */
    compute_count (data) {
      let total_times = 0
      let total_amount = 0
      let total_amount_stones = 0
      let manual_times = 0
      let avg_hourly = 0
      for (let i = 0; i < data.weekstones.length; i++) {
        total_times += data.weekstones[i].manual_times
        total_times += data.weekstones[i].shot_times
        manual_times += data.weekstones[i].manual_times
        total_amount += data.weekstones[i].actual_amount
        avg_hourly += data.weekstones[i].hourly
        data.weekstones[i].times = data.weekstones[i].manual_times + data.weekstones[i].shot_times
      }
      avg_hourly = avg_hourly / (data.weekstones.length)
      for (let i = 0; i < data.milestones.length; i++) {
        total_amount_stones += data.milestones[i].amount
      }
      this.$set('reports', data)
      this.$set('total_amount_stones', total_amount_stones.toFixed(2))
      this.$set('balance', data.balance.toFixed(2))
      this.$set('total_times', total_times)
      this.$set('total_amount', total_amount.toFixed(2))
      this.$set('manual_times', manual_times)
      if (total_times && total_amount) {
        this.$set('avg_hourly', (total_amount * 60 / total_times).toFixed(2))
      } else {
        this.$set('avg_hourly', avg_hourly.toFixed(2))
      }
    },
    record_amount () {
      let record_count = 0
      for (let i = 0; i < this.records.length; i++) {
        record_count += this.records[i].amount
      }
      this.$set('record_count', record_count.toFixed(2))
    },
    /* 获取进行中工作 */
    get_report_working () {
      reportService.get_freelancer_report({status: 'carry'}).success((result) =>{
        if (result.error_code === 0) {
          this.compute_count(result)
          this.$set('amount_carry', result.amount_carry.toFixed(2))
          this.$set('amount_carry_pay', result.amount_carry_pay.toFixed(2))
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    },
    /* 获取审核中工作 */
    get_report_checking () {
      reportService.get_freelancer_report({status: 'carry_pay'}).success((result) =>{
        if (result.error_code === 0) {
          this.compute_count(result)
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    },
    /* 获取账户金额 */
    get_record_list () {
      let data = {
        pagenum: this.pageObject.pageNo,
        pagesize: this.pageObject.pageSize,
        report: true
      }
      accountService.get_record_list(data).success((result) =>{
        if (result.error_code === 0) {
          this.$set('records', result.records)
          this.pageObject = {itemsCount: result.count, pageNo: data.pagenum, pageSize: data.pagesize}
          this.record_amount()
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    }
  },
  watch: {
    select_value (value) {
      let data = {
        pagenum: this.pageObject.pageNo,
        pagesize: this.pageObject.pageSize,
        report: true
      }
      if (value === 'income') {
        data.rtype = 'income'
      } else if (value === 'bonus') {
        data.rtype = 'bonus'
      }
      accountService.get_record_list(data).success((result) =>{
        if (result.error_code === 0) {
          this.$set('records', result.records)
          this.pageObject = {itemsCount: result.count, pageNo: data.pagenum, pageSize: data.pagesize}
          this.record_amount()
        } else {
          $('#alert').modal('show')
          this.error_msg = result.msg
        }
      })
    }
  }
})
