import Vue from 'vue'
import $ from 'jquery'
import datetime from './filters/datetime'
import finish_contract from './components/forms/finish_contract.vue'
import modal from './components/common/modal.vue'
import mixin_modal from './mixins/modal.js'
import num from './filters/num'
import star from './directives/star'
import Cookies from 'js-cookie'
import postBonus from './components/contracts/post_bonus.vue'
import finishHourContract from './components/contracts/finish_hour_contract.vue'
import sendMessage from './components/common/send_message.vue'
import pay from './service/weekstone_service'
require('./assets/sass/views/freelancers/contract-detail.scss')

Vue.config.delimiters = ['{[', ']}']
Vue.use(datetime)
Vue.use(num)
Vue.use(star)

var uuid = window.location.pathname.split('/')[3]

$.ajaxPrefilter(function (options, originalOptions, jqXHR) {
  try {
    options.data = $.param($.extend(originalOptions.data, { '_xsrf': Cookies.get('_xsrf') }))
  } catch (e) {
    console.log(e)
  }
})

new Vue({
  el: '#my-jobs',
  mixins: [mixin_modal],
  data: {
    contracts: [],
    computed: '',
    doing: [],
    doing_hour: [],
    applyStoneId: '',
    stoneName: '',
    message: '',
    stoneAmount: 0,
    filename: '',
    attachment: '',
    is_pay: '',
    errFile: '',
    contractId: '',
    status: ['finish', 'service', 'cancel'],
    is_carray: false,
    stone: '',
    money: '',
    description: '',
    money_type: '',
    is_submit: '',
    uuid: uuid
  },
  computed: {
    workloadNow () {
      return this.contract.stones[this.contract.stones.length - 1].shot_times
    },
    workloadPrev () {
      return this.contract.stones[this.contract.stones.length - 2] ? this.contract.stones[this.contract.stones.length - 2].shot_times : 0
    },
    isInProgress () {
      return this.contract.status === 'carry' || this.contract.status === 'carry_pay' || this.contract.status === 'paid'
    },
    isPauce () {
      return this.contract.status === 'pause' || (this.contract.status === 'carry' && this.contract.stones[this.contracts.stones.length - 1].status === 'finish' && this.contract.job.paymethod === 'hour')
    },
    isEnd () {
      return this.contract.status !== 'finish' && this.contract.status !== 'dispute' && this.contract.status !== 'service'
    }
  },
  ready () {
    let timestamp = new Date().getTime()
    $.getJSON('/api/contract', {timestamp: timestamp, contract_id: uuid}, (data) => {
      if (data.error_code === 0) {
        let totalc = 0
        let totalf = 0
        this.setContract(data)
        if (this.contract.evaluate.team.content !== undefined) {
          totalc = (parseInt(this.contract.evaluate.team.exchange, 10) + parseInt(this.contract.evaluate.team.cooper, 10) + parseInt(this.contract.evaluate.team.quality, 10) + parseInt(this.contract.evaluate.team.skill, 10) + parseInt(this.contract.evaluate.team.punctual, 10)) / 5
          this.$set('totalc', totalc.toFixed(2))
        }
        if (this.contract.evaluate.user.content !== undefined) {
          totalf = (parseInt(this.contract.evaluate.user.exchange, 10) + parseInt(this.contract.evaluate.user.cooper, 10) + parseInt(this.contract.evaluate.user.quality, 10) + parseInt(this.contract.evaluate.user.skill, 10) + parseInt(this.contract.evaluate.user.avail, 10) + parseInt(this.contract.evaluate.user.deliver, 10)) / 6
          this.$set('totalf', totalf.toFixed(2))
        }
        for (let i = 0; i < this.stones.length; i++) {
          if (this.status.indexOf(this.stones[i].status) === -1) {
            this.is_carray = true
            this.stone = this.stones[i]
            return
          }
        }
      }
    })
  },
  methods: {
    finish_contract () {
      this.open('finish_modal')
    },
    setContract (data) {
      let stone = []
      this.contract = data.contracts[0]
      this.contract.stones.forEach((value) => {
        value.apply_time = formateStyle(value.request_at)
        value.pay_time = formateStyle(value.audit_at)
        stone.push(value)
      })
      this.$set('stones', stone)
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
    pay (id) {
      pay.post_weekstone({contract_id: id}).success((data) => {
        if (data.error_code === 0) {
          window.location.href = '/contracts/' + data.contract_id + '/' + 'weekstone' + '/' + data.trade_no
        }
      })
    }
  },
  components: {
    modal,
    finish_contract,
    postBonus,
    finishHourContract,
    sendMessage
  }
})

function formateTime (time, style) {
  let now = new Date()
  if (time === undefined) {
    return
  }
  let d = time.split(' ')
  let old = new Date(d[0].split('-')[0], d[0].split('-')[1] - 1, d[0].split('-')[2], d[1].split(':')[0], d[1].split(':')[1], d[1].split(':')[2])
  let dt = now.getTime() - old.getTime()
  switch (style) {
    case 's':
      return parseInt(dt / 1000, 10)
    case 'n':
      return parseInt(dt / 60000, 10)
    case 'h':
      return parseInt(dt / 3600000, 10)
    case 'd':
      return parseInt(dt / 86400000, 10)
    case 'm':
      return (now.getMonth() + 1) + ((now.getFullYear() - old.getFullYear()) * 12) - (old.getMonth() + 1)
    case 'y':
      return now.getFullYear() - old.getFullYear()
  }
}
function formateStyle (time) {
  if (time === '') {
    return null
  }
  if (formateTime(time, 's') < 60) {
    return formateTime(time, 's') + '秒'
  } else if (formateTime(time, 'n') < 60) {
    return formateTime(time, 'n') + '分钟'
  } else if (formateTime(time, 'h') < 24) {
    return formateTime(time, 'h') + '小时'
  } else if (formateTime(time, 'd') < 31) {
    return formateTime(time, 'd') + '天'
  } else if (formateTime(time, 'm') < 12) {
    return formateTime(time, 'm') + '个月'
  } else if (formateTime(time, 'y') < 60) {
    return formateTime(time, 'y') + '年'
  }
}
