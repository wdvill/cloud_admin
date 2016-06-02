<template>
<h3 class="modal-title text-muted text-center" v-if="is_delete">删除确认</h3>
<h3 class="modal-title text-muted text-center" v-else>编辑备注</h3>
<div class="yzj-size-16 yzj-top-distance50">
  <div class="row">
    <div class="col-xs-offset-1 col-xs-3 text-muted clear-right">
      <p>已选择时间</p>
    </div>
    <div class="col-xs-6 clear-left">
      {[shot_times | hourformat]} 小时
    </div>
  </div>
  <div class="row yzj-top-distance20">
    <template v-if="is_delete">
      <p class="col-xs-offset-1 col-xs-10 text-info yzj-height30-real">您的工作时间是您与需求方进行资金往来的凭证，删除之后将无法恢复，您确定要删除么？</p>
    </template>
    <template v-else>
      <div class="col-xs-offset-1 col-xs-3 text-muted clear-right">
      <p>备注名</p>
      </div>
      <div class="col-xs-6 clear-left">
        <textarea rows="5" class="form-control" v-model="remark" name="remark"></textarea>
      </div>
      <div class="clearfix"></div>
      <div id="remark-error" class="col-xs-offset-2" style="display:none"><error name="remark"></error></div>
    </template>
  </div>
  <div class="yzj-top-distance50 yzj-size-14 col-xs-offset-2">
    <div class="col-xs-4 clear-right" v-if="is_delete">
      <button type="button" class="btn btn-primary btn-block yzj-right-distance15" v-on:click="del()">确定</button>
    </div>
    <div class="col-xs-4 clear-right" v-else>
      <button type="button" class="btn btn-primary btn-block yzj-right-distance15" v-on:click="save()">修改</button>
    </div>
    <div class="col-xs-4 clear-right">
      <button type="button" :disabled="btnDisabled" class="btn btn-default btn-block yzj-right-distance15" v-on:click="cancel()">取消</button>
    </div>
    <div class="clearfix"></div>
  </div>
</div>

</template>
<script>
  import $ from 'jquery'
  import error from '../common/error_div.vue'
  import weekstoneService from '../../service/weekstone_service'
  export default {
    data () {
      return {
      }
    },
    components: {
      error
    },
    props: ['shot_times', 'shot_ids', 'remark', 'is_delete'],
    methods: {
      save () {
        if (this.remark === undefined || this.remark === '' || this.length > 30) {
          $('#remark-error').show()
          $('.error-div .errorMsg').html('请输入小于30字的备注')
          return
        }
        weekstoneService.update_screenshot({shot_ids: this.shot_ids, name: this.remark}).success((result) => {
          if (result.error_code === 0) {
            this.$dispatch('close', 'remark_modal')
            this.$dispatch('get_screenshot_list')
          } else {
            alert(result.msg)
          }
        })
      },
      del () {
        weekstoneService.delete_screenshot({shot_ids: this.shot_ids}).success((result) => {
          if (result.error_code === 0) {
            this.$dispatch('get_screenshot_list')
            this.$dispatch('close', 'remark_modal')
          } else {
            alert(result.msg)
          }
        })
      },
      cancel () {
        this.$dispatch('close', 'remark_modal')
      }
    }
  }
</script>
