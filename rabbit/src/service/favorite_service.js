import YWORK from '../utils/ywk.js'

export default {
  add_favorite (data) {
    return YWORK.postJson('/api/favorite', data, 'application/json')
  },
  delete_favorite (data) {
    return YWORK.deleteJson('/api/favorite', data, 'application/json')
  },
  get_favorite_list (data) {
    return YWORK.getJson('/api/favorite', data, 'application/json')
  }
}
