import Vue from 'vue'
import $ from 'jquery'
import YWORK from '../../utils/ywk.js'
import finish_contract from '../../components/forms/finish_contract.vue'
import postBonus from '../../components/contracts/post_bonus.vue'
import finishHourContract from '../../components/contracts/finish_hour_contract.vue'
import modal from '../../components/common/modal.vue'
import sendMessage from '../../components/common/send_message.vue'
import operateContract from '../../components/contracts/operate_contract.vue'
import strap_alert from '../../components/strap_alert.vue'
import employ from '../../components/job/employ.vue'
import confirm from '../../components/confirm.vue'
import mixin_modal from '../../mixins/modal.js'
import star from '../../components/job/star.vue'
import pay from '../../service/weekstone_service'

require('../../assets/sass/views/clients/my-project.scss')

let formatDate = (date) => {
  let datetime = new Date(date.replace('-', '/').replace('-', '/'))
  let getStr = (num) => {
    return num * 1 < 10 ? '0' + num : num
  }
  return [datetime.getFullYear(), getStr(datetime.getMonth() * 1 + 1), getStr(datetime.getDate())].join('-')
}

let formateTime = (time, style) => {
  let now = new Date()
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

let formateStyle = (time) => {
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

Vue.filter('dataformat', (value) => formatDate(value))
Vue.filter('year_month_day', (value) => {
  let pattern = /\d{4}-\d{2}-\d{2}/.exec(value)
  return pattern ? pattern[0] : value
})
Vue.filter('hourformat', (value) => {
  let hour = Math.floor(value / 60)
  let minute = (value % 60)
  if (minute < 10) {
    minute = '0' + minute
  }
  return hour + ':' + minute
})
$.i18n().then((data) => {
  window['CODE'] = data.CODE
  let COMMONS = data.COMMONS
  new Vue({
    el: 'body',
    data: {
      global: {},
      show_alert: false,
      jobs: [],
      drafts: [],
      contracts: [],
      contract: {},
      profile: {},
      origin_arr: [],
      process: [],
      closed: [],
      uuid: '',
      actual_amount: 0,
      status: ['finish', 'service', 'cancel'],
      is_carray: false,
      stone: '',
      draftTarget: {},
      // 弱提示参数
      alert: {
        showType: 'info',
        msg: '',
        showAlert: false
      }
    },
    mixins: [mixin_modal],
    ready () {
      this.global = COMMONS
      this.getJobs()
      YWORK.getJson('/api/contract', {status: 'all'}).success((result) => {
        this.contracts = this.getResetStone(result.contracts)
        this.initContract(this.contracts)
        for (let i = 0; i < this.contracts.length; i++) {
          if (this.contracts[i].status === 'finish') {
            this.actual_amount += this.contracts[i].amount
          }
        }
      })
      YWORK.getJson('/api/user/profile', {}).success((result) => {
        this.profile = result.profile
      })
    },
    methods: {
      pay (id) {
        pay.post_weekstone({contract_id: id}).success((data) => {
          if (data.error_code === 0) {
            window.location.href = '/contracts/' + data.contract_id + '/' + 'weekstone' + '/' + data.trade_no
          }
        })
      },
      initDrafs (drafts) {
        let draft_list = []
        drafts.forEach((value) => {
          value.draft_time = formateStyle(value.created_at)
          draft_list.push(value)
        })
        this.drafts = draft_list
      },
      update_pro (id, type) {
        YWORK.putJson('/api/jobs/status', {job_id: id, status: type}).success((result) => {
          if (result.error_code === 0) {
            this.getJobs()
          }
        })
      },
      getJobs () {
        YWORK.getJson('/api/jobs/proposal?t=' + new Date().getTime(), {}).success((result) => {
          this.jobs = result.jobs
          this.initDrafs(result.draft)
        })
      },
      initContract (contracts) {
        for (let i = 0; i < contracts.length; i++) {
          if (contracts[i].stoneStatus === 'carry_pay') {
            this.closed.push(contracts[i])
          } else {
            this.process.push(contracts[i])
          }
        }
      },
      delDraft (index) {
        let data = {
          job_id: this.draftTarget.id
        }
        YWORK.deleteJson('/api/jobs', data).success((result) =>{
          if (result.error_code === 0) {
            this.drafts.splice(this.draftTarget.index, 1)
          } else {
            alert(result.msg)
          }
        })
      },
      endOperate () {
        window.location.reload()
      },
      getResetStone (contracts) {
        let len = contracts.length
        let contract = []
        let getStone = (stones) => {
          let jlen = stones.length
          for (let j = 0; j < jlen; j++) {
            if (stones[j].status === 'carry' || stones[j].status === 'carry_pay') {
              return stones[j]
            }
          }
          return stones[jlen - 1]
        }

        for (let i = 0; i < len; i++) {
          if (contracts[i].status === 'finish' || contracts[i].status === 'service' || contracts[i].status === 'carry' || contracts[i].status === 'carry_pay' || contracts[i].status === 'dispute' || contracts[i].status === 'pause') {
            contracts[i].stoneStatus = getStone(contracts[i].stones).status
            contracts[i].stone = getStone(contracts[i].stones)
            if (contracts[i].is_evaluate === true && contracts[i].evaluate.team.content !== undefined) {
              contracts[i].score = (contracts[i].evaluate.team.cooper + contracts[i].evaluate.team.exchange + contracts[i].evaluate.team.punctual + contracts[i].evaluate.team.quality + contracts[i].evaluate.team.skill) / 5
            }
            contract.push(contracts[i])
          }
        }
        return contract
      },
      finish_contract (item) {
        this.contract = item
        let stone = item.stones.find((stone) => {
          this.status.indexOf(stone) === -1
        })
        if (stone) {
          this.is_carray = true
          this.stone = stone
        }
        this.open('finish_modal')
      },
      setContract (item) {
        this.contract = item
      },
      // 再次雇佣
      employ (uid) {
        this.uuid = uid
      },
      // 重新开启合同
      carryContract (item, index) {
        YWORK.putJson('/api/contract', {contract_id: item.id, status: 'carry'}).success((result) =>{
          if (result.error_code === 0) {
            this.alert.msg = '合同重新开启成功!'
            this.alert.showType = 'info'
            this.alert.showAlert = true
            window.location.reload()
          } else {
            this.alert.msg = result.msg
            this.alert.showType = 'danger'
            this.alert.showAlert = true
          }
        })
      }
    },
    components: {
      modal,
      postBonus,
      finishHourContract,
      finish_contract,
      sendMessage,
      operateContract,
      strap_alert,
      employ,
      confirm,
      star
    }
  })
})
