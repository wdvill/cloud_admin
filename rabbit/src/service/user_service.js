import YWORK from '../utils/ywk.js'

export default {
  get_category_list (data) {
    return YWORK.getJson('/api/user/category', data, 'application/json')
  },
  get_client_info (data) {
    return YWORK.getJson('/api/user/client', data, 'application/json')
  },
  get_user_profile (data) {
    return YWORK.getJson('/api/user/profile', data, 'application/json')
  },
  get_user_portfolio (data) {
    return YWORK.getJson('/api/portfolio', data, 'application/json')
  },
  get_user_employment (data) {
    return YWORK.getJson('/api/employment', data, 'application/json')
  },
  get_user_education (data) {
    return YWORK.getJson('/api/education', data, 'application/json')
  },
  get_user_work (data) {
    return YWORK.getJson('/api/freelancers/contract', data, 'application/json')
  },
  update_user_profile (data) {
    return YWORK.putJson('/api/user/profile', data, 'application/json')
  },
  add_user_verify (data) {
    return YWORK.postJson('/api/user/verify', data, 'application/json')
  },
  add_client_verify (data) {
    return YWORK.postJson('/api/client/verify', data, 'application/json')
  },
  add_freelancer (data) {
    return YWORK.postJson('/api/user/freelancer', data, 'application/json')
  },
  get_notify_setting (data) {
    return YWORK.getJson('/api/notify/setting', data, 'application/json')
  },
  add_notify_setting (data) {
    return YWORK.postJson('/api/notify/setting', data, 'application/json')
  },
  add_discover (data) {
    return YWORK.getJson('/api/freelancers/discover', data, 'application/json')
  }
}
