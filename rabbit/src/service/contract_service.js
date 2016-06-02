import YWORK from '../utils/ywk.js'
export default {
  select_bid (data) {
    return YWORK.getJson('/api/proposal', data, 'application/json')
  },
  update_bid (data) {
    return YWORK.putJson('/api/proposal', data, 'application/json')
  },
  select_contract (data) {
    return YWORK.getJson('/api/contract', data, 'application/json')
  },
  update_contract (data) {
    return YWORK.putJson('/api/contract', data, 'application/json')
  },
  send_message (data) {
    return YWORK.postJson('/api/proposal/message', data, 'application/json')
  },
  get_message_list (data) {
    return YWORK.getJson('/api/proposal/message', data, 'application/json')
  },
  add_favorite (data) {
    return YWORK.postJson('/api/favorite', data, 'application/json')
  },
  add_evaluate (data) {
    return YWORK.postJson('/api/contract/evaluate', data, 'application/json')
  },
  add_feedback (data) {
    return YWORK.postJson('/api/feedback', data, 'application/json')
  },
  contract_basic (data) {
    return YWORK.getJson('/api/contract/basic', data, 'application/json')
  },
  get_weekstone_contract_list (data) {
    return YWORK.getJson('/api/contract/weekstone', data, 'application/json')
  },
  contract_freelancers_list (data) {
    return YWORK.getJson('/api/contract/freelancers', data, 'application/json')
  }
}
