<template>
  <div class="work-log-suspend text-info">
    <div class="auto-log">
      <img :src="item.attachment" style="width:230px" alt="工作日志截屏">
    </div>
    <div class="yzj-top-distance20">
      <div class="col-xs-6 clear-both">
        <p>窗口名称</p>
      </div>
      <div class="col-xs-6 clear-both">
        <p v-text="item.name"></p>
      </div>
      <div class="clearfix"></div>
    </div>
    <div class="yzj-top-distance20">
      <div class="col-xs-6 clear-both">
        <p>截屏时间</p>
      </div>
      <div class="col-xs-6 clear-both">
        <p v-text="item.shot_at | formatTime"></p>
      </div>
      <div class="clearfix"></div>
    </div>
    <div class="yzj-top-distance20">
      <div class="col-xs-6 clear-both">
        <p>备注</p>
      </div>
      <div class="col-xs-6 clear-both">
        <p v-text="item.description"></p>
      </div>
      <div class="clearfix"></div>
    </div>
    <div class="yzj-top-distance20 work-log-component" style="background:none;padding:0;margin-top:30px">
      <div class="col-xs-6 clear-both">
        <p>活跃度</p>
      </div>
      <div class="col-xs-6 clear-both log-ft" style="clear:none;padding:0">
        <ul class="active-state">
          <li v-for="n in 10" :class="{'active': n < parseInt(item.activity/10, 10)}"></li>
        </ul>
      </div>
      <div class="clearfix"></div>
    </div>
    <div class="arrow">
      <em class="arrow_line"></em>
    </div>
  </div>
</template>
<script>
  require('../assets/sass/components/work-log.scss')
  export default {
    data () {
      return {
      }
    },
    props: ['item', 'contract_id'],
    methods: {
    }
  }
</script>
