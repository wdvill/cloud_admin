require('../../assets/sass/views/contracts/add-milestone.scss')

import Vue from 'vue'
import YWORK from '../../utils/ywk.js'
import contract from '../../components/contracts/contract-info.vue'
import milestoneList from '../../components/contracts/milestone-list.vue'

// Vue.config.delimiters = ['{[', ']}']
// Vue三方库都是用的是{{}}

let milestoneDataBase = {
  name: '',
  amount: '',
  end_at: ''
}

// 在url上获取 uuid
let uuid = window.location.pathname.split('/')[3]

new Vue({
  el: 'body',
  data: {
    value: '',
    milestoneData: [milestoneDataBase],
    uuid: uuid,
    btnDisable: false
  },
  methods: {

    // 向数组里面添加数据原型 注意要浅拷贝
    addMilestone () {
      let obj = Object.assign({}, milestoneDataBase)
      this.milestoneData.push(obj)
    },

    // 检查数据格式
    checkData () {
      let checkResult = this.milestoneData.find((value, index) => {
        let numRex = /^[0-9]*$/

        // 验证不能为空
        if (!value.name) {
          alert(`请输出第${index + 1}个里程碑名称`)
          return true
        }

        // 数字验证
        if (!value.amount || !numRex.test(value.amount)) {
          alert(`请正确输入第${index + 1}个里程碑的金额`)
          return true
        }

        // 日期验证
        if (!value.end_at) {
          alert(`请选择第${index + 1}个里程碑的截止日期`)
          return true
        }

        let d = +new Date(value.end_at)
        let t = +new Date()

        // 日期验证
        if (d < t) {
          alert(`请正确选择第${index + 1}个里程碑的截止日期`)
          return true
        }

        return false
      })

      // 全部测试通过会返回 undefined
      return !!checkResult

    },

    creatMilestone () {

      // 防止用户连续点击
      if (this.btnDisable) {
        return false
      }

      this.btnDisable = true

      // 验证数据
      if (this.checkData()) {
        this.btnDisable = false
        return false
      }

      // 拼凑需要提交的数据
      let data = {
        contract_id: this.uuid,
        milestones: JSON.stringify(this.milestoneData)
      }

      // 创建里程碑并跳转支付
      YWORK.postJson('/api/milestone', data)
        .success((res) => {

          // 打开开关
          this.btnDisable = false

          if (res.error_code === 0) {
            window.herf = `/contracts/${this.uuid}/milestone/${res.trade_no}`
          } else {
            alert(res.msg)
          }
        })
    }
  },
  components: {
    contract,
    milestoneList
  }
})
