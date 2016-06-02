import YWORK from '../utils/ywk.js'

export default {
  /* 开发者报表查询 */
  get_freelancer_report (data) {
    return YWORK.getJson('/api/stats/freelancer', data, 'application/json')
  },
  /* 开发者统计数据 */
  get_freelancer_statis (data) {
    return YWORK.getJson('/api/stats/statis', data, 'application/json')
  },
  /* 需求者每周总结 */
  get_client_weekly (data) {
    return YWORK.getJson('/api/stats/weekly', data, 'application/json')
  },
  /* 需求者预算 */
  get_client_budget (data) {
    return YWORK.getJson('/api/stats/budget', data, 'application/json')
  },
  /* 需求者工时表 */
  get_client_timesheet (data) {
    return YWORK.getJson('/api/stats/timesheet', data, 'application/json')
  },
  /* 需求者交易记录 */
  get_client_trade (data) {
    return YWORK.getJson('/api/margin/record', data, 'application/json')
  }
}
