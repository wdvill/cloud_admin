<template>
  <table>
    <thead>
      <tr>
        <th>里程碑的名字</th>
        <th>托管资金</th>
        <th>结束时间</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in mlist" track-by="$index">
        <td>
          <span class="text-block">{{ $index + 1 }}.</span>
          <input type="text" v-model="item.name" placeholder="请输入里程碑的名字">
        </td>
        <td>
          <span class="text-block">¥</span><input type="text" v-model="item.amount" placeholder="请输入金额">
        </td>
        <td>
          <datepicker :value.sync="item.end_at"
              format="yyyy-MM-dd"
              :show-reset-button="true">
          </datepicker>
        </td>
        <td>
          <a @click="delMilestone($index)">X</a>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  import { datepicker } from 'vue-strap'

  export default {
    props: {
      mlist: [Array]
    },
    methods: {
      delMilestone (index) {
        if (this.mlist.length < 2) {
          return false
        }
        this.mlist.splice(index, 1)
      }
    },
    components: {
      datepicker
    }
  }
</script>