<template>
  <div class="modal fade bs-example-modal-lg choose-sort" id="send-reward" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
      <div class="modal-dialog contract-dialog">
        <div class="modal-content">
          <form class="form-horizontal yzj-top-distance20">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-label="Close" id="education_close">
                <span aria-hidden="true" class="yzj-size-30">&times;</span>
              </button>
            </div>
            <div class="modal-body yzj-box yzj-height20 yzj-top-distance10">
              <h3 class="modal-title text-muted text-center">发放奖金</h3>
              <div class="yzj-size-16 yzj-top-distance50" style="padding-left:100px;padding-right: 100px;">
                <p></p>
                <div class="form-group">
                  <label class="control-label col-xs-3 text-left">
                  <span class="icon-required-star icon-distance text-warning"> *</span>
                  付款类型
                  </label>
                  <div class="col-xs-8">
                    <select id="select01" class="form-control" v-model="money_type">
                      <option value="0" selected="">请选择奖金类型</option>
                      <option value="1">奖金</option>
                      <option value="2">费用报销</option>
                    </select>
                    <p class="text-warning yzj-size-14 yzj-top-distance10">{[error_type]}</p>
                  </div>
                </div>
                <div class="form-group">
                  <label class="control-label col-xs-3 text-left">
                  <span class="icon-required-star icon-distance text-warning"> *</span>
                  金额
                  </label>
                  <div class="col-xs-8">
                    <input id="money" type="number" min="1" class="form-control" v-model="money" autofoces="autofoces">
                    <p class="text-warning yzj-size-14 yzj-top-distance10">{[error_money]}</p>
                  </div>
                </div>
                <div class="form-group">
                  <label class="control-label col-xs-3 text-left">描述</label>
                  <div class="col-xs-8">
                    <textarea rows="4" class="form-control" v-model="description"  autofoces="autofoces"></textarea>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer yzj-top-distance10">
              <div class="form-group">
                <div class="col-xs-3 clear-right col-xs-offset-3">
                  <button class="btn btn-primary btn-block yzj-right-distance15" type="button" v-on:click="money_submit()">确认
                  </button>
                </div>
                <div class="col-xs-3 clear-right">
                  <button data-dismiss="modal" class="btn btn-default btn-block yzj-right-distance15" type="button">取消
                  </button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    <strap-alert :msg="errMsg" show-type="danger" :show-alert="showAlert"></strap-alert>
</template>

<script>
  import strapAlert from '../strap_alert.vue'
  import YWORK from '../../utils/ywk.js'
  
  export default {
    data () {
      return {
        errMsg: '',
        showAlert: false,
        money_type: 0,
        error_type: '',
        error_money: '',
        money: '',
        description: ''
      }
    },
    props: {
      freelancerId: [String, Number],
      contractId: [String, Number]
    },
    methods: {
      money_submit () {
        if (this.money === '' || this.money === '0') {
          this.$set('error_money', '奖金金额必填且必须大于0')
          this.$set('is_submit', false)
        }
        if (this.is_submit === true) {
          YWORK.postJson('/api/contract/bonus', {amount: this.money, freelancer_id: this.freelancerId, contract_id: this.contractId, description: this.description}, 'application/json').success((data) => {
            if (data.error_code === 0) {
              window.location.href = '/contracts/' + data.contract_id + '/bonus/' + data.trade_no
            } else {
              this.errMsg = data.msg
              this.showAlert = true
            }
          })
        }
      }
    },
    watch: {
      money_type: {
        handler (val, oldVal) {
          if (val === '0') {
            this.$set('error_type', '请选择奖金类型')
            this.$set('is_submit', false)
          } else {
            this.$set('error_type', '')
            this.$set('is_submit', true)
          }
        }
      },
      money: {
        handler (val, oldVal) {
          if (val === '' || val === '0') {
            this.$set('error_money', '奖金金额必填且必须大于0')
            this.$set('is_submit', false)
          } else {
            this.$set('error_money', '')
            this.$set('is_submit', true)
          }
        }
      }
    },
    components: {
      strapAlert
    }
  }
</script>
