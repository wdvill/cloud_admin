import YWORK from '../utils/ywk.js'
export default {
  get_category_list (data) {
    return YWORK.postJson('/api/category', data, 'application/json')
  },
  update_user_category (data) {
    return YWORK.postJson('/api/user/category', data, 'application/json')
  }
}
