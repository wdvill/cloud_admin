<template>
<modal class="modal fade bs-example-modal-lg" role="dialog" id="proposal_detail">
  <div class="modal-dialog contract-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true" class="yzj-size-30">&times;</span>
        </button>
      </div>
      <div class="modal-body yzj-box yzj-height20 yzj-top-distance10 yzj-bot-distance50">
        <h3 class="modal-title text-muted text-center">服务方报价</h3>
        <div class="yzj-box col-xs-12 clear-both yzj-size-16" style="padding-left: 50px;">
          <div class="form-group">
            <div class="col-xs-4 clear-left text-left">
              <img class="img-circle" width="69" height="69" v-bind:src="item.avatar">
            </div>
            <div class="col-xs-8 clear-left text-info">
              <p class="yzj-height40">{[item.name]}</p>
              <a href="javascript:;" onclick="window.open('/freelancers/{[item.id]}')" class="text-warning">查看个人档案</a>
            </div>
          </div>
          <div class="clearfix"></div>
          <div class="form-group yzj-top-distance30">
            <div class="col-xs-4 clear-left text-left">报价</div>
            <div class="col-xs-8 clear-left text-info">{[item.price]}元<span v-if="item.paymethod === 'hour'">/小时</span></div>
          </div>
          <div class="clearfix"></div>
          <div class="form-group yzj-top-distance30" v-if="item.paymethod === 'fixed'">
            <div class="col-xs-4 clear-left text-left">预计完成时间</div>
            <div class="col-xs-8 clear-left text-info" v-if="item.duration==1">6个月以上</div>
            <div class="col-xs-8 clear-left text-info" v-if="item.duration==2">3到6个月</div>
            <div class="col-xs-8 clear-left text-info" v-if="item.duration==3">1到3个月</div>
            <div class="col-xs-8 clear-left text-info" v-if="item.duration==4">一个月以内</div>
            <div class="col-xs-8 clear-left text-info" v-if="item.duration==5">一周以内</div>
            <div class="clearfix"></div>
          </div>
          <div class="form-group yzj-top-distance30">
            <div class="col-xs-4 clear-left text-left">求职信</div>
            <div class="col-xs-8 clear-left text-info yzj-height30">{[item.message]}</div>
          </div>
          <div class="clearfix"></div>
          <div class="form-group yzj-top-distance30" v-if="item.attachment.path">
            <div class="col-xs-4 clear-left text-left">附件</div>
            <div class="col-xs-8 clear-left text-info"><a href="{[item.attachment.path]}">{[item.attachment.name]}</a></div>
            <div class="clearfix"></div>
          </div>
          <div class="form-group yzj-top-distance30" v-if="messages.length>0">
            <p>消息</p>
            <ul class="message-list yzj-top-distance10" style="padding-left:0;max-height:100px;overflow-y:auto">
              <li v-for="i in messages">
                <i v-if="i.name==item.name"></i>
                <i v-if="i.name!=item.name" class="active"></i>
                <p>
                  <span v-if="i.name!=item.name" class="text-warning yzj-size-14" style="padding-right:10px">{[i.name]}</span>
                  <span v-if="i.name==item.name" class="text-warning yzj-size-14" style="padding-right:10px">我</span>
                  {[i.create_at]}
                </p>
                <p v-bind:class="$index==messages.length-1?'timeline':'activeline'">{[i.content]}</p>
                <div class="clearfix"></div>
              </li>
            </ul>
          </div>
        </div>
        <div class="clearfix"></div>
      </div>
    </div>
  </div>
</modal>
</template>

<script>
  export default {
    props: ['item', 'messages']
  }
</script>
