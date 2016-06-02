import YWORK from '../utils/ywk.js'
export default {
  get_weekstone_pay (data) {
    return YWORK.getJson('/api/weekstone/pay', data, 'application/json')
  },
  update_weekstone (data) {
    return YWORK.putJson('/api/weekstone/pay', data, 'application/json')
  },
  post_weekstone (data) {
    return YWORK.postJson('/api/weekstone/pay', data, 'application/json')
  },
  get_weekstone_time (data) {
    return YWORK.getJson('/api/weekstone/time', data, 'application/json')
  },
  get_screenshot_list (data) {
    return YWORK.getJson('/api/weekstone/screenshot', data, 'application/json')
  },
  add_screenshot (data) {
    return YWORK.postJson('/api/weekstone/screenshot', data, 'application/json')
  },
  update_screenshot (data) {
    return YWORK.putJson('/api/weekstone/screenshot', data, 'application/json')
  },
  delete_screenshot (data) {
    return YWORK.deleteJson('/api/weekstone/screenshot', data, 'application/json')
  }
}
