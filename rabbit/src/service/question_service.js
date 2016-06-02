import YWORK from '../utils/ywk.js'

export default {
  get_question_list (data) {
    return YWORK.getJson('/api/question', data, 'application/json')
  }
}

