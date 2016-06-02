<template>
  <h3 class="modal-title text-muted text-center">冻结</h3>
  <div class="yzj-size-16 yzj-top-distance50" style="padding:0 10%">
    <p>您可使用冻结功能在不通知需求方的情况下冻结这个工作，该投标将移至"已冻结"模块，在工作关闭之前，您都可以重新激活该投标。</p>
    <p class="yzj-top-distance20"><input type="checkbox" v-model="remeber"/> 下次不再显示该提示</p>
    <div class="yzj-top-distance50 yzj-size-14 col-xs-offset-2">
      <div class="col-xs-4 clear-right">
        <button type="button" class="btn btn-primary btn-block yzj-right-distance15" id="refuse-btn" v-on:click="save()">确认</button>
      </div>
      <div class="col-xs-4 clear-right">
        <button type="button" class="btn btn-default btn-block yzj-right-distance15" data-dismiss="modal" v-on:click="cancel()">取消</button>
      </div>
      <div class="clearfix"></div>
    </div>
  </div>
</template>
<script>
  import proposal_service from '../../service/proposal_service'
  export default {
    created () {
      console.log(this.proposal_id, 'created')
    },
    data () {
      return {
      }
    },
    props: ['proposal_id'],
    methods: {
      save () {
        console.log(this.proposal_id, 'proposal_id')
        this.$dispatch('save', 'archive')
        proposal_service.update_proposal({proposal_id: this.proposal_id, operate: 'archive'})
          .success((data) => {
            if (data.error_code === 0) {
              this.$dispatch('save', 'freeze_modal')
              window.location.reload()
            } else {
              alert(data.msg)
            }
          })
      },
      cancel () {
        this.$dispatch('close', 'freeze_modal')
      }
    },
    watch: {
      proposal_id (value) {
        console.log(value, 'created')
      }
    }
  }
</script>

