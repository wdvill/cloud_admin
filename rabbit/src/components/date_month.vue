<template>
  <select class="form-control select-control" v-model="monthv">
    <option v-for="month in monthList" v-bind:value="month">{[month]}</option>
  </select>
</template>

<script>
  export default {
    created () {
      if (!this.monthv) {
        this.monthv = this.currentMonth
      }
    },
    data () {
      let monthList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
      return {
        currentMonth: monthList[0],
        monthList: monthList
      }
    },
    watch: {
      monthv (val, oldval) {
        this.monthv = val
      }
    },
    props: ['monthv']
  }
</script>

