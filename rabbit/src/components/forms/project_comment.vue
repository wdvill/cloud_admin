<template>
  <div class="col-xs-10 col-xs-offset-1">
    <p class="modal-title text-muted yzj-size-18"><strong v-text="work_detail.name"></strong></p>
    <p class="text-muted yzj-top-distance40">
      {[work_detail.start_at]} -
        <span v-if="work_detail.end_at!=''"> {[work_detail.end_at]}</span>
        <span v-if="work_detail.end_at==''"> 至今</span>
    </p>
    <div class="line"></div>
    <div class="yzj-top-distance20 text-muted">
      <div class="col-xs-7 text-left clear-both">
        <strong>需求方评价</strong>
      </div>
      <div class="col-xs-5 clear-both text-right" v-if="(work_detail.status == 'finish' || work_detail.status == 'service' || work_detail.status == 'dispute') && work_detail.evaluate.team.content != undefined">
          <span v-yzj_star="average_score"></span>
          <span class="text-warning" style="margin-left: 15px" v-html="average_score.toFixed(1) + '分'"></span>
      </div>
    </div>
    <div v-if="(work_detail.status == 'finish' || work_detail.status == 'service' || work_detail.status == 'dispute') && work_detail.evaluate.team.content != undefined">
      <p class="yzj-top-distance50 modal-title text-muted yzj-size-14" v-text="work_detail.evaluate.team.content">
      </p>
      <div class="yzj-top-distance20 text-left">
        <div class="col-xs-6 clear-both yzj-top-distance20">
          <div class="col-xs-6 clear-both">能力</div>
          <div class="col-xs-6 clear-both"><strong v-html="work_detail.evaluate.team.skill.toFixed(1)"></strong></div>
        </div>
        <div class="col-xs-6 clear-both yzj-top-distance20">
          <div class="col-xs-6 clear-both">完成质量</div>
          <div class="col-xs-6 clear-both"><strong v-html="work_detail.evaluate.team.quality.toFixed(1)"></strong></div>
        </div>
      </div>
      <div class="yzj-top-distance20 text-left">
        <div class="col-xs-6 clear-both yzj-top-distance20">
          <div class="col-xs-6 clear-both">沟通</div>
          <div class="col-xs-6 clear-both"><strong v-html="work_detail.evaluate.team.exchange.toFixed(1)"></strong></div>
        </div>
        <div class="col-xs-6 clear-both yzj-top-distance20">
          <div class="col-xs-6 clear-both">交付时间</div>
          <div class="col-xs-6 clear-both"><strong v-html="work_detail.evaluate.team.punctual.toFixed(1)"></strong></div>
        </div>
      </div>
      <div class="yzj-top-distance20 text-left">
        <div class="col-xs-6 clear-both yzj-top-distance20">
          <div class="col-xs-6 clear-both">可用性</div>
          <div class="col-xs-6 clear-both"><strong v-html="work_detail.evaluate.team.cooper.toFixed(1)"></strong></div>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="clearfix"></div>
      <div v-if="work_detail.status != 'finish' && work_detail.status != 'service' && work_detail.status != 'dispute'">
        <p class="yzj-top-distance30 modal-title text-left yzj-size-14">项目正在进行中</p>
      </div>
      <div v-else>
        <p class="yzj-top-distance30 modal-title text-left yzj-size-14">需求方并没有给出评价</p>
      </div>
    </div>
    <div class="clearfix"></div>
    <div class="yzj-top-distance50"></div>
  </div>
</template>
<script>
  export default {
    props: ['work_detail'],
    created () {
      let regex = /\d{4}-\d{2}-\d{2}/
      if (this.work_detail.start_at !== '') {
        this.work_detail.start_at = regex.exec(this.work_detail.start_at)
      }
      if (this.work_detail.end_at !== '') {
        this.work_detail.end_at = regex.exec(this.work_detail.end_at)
      }
    },
    computed: {
      average_score: function () {
        return (this.work_detail.evaluate.team.quality + this.work_detail.evaluate.team.exchange + this.work_detail.evaluate.team.punctual + this.work_detail.evaluate.team.cooper + this.work_detail.evaluate.team.skill) / 5
      }
    },
    methods: {
      cancel () {
        this.$dispatch('close', 'comment_modal')
      }
    }
  }
</script>