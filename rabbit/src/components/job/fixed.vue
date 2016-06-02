<template>
  <div class="yzj-top-distance20 text-info yzj-size-14">
    <span class="yzj-right-distance45">
      定价付费 丨 {[job.budget]} 元
    </span>
    <span class="yzj-right-distance45">难度:{[job.level | level]}</span>
  </div>
</template>

<script>
  import localize from '../../filters/localize'
  import Vue from 'vue'

  Vue.use(localize)

  export default {
    data () {
      return {
      }
    },
    props: ['job']
  }
</script>
