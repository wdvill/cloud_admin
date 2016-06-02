<template>
  <div class="container yzj-top-distance50" v-if="!hasWork">
    <h3 class="text-muted">工作日志</h3>
    <div class="yzj-box yzj-top-distance20">
      <div class="yzj-top-distance30"></div>
      <div class="col-xs-1"></div>
      <div class="col-xs-1 clear-both">
        <img src="/static/images/daily-log-icon.png"/>
      </div>
      <div class="col-xs-8 yzj-size-16 text-muted">
        <p>您现在还没有进行中的时薪制工作。</p>
        <p class="yzj-top-distance15">请使用找工作功能，寻找并申请新工作</p>
      </div>
      <div class="col-xs-2 text-right">
        <a href="/find-work-home" class="btn btn-primary btn-block">找工作</a>
      </div>
      <div class="clearfix"></div>
    </div>
  </div>
</template>