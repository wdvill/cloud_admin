<template>
   <div class="modal fade bs-example-modal-lg choose-sort" id="employ" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
      <div class="modal-dialog contract-dialog">
          <div class="modal-content">
              <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close" id="education_close">
                      <span aria-hidden="true" class="yzj-size-30">&times;</span>
                  </button>
              </div>
              <div class="modal-body yzj-box yzj-height20 yzj-top-distance10">
                  <h3 class="modal-title text-muted text-center">您要为那份项目雇佣？</h3>
                  <div class="yzj-size-16 yzj-top-distance50">
                      <div class="yzj-top-distance50 yzj-size-14 col-xs-offset-1">
                          <p class="text-muted">项目列表</p>
                          <div class="form-group yzj-top-distance40">
                              <label class="control-label col-xs-3 clear-left text-left text-info">选择为哪份项目雇佣</label>
                              <div class="col-xs-9 clear-left">
                                  <div class="yzj-size-14">
                                      <div class="col-xs-12 clear-left">
                                          <select class="form-control" name="job_id" id="job_id" style="margin-top:-15px;" v-model="job_id">
                                              <option v-for="item in jobs" value="{[item.id]}">{[item.name]}</option>
                                          </select>
                                      </div>
                                      <div class="clearfix"></div>
                                  </div>
                              </div>
                              <input type="hidden" id="user_id">
                          </div>
                          <div class="clearfix"></div>
                          <div class="form-group yzj-top-distance10" v-show="error_msg">
                              <div class="col-xs-9 col-xs-offset-3 text-warning yzj-size-14">
                                  <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
                                  {[error_msg]}
                              </div>
                          </div>
                          <div class="form-group yzj-top-distance50">
                              <div class="col-xs-4 clear-right col-xs-offset-1">
                                  <button class="btn btn-primary btn-block yzj-right-distance15" @click="employ" id="btn-hire">雇佣</a>
                              </div>
                              <div class="col-xs-4 clear-right">
                                  <button type="button" class="btn btn-default btn-block yzj-right-distance15" data-dismiss="modal">取消</button>
                              </div>
                          </div>
                          <div class="clearfix"></div>
                      </div>
                  </div>
              </div>
              <div class="modal-footer yzj-top-distance10"></div>
          </div>
      </div>
  </div>
</template>

<script>
  import YWORK from '../../utils/ywk.js'
  
  export default {
    data () {
      return {
        job_id: '',
        jobs: [],
        error_msg: ''
      }
    },
    props: {
      uuid: [String, Number]
    },
    ready () {
      YWORK.getJson('/api/jobs/my', {status: 'normal'}, 'application/json').success((res) => {
        if (res.error_code === 0) {
          this.jobs = res.jobs
          this.job_id = res.jobs[0].id
        } else {
          this.error_msg = res.msg
        }
      })
    },
    methods: {
      // 雇佣
      employ () {
        if (this.job_id) {
          window.location.href = '/clients/offer/' + this.job_id + '/' + this.uuid + '/direct'
        } else {
          this.error_msg = '您没有选中任何项目'
          return false
        }
      }
    }
  }
</script>