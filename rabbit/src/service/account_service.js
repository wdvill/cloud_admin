import YWORK from '../utils/ywk.js'
export default {
  get_account_list (data) {
    return YWORK.getJson('/api/margin/withdraw/accounts', data, 'application/json')
  },
  update_account_withdraw (data) {
    return YWORK.postJson('/api/margin/withdraw', data, 'application/json')
  },
  update_account_recharge (data) {
    return YWORK.postJson('/api/margin/deposit', data, 'application/json')
  },
  get_record_list (data) {
    return YWORK.getJson('/api/margin/record', data, 'application/json')
  }
}
