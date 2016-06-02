import YWORK from '../utils/ywk.js'

export default {
  send_feedback (data) {
    return YWORK.postJson('/api/feedback', data, 'application/json')
  }
}

