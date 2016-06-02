<template>
  <div class="modal fade bs-example-modal-lg choose-sort" id="finish-hour-contract" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
      <div class="modal-dialog contract-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" id="education_close">
              <span aria-hidden="true" class="yzj-size-30">&times;</span>
            </button>
          </div>
          <div class="modal-body yzj-box yzj-height20 yzj-top-distance10"> 
            <h3 class="modal-title text-muted text-center">结束合同</h3> 
            <div class="yzj-size-16 yzj-top-distance50" style="padding-left:100px;padding-right: 100px;"> 
              <div v-if="contract.status == 'carry'">
                <div v-if="contract.stones[contract.stones.length-1].shot_times == 0">
                  <p class="yzj-top-distance20 text-center">
                  本周服务方已完成工作0小时，是否确定结束合同吗？
                  </p>
                  <div class="yzj-top-distance50 yzj-size-14 col-xs-offset-2">
                    <div class="col-xs-4 clear-right">
                      <button type="button" class="btn btn-primary btn-block yzj-right-distance15" v-on:click="finish_confirm_nowork()">确定结束</button>
                    </div>
                    <div class="col-xs-4 clear-right">
                      <button type="button" class="btn btn-default btn-block yzj-right-distance15" data-dismiss="modal">取消</button>
                    </div>
                    <div class="clearfix"></div>
                  </div>
                </div>
                <div v-if="contract.stones[contract.stones.length-1].shot_times > 0">
                  <p class="yzj-top-distance20">本周服务方已完成工作35小时，按照¥ 300/小时计算，需支付¥ 10500，是否同意支付已完成工作的费用？</p>
                
                  <div class="text-info yzj-size-14 yzj-top-distance30 yzj-height40">
                    <input type="radio" value='true' v-model="is_pay"/>同意支付已完成工作费用，并结束合同。
                  </div>
                  <div class="text-info yzj-size-14 yzj-top-distance10 yzj-height40">
                    <input type="radio" value="false" v-model="is_pay">不同意支付已完成工作费用，进入争议流程，申请客服介入，并结束合同。
                  </div>
                  <div class="yzj-top-distance50 yzj-size-14 col-xs-offset-2">
                    <div class="col-xs-4 clear-right">
                      <button type="button" class="btn btn-primary btn-block yzj-right-distance15" v-on:click="finish_confirm()">确定结束</button>
                    </div>
                    <div class="col-xs-4 clear-right">
                      <button type="button" class="btn btn-default btn-block yzj-right-distance15" data-dismiss="modal">取消</button>
                    </div>
                    <div class="clearfix"></div>
                  </div>
                </div>
              </div>
              <div v-if="contract.status == 'pause'">
                <p class="yzj-top-distance20">您当前的合同处于暂停状态，确定要结束吗？
                </p>
                <div class="yzj-top-distance50 yzj-size-14 col-xs-offset-2">
                  <div class="col-xs-4 clear-right">
                    <button type="button" class="btn btn-primary btn-block yzj-right-distance15" v-on:click="finish_confirm_nowork()">确定结束</button>
                  </div>
                  <div class="col-xs-4 clear-right">
                    <button type="button" class="btn btn-default btn-block yzj-right-distance15" data-dismiss="modal">取消</button>
                  </div>
                  <div class="clearfix"></div>
                </div>
              </div>
            </div>
          </div>
            <div class="modal-footer yzj-top-distance10"></div>
        </div>
      </div>
    </div>
    <strap-alert :msg="errMsg" show-type="danger" :show-alert="showAlert"></strap-alert>
</template>

<script>
  import $ from 'jquery'
  import strapAlert from '../strap_alert.vue'
  import YWORK from '../../utils/ywk.js'

  export default {
    data: {
      return {
        errMsg: '',
        showAlert: false
      }
    },
    props: {
      contract: [Object]
    }
    methods: {
      finish_confirm () {
        let data = {}
        if (this.is_pay === '') {
          alert('请选择是否同意为已完成的工作付费')
          return
        } else {
          data = {
            contract_id: this.contract.id,
            status: 'finish',
            is_pay: this.is_pay
          }
        }
        YWORK.putJson('/api/contract', data, 'application/json').success((data) => {
          if (data.error_code === 0) {
            $('#finish-hour-contract').modal('hide')
            window.location.href = '/contracts/' + this.contract.id + '/evaluate'
          }
        })
      },
      finish_confirm_nowork () {
        let data = {
          contract_id: this.contract.id,
          status: 'finish',
          is_pay: false
        }
        YWORK.putJson('/api/contract', data, 'application/json').success((data) => {
          if (data.error_code === 0) {
            $('#finish-hour-contract').modal('hide')
            window.location.href = '/contracts/' + this.contract.id + '/evaluate'
          }
        })
      }
    },
    components: {
      strapAlert
    }
  }
</script>