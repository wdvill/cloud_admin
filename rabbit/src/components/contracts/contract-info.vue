<template>
  <ul class="contract-info">
    <li><span>* 合同标题</span>{{info.name}}</li>
    <li><span>* 服务方</span><a :href="'/freelancers/' + info.freelancerId">{{info.freelancerName}}</a></li>
    <li><span>* 签订时间</span>{{info.time}}</li>
  </ul>
</template>

<script>
  import YWORK from '../../utils/ywk.js'

  export default {
    data () {
      return {
        info: {}
      }
    },
    props: {
      uuid: [String]
    },
    ready () {
      this.getContract()
    },
    methods: {
      // 获取合同详情
      getContract () {
        YWORK.getJson('/api/contract',
          { contract_id: this.uuid })
          .success((res) => {
            if (res.error_code === 0) {
              let { name, accept_at: time, user: { freelancer: { name: freelancerName, id: freelancerId } } } = res.contracts[0]
              this.info = {
                name,
                time,
                freelancerName,
                freelancerId
              }
            } else {
              alert(res.msg)
            }
          })
      }
    }
  }
</script>