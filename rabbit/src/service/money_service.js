import YWORK from '../utils/ywk.js'
export default {
  post_bonus (data) {
    return YWORK.postJson('/api/contract/bonus', data, 'application/json')
  }
}
