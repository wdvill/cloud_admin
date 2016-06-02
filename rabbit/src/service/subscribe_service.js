import YWORK from '../utils/ywk.js'

export default {
  unsubscribe (data) {
    return YWORK.deleteJson('/api/subscribe', data, 'application/json')
  },
  get_subscribe_list (data) {
    return YWORK.getJson('/api/subscribe', data, 'application/json')
  }
}

