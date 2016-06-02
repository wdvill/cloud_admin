import Vue from 'vue'
import $ from 'jquery'
import datetime from './filters/datetime'
import num from './filters/num'
import Cookies from 'js-cookie'
import sendMessage from './components/common/send_message.vue'
Vue.config.delimiters = ['{[', ']}']
Vue.use(datetime)
Vue.use(num)

$.ajaxPrefilter(function (options, originalOptions, jqXHR) {
  try {
    options.data = $.param($.extend(originalOptions.data, { '_xsrf': Cookies.get('_xsrf') }))
  } catch (e) {
    console.log(e)
  }
})

var vue = new Vue({
  el: '#my-jobs',
  data: {
    contracts: [],
    doing: [],
    doing_hour: [],
    applyStoneId: '',
    stoneName: '',
    message: '',
    stoneAmount: 0,
    filename: '',
    attachment: '',
    errFile: '',
    contractId: '',
    current_id: ''
  },
  methods: {
    setContract (id) {
      this.current_id = id
    },
    setDoing (data) {
      let contracts = []
      for (let i = 0; i < data.length; i++) {
        let contract = data[i]
        let stones = contract.stones

        if (contract.status !== 'finish' && contract.status !== 'service' && contract.status !== 'dispute' && contract.status !== 'paid') {
          for (let j = 0; j < stones.length; j++) {
            if (stones[j].status === 'carry' || stones[j].status === 'refuse' || stones[j].status === 'carry_pay') {
              contract.currentStone = stones[j]
              break
            }
          }

          contracts.push(contract)
        }
        // console.log(contract.currentStone.name, 'test stone name')
      }

      this.$set('doing', contracts)
      console.log(this.doing, 'doing')

    },
    DoingHour (data) {
      let contracts = []

      for (let i = 0; i < data.length; i++) {
        let contract = data[i]
        let stones = contract.stones
        if (contract.status !== 'finish' && contract.status !== 'service' && contract.status !== 'dispute' && contract.status !== 'paid') {
          for (let j = 0; j < stones.length; j++) {
            if (stones[j].status === 'carry' || stones[j].status === 'refuse' || stones[j].status === 'carry_pay') {
              contract.currentStone = stones[j]
              break
            }
          }

          contracts.push(contract)
        }
        // console.log(contract.currentStone.name, 'test stone name')
      }

      this.$set('doing_hour', contracts)

    },
    setStone (stone, id) {
      this.applyStoneId = stone.id
      this.stoneName = stone.name
      this.stoneAmount = stone.amount
      this.contractId = id
    },
    notifyFileInput (event) {
      var file = event.target.files[0]
      if (file.size > 5 * 1024 * 1024) {
        this.errFile = '文件太大'
        return
      } else {
        this.errFile = ''
      }
      var data = new FormData()
      var that = this
      data.append('file', file)
      data.append('_xsrf', Cookies.get('_xsrf'))
      data.append('t', 'milestone')
      $.ajax({
        type: 'POST',
        url: '/api/attachment',
        cache: false,
        dataType: 'json',
        data: data,
        processData: false,
        contentType: false,
        error: function (xhr, textStatus) {
        },
        success: function (result) {
          if (result.error_code !== 0) {
            that.attachment = ''
            that.filename = ''
          } else {
            that.errFile = ''
            that.attachment = result.attachment_id
            that.filename = file.name
          }
        }
      })
    },
    apply () {
      var that = this
      let data = {
        milestone_id: this.applyStoneId,
        message: this.message,
        attachment_id: this.attachment
      }
      $.ajax({
        method: 'put',
        url: '/api/milestone',
        dataType: 'json',
        data: data
      }).success((data) => {
        if (data.error_code === 0) {
          $('#apply').modal('hide')
          window.location.href = '/freelancers/contracts/' + that.contractId + '/' + that.applyStoneId + '/complete'
        }
      })
    },
    getStone (id) {
      var that = this
      that.stones.forEach((value)=>{
        if (value.id === id) {
          that.$set('nowStone', value)
        }
      })
    }
  },
  components: {
    sendMessage
  }
})

$.getJSON('/api/contract?timestamp=' + new Date().getTime(), {status: 'paid'}, function (data) {
  if (data.error_code === 0) {
    vue.$set('contracts', data.contracts)
  }
})

$.getJSON('/api/contract?timestamp=' + new Date().getTime(), {status: 'carry_fixed'}, function (data) {
  console.log('carry_fixed', data)
  if (data.error_code === 0) {
    vue.setDoing(data.contracts)
  }
})
$.getJSON('/api/contract?timestamp=' + new Date().getTime(), {status: 'carry_hour'}, function (data) {
  if (data.error_code === 0) {
    vue.DoingHour(data.contracts)
  }
})

