<template>
  <div class="yzj-box" v-bind:class="{'yzj-top-distance30': top}">
    <p class="text-muted yzj-size-16">需求方简介</p>
    <p class="yzj-top-distance15 yzj-size-16">需求方：{[info.name]}</p>

    <p class="text-muted yzj-top-distance30 yzj-size-14">{[info.location]}</p>
    <p class="yzj-top-distance15 yzj-size-14">注册时间：{[info.reg_at]}</p>

    <p class="yzj-top-distance10 yzj-size-14">
    	<star user-class="yzj-right-distance10 star-list" :aver-score="info.aver_score" :eveluate-num="info.eveluate_num"></star>
      <span >（{[info.aver_score]}）{[info.eveluate_num]}条评论</span>
    </p>
    <p class="yzj-top-distance30 yzj-size-14 clearfix">
      <span class="pull-left">总消费</span>
      <span class="pull-right text-muted">￥{[info.total_amount]}</span>
    </p>
    <p class="line"></p>
    <p class="yzj-top-distance30 yzj-size-14 clearfix">
      <span class="pull-left">发布工作</span>
      <span class="pull-right text-muted">{[info.jobs]}</span>
    </p>
    <p class="line"></p>
    <p class="yzj-top-distance30 yzj-size-14 clearfix">
      <span class="pull-left">雇佣人数</span>
      <span class="pull-right text-muted">{[info.hires]}</span>
    </p>
    <p class="line"></p>
    <p class="yzj-top-distance30 yzj-size-14 clearfix">
      <span class="pull-left">公开工作</span>
      <span class="pull-right text-muted">{[info.open_jobs]}</span>
    </p>
  </div>
</template>

<script>
  import YWORK from '../../utils/ywk.js'
  import star from '../job/star.vue'
  
  export default {
    data () {
      return {
        box: true
      }
    },
    props: ['team_id', 'top'],
    watch: {
      team_id (value) {
        let _self = this
        if (value) {
          YWORK.getJson('/api/user/client', {team_id: value}, 'application/json')
            .success((data) => {
              if (data.error_code === 0) {
                _self.$set('info', data.info)
              }
            })
        }
      }
    },
    components: {
      star
    }
  }
  
</script>
