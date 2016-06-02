import YWORK from '../utils/ywk.js'
export default {
  get_freelancer_list (data) {
    return YWORK.getJson('/api/client/freelancers', data, 'application/json')
  }
}
