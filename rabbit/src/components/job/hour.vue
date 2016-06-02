<template>
  <div class="yzj-top-distance20 text-info yzj-size-14">
    <span class="yzj-right-distance45">
      按工时付费 丨 {[job.level | level 'price']}
    </span>
    <span class="yzj-right-distance45">难度:{[job.level | level]}</span>
    <span class="yzj-right-distance45">
      周期:{[job.duration | duration]}</span>
    <span class="yzj-right-distance45">工作量:{[job.workload | workloadC]}</span>
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
