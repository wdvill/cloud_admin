<template>
  <select class="form-control select-control" v-model="yearv">
    <option v-for="year in years" v-bind:value="year">{[year]}</option>
  </select>
</template>

<script>
  import datetime from '../utils/datetime'
  export default {
    created () {
      if (!this.yearv) {
        this.yearv = this.currentYear
      }
    },
    data () {
      let yearList = datetime.getYearList()
      return {
        currentYear: yearList[0],
        years: yearList
      }
    },
    props: ['yearv']
  }
</script>
