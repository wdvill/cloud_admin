import YWORK from '../utils/ywk.js'
export default {
  verifycode (data) {
    return YWORK.postJson('/api/verifycode', data, 'application/json')
  },
  address (data) {
    return YWORK.getJson('/api/address', data, 'application/json')
  },
  category (data) {
    return YWORK.postJson('/api/category', data, 'application/json')
  },
  question (data) {
    return YWORK.getJson('/api/question', data, 'application/json')
  },
  checkpwd (data) {
    return YWORK.postJson('/api/user/password/verify', data, 'application/json')
  },
  recommend_freelancers (data) {
    return YWORK.getJson('/api/freelancers/recommand', data, 'application/json')
  }
}
