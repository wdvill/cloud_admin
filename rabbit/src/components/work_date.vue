<template>
<div class="form-group">
  <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
    <span class="text-warning size-18">
      *
    </span>
    工作时间
  </label>
  <div class="col-xs-7">
    <div class="col-xs-5 clear-both">
      <date_year :yearv.sync="start_year"></date_year>
      <date_year :yearv.sync="end_year"></date_year>
    </div>
    <div class="col-xs-2 yzj-height30 text-center yzj-top-distance40">
      至
    </div>
    <div class="col-xs-5 clear-both">
      <date_month :monthv.sync="start_month" v-ref:startmonth></date_month>
      <date_month :monthv.sync="end_month" v-ref:endmonth></date_month>
    </div>
  </div>
</div>

<div class="form-group" v-show="errDate">
  <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
    <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
    aria-hidden="true">
    </span>
    {[errDate]}
  </div>
</div>
</template>
<script>
  import date_year from './date_year.vue'
  import date_month from './date_month.vue'

  export default {
    created () {
      this.setDefault(this.start_at, this.end_at)
    },
    data () {
      return {
        start_year: '',
        start_month: '',
        end_year: '',
        end_month: ''
      }
    },
    methods: {
      setDefault (start_at, end_at) {
        if (start_at) {
          let year_month = start_at.split('-')
          this.start_year = year_month[0]
          this.start_month = year_month[1]
        }
        if (end_at) {
          let year_month = end_at.split('-')
          this.end_year = year_month[0]
          this.end_month = year_month[1]
        }
      }
    },
    components: {
      date_year,
      date_month
    },
    watch: {
      start_at (value) {
        this.setDefault(value, null)
      },
      end_at (value) {
        this.setDefault(null, value)
      },
      start_year (value) {
        console.log('start year', value)
        this.start_at = [this.start_year, this.start_month].join('-')
      },
      start_month (value) {
        this.start_at = [this.start_year, this.start_month].join('-')
      },
      end_year (value) {
        console.log('end year', value)
        this.end_at = [this.end_year, this.end_month].join('-')
      },
      end_month (value) {
        this.end_at = [this.end_year, this.end_month].join('-')
      }
    },
    props: ['start_at', 'end_at']
  }

</script>
