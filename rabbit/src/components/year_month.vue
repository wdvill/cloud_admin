<template>
  <div class="row">
    <div class="col-xs-6">
      <date_year :yearv.sync="year" v-ref:year></date_year>
    </div>
    <div class="col-xs-6">
      <date_month :monthv.sync="month" v-ref:month></date_month>
    </div>
  </div>
</template>

<script>
  import date_year from './date_year.vue'
  import date_month from './date_month.vue'
  export default {
    data () {
      return {
        year: '',
        month: ''
      }
    },
    props: ['date'],
    created () {
      if (this.date) {
        let dates = this.date.split('-')
        this.year = dates[0]
        this.month = dates[1]
      }
    },
    methods: {
      getValue () {
        return [this.year, this.month].join('-')
      }
    },
    watch: {
      date (val, oldval) {
        let dates = val.split('-')
        this.year = dates[0]
        this.month = dates[1]
      }
    },
    components: {
      date_year,
      date_month
    }
  }
</script>

