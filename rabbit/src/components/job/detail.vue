<template>
  <p class="yzj-top-distance25 yzj-size-14 text-info">技能要求: &nbsp;
    <span class="label label-default label-pro-detail" v-for="skill in job.skills" v-text="skill"></span>
  </p>
  <p class="yzj-top-distance25 yzj-size-14 text-info" v-if="showItem.stage && job.stage">所处阶段: &nbsp;
    <span class="pro-item"><span class="pro-icon"><img src="/static/images/project/{[job.stage]}.png" /></span>{[job.stage | stageFrm]}</span>
  </p>
  <p class="yzj-top-distance25 yzj-size-14 text-info" v-if="showItem.platform && job.platforms && job.platforms.length > 0">应用平台: &nbsp;
    <span v-for="pl in job.platforms" class="pro-item"><span class="pro-icon"><img  src="/static/images/project/{[pl]}.png" /></span>{[pl]}</span>
  </p>
  <p class="yzj-top-distance25 yzj-size-14 text-info" v-if="showItem.language && job.languages && job.languages.length > 0">开发语言: &nbsp;
    <span class="label label-default label-pro-detail" v-for="item in job.languages" v-text="item"></span>
  </p>
  <p class="yzj-top-distance25 yzj-size-14 text-info" v-if="showItem.framework && job.frameworks && job.frameworks.length > 0">开发框架: &nbsp;
    <span class="label label-default label-pro-detail" v-for="item in job.frameworks" v-text="item"></span>
  </p>
  <p class="yzj-top-distance25 yzj-size-14 text-info" v-if="showItem.api && job.api && job.api.length > 0">集成 API: &nbsp;
    <span v-for="pl in job.api" class="pro-item"><span class="pro-icon"><img  src="/static/images/project/{[pl]}.png" /></span>{[pl | apiFrm]}</span>
  </p>
  <p class="yzj-top-distance25 yzj-size-14 text-info" v-if="job.attachment && job.attachment.id">附件文档: &nbsp;
    <a href="{[job.attachment.path]}" download="{[job.attachment.name]}" class="pro-item"><span class="file"><img src="/static/images/project/file.png" /></span>{[job.attachment.name]}</a>
  </p>
</template>

<script>
  import localize from '../../filters/localize'
  import Vue from 'vue'
  import YWORK from '../../utils/ywk.js'

  Vue.use(localize)
  // 所处阶段过滤器
  Vue.filter('stageFrm', function (value) {
    let stage = ''
    switch (value) {
      case 'design':
        stage = '有设计'
        break
      case 'introduction':
        stage = '有详细的需求说明'
        break
      case 'idea':
        stage = '只有一个想法'
        break
      default:
        stage = '啥也没有'
        break
    }
    return stage
  })
  Vue.filter('apiFrm', function (value) {
    let stage = ''
    switch (value) {
      case 'social':
        stage = '社交API'
        break
      case 'pay':
        stage = '支付API'
        break
      case 'storage':
        stage = '存储API'
        break
      default:
        stage = '其他'
        break
    }
    return stage
  })

  export default {
    data () {
      return {
        showItem: {}
      }
    },
    props: ['job'],
    ready () {
      YWORK.getJson('/api/category/options', {
        category_id: this.job.category.id
      }).success((res) => {
        if (res.error_code === 0) {
          this.$set('showItem', res.options)
        }
      })
    }
  }
</script>
<style lang="sass">
  .pro-item{
    margin-right: 20px;
    
    .pro-icon{
      padding: 5px;
      border: solid 1px #ededed;
      border-radius: 2px;
      background-color: #f7f7f7;
      margin-right: 5px;
      
      img{
        width: 12px;
        height: 12px;
      }
    }
    .file {
      margin-right: 5px;
      img{
        width: 15px;
        height: 15px;
      }
    }
  }
</style>

