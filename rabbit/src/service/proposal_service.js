import YWORK from '../utils/ywk.js'
export default {
  get_proposal_list (data) {
    return YWORK.getJson('/api/proposal', data, 'application/json')
  },
  add_proposal (data) {
    return YWORK.postJson('/api/proposal', data, 'application/json')
  },
  update_proposal (data) {
    return YWORK.putJson('/api/proposal', data, 'application/json')
  },
  get_message_list (data) {
    return YWORK.getJson('/api/proposal/message', data, 'application/json')
  }
}
