import YWORK from '../utils/ywk.js'
export default {
  get_profile (data) {
    return YWORK.getJson('/api/user/profile', data, 'application/json')
  },
  put_profile (data) {
    return YWORK.putJson('/api/user/profile', data, 'application/json')
  }
}
