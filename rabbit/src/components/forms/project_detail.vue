<template>
  <div class="col-xs-10 col-xs-offset-1">
    <h3 class="modal-title text-muted text-center">项目经验详情</h3>
    <div class="yzj-top-distance20 text-muted">
        <p class="yzj-size-16 yzj-top-distance15">项目名称：<span v-text="project_detail.name"></span></p>
        <p class="yzj-size-14 yzj-top-distance15" v-html="project_detail.end_at | year_month"></p>
        <p class="yzj-size-14 yzj-top-distance15">
        <span class="yzj-right-distance10" v-text="project_detail.category.parent_name"></span>
        <span class="yzj-right-distance10" v-text="project_detail.category.name"></span>
      </p>
    </div>
    <div class="line"></div>
    <div class="yzj-top-distance20">
      <p class="yzj-size-16 yzj-top-distance15">项目简介：<span v-text="project_detail.detail"></span></p>
      <p class="yzj-size-14 yzj-top-distance15 text-warning"><a :href="project_detail.link" target="_blank" v-text="project_detail.link"></a></p>
      <p class="yzj-size-14 yzj-top-distance15" v-if="project_detail.picture.path!=''">
        <img :src="project_detail.picture.path" :alt="{[project_detail.picture.name]}" width="150" height="150"/>
      </p>
    </div>
    <div class="clearfix"></div>
    <div class="yzj-top-distance50"></div>
  </div>
</template>
<script>
  export default {
    props: ['project_detail'],
    created () {
    },
    methods: {
      cancel () {
        this.$dispatch('close', 'project_modal')
      }
    }
  }
</script>