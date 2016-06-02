<template>
  <div class="col-xs-12 clear-both">
    <div class="col-xs-10 clear-left">
      <p class="text-primary">
        {[itemout.start_at]} -
        <span v-if="itemout.end_at!=''"> {[itemout.end_at]}</span>
        <span v-if="itemout.end_at==''"> 至今</span>
      </p>
      <p class="yzj-top-distance10 yzj-height30"><a href="javascript:;" v-on:click="project_comment">{[itemout.name]}</a></p>
      <p class="yzj-top-distance10 text-warning" v-if="itemout.status != 'finish' && itemout.status != 'service' && itemout.status != 'dispute'">进行中</p>
      <div v-if="(itemout.status == 'finish' || itemout.status == 'service' || itemout.status == 'dispute') && itemout.evaluate.team.content != undefined">
        <P class="yzj-top-distance10">
          <span class=""  v-yzj_star="average_score"></span>
          <span class="text-warning" style="margin-left: 15px" v-html="average_score.toFixed(1) + '分'"></span>
        </p>
        <p class="yzj-top-distance10" v-if="itemout.evaluate.team" v-text="itemout.evaluate.team.content"></p>
      </div>
      <div v-if="(itemout.status == 'finish' || itemout.status == 'service' || itemout.status == 'dispute') && itemout.evaluate.team.content == undefined">
        <p class="yzj-top-distance10 text-warning">需求方没有给出评价</p>
      </div>
    </div>
    <div class="col-xs-2 clear-both text-right" v-if="itemout.paymethod=='hour'">
      <p>用时{[itemout.shot_times | hourformat]}</p>
      <p class="yzj-top-distance15">{[itemout.hourly]}元/小时</p>
      <p class="yzj-top-distance15">赚取了{[itemout.total_amount]}元</p>
    </div>
    <div class="col-xs-2 clear-both text-right" v-if="itemout.paymethod=='fixed'">
      <p>赚取了{[itemout.total_amount]}元</p>
      <p class="yzj-top-distance15">固定项目价格</p>
    </div>
  </div>
  <div class="clearfix"></div>
  <div class="line02" v-if="islast=='no'"></div>
</template>
<script>
  export default {
    created () {
      // reset date
      let regex = /\d{4}-\d{2}-\d{2}/
      if (this.itemout.start_at !== '') {
        this.itemout.start_at = regex.exec(this.itemout.start_at)
      }
      if (this.itemout.end_at !== '') {
        this.itemout.end_at = regex.exec(this.itemout.end_at)
      }
    },
    props: ['itemout', 'index', 'islast'],
    computed: {
      average_score: function () {
        return (this.itemout.evaluate.team.quality + this.itemout.evaluate.team.exchange + this.itemout.evaluate.team.punctual + this.itemout.evaluate.team.cooper + this.itemout.evaluate.team.skill) / 5
      }
    },
    methods: {
      project_comment: function () {
        this.$dispatch('contract_detail', this.itemout)
      }
    }
  }
</script>
