import YWORK from '../utils/ywk.js'

export default {
  get_job_list (data) {
    return YWORK.getJson('/api/jobs', data, 'application/json')
  },
  get_job (data) {
    return YWORK.getJson('/api/jobs', data, 'application/json')
  },
  update_job (data) {
    return YWORK.putJson('/api/jobs/status', data, 'application/json')
  },
  add_job (data) {
    return YWORK.postJson('/api/jobs', data, 'application/json')
  },
  search (data) {
    return YWORK.postJson('/api/jobs/search', data, 'application/json')
  },
  get_job_proposal (data) {
    return YWORK.getJson('/api/jobs/proposal', data, 'application/json')
  },
  get_jobs_recommand (data) {
    return YWORK.getJson('/api/jobs/freelancers/recommand', data, 'application/json')
  },
  get_jobs_my (data) {
    return YWORK.getJson('/api/jobs/my', data, 'application/json')
  }
}
