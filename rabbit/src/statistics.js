import Vue from 'vue'
import $ from 'jquery'
import profile from './service/profile_service'
import modal from './components/common/modal.vue'
import workload from './components/forms/workload.vue'
import mixin_modal from './mixins/modal.js'
import reportService from './service/report_service'

Vue.config.delimiters = ['{[', ']}']
/* eslint-disable no-new */
var vue = new Vue({
  el: '#container',
  data: {
    workload: '',
    completeness: '',
    data: ''
  },
  mixins: [mixin_modal],
  components: {
    modal,
    workload
  },
  ready () {
    this.get_profile()
    $('#highchart').highcharts({
      chart: {
        type: 'pie',
        events: {
          load: function () {
            let series = this.series
            reportService.get_freelancer_statis().success((result) =>{
              if (result.error_code === 0) {
                vue.data = result.data
                let d = []
                d.push(result.data.coop_rate * 100)
                d.push(100 - result.data.coop_rate * 100)
                series[0].setData(d)
                let now = new Date().getMonth() + 1 + '-' + new Date().getDate()
                let subtitle = {
                  text: '<p class="text-info yzj-size-16">更新时间：' + (result.data.update_at === '' ? now : (result.data.update_at).substr(5, 5)) + '</p>',
                  verticalAlign: 'bottom',
                  y: 8,
                  useHTML: true
                }
                this.setTitle(null, subtitle)
                if (result.data.coop_rate > 0) {
                  let title = {
                    text: '<div class="text-center"><p class="text-warning yzj-size-14"><strong>' + (result.data.coop_rate * 100).toFixed(2) + '%</strong></p><p class="text-info yzj-size-16">工作成功率</p></div>',
                    verticalAlign: 'middle',
                    y: -10,
                    useHTML: true,
                    fontFamily: '微软雅黑'
                  }
                  this.setTitle(title)
                }
              }
            })
          }
        }
      },
      title: {
        text: '<div class="text-center"><p class="text-primary yzj-size-14">暂无数据</p><img src="/static/images/nav-icon03.png"><p class="text-info yzj-size-16">工作成功率</p></div>',
        verticalAlign: 'middle',
        y: -20,
        useHTML: true,
        fontFamily: '微软雅黑'
      },
      credits: {
        enabled: false
      },
      plotOptions: {
        pie: {
          shadow: false,
          innerSize: '70%',
          colors: [
            '#ff6600',
            '#e0e0e0'
          ],
          dataLabels: {
            enabled: false
          },
          enableMouseTracking: false,
          borderWidth: 0
        }
      },
      series: [{
        name: '工作成功率'
      }]
    })
    $('#highchart2').highcharts({
      chart: {
        type: 'area',
        zoomType: 'y',
        events: {
          load: function () {
            let now = new Date(new Date().setDate(new Date().getDate() - 1))
            let begin = new Date(new Date().setDate(now.getDate() - 6))
            let d = []
            this.options.xAxis.categories = [begin.getMonth() + 1 + '-' + begin.getDate()]
            setTimeout(() =>{
              reportService.get_freelancer_statis().success((result) =>{
                if (result.error_code === 0 && result.data.views.length > 0 && result.data.views.length < 10) {
                  for (let i = 0; i < result.data.views.length; i++) {
                    let date = result.data.views[i].period.toString()
                    d.push([date.substr(4, 2) + '-' + date.substr(6, 2), result.data.views[i].count])
                  }
                } else {
                  d = [[begin.getMonth() + 1 + '-' + begin.getDate(), 0]]
                  while (!(begin.getFullYear() === now.getFullYear() && begin.getMonth() === now.getMonth() && begin.getDate() === now.getDate())) {
                    let data_new = new Date(begin.setDate(begin.getDate() + 1))
                    this.options.xAxis.categories.push(data_new.getMonth() + 1 + '-' + data_new.getDate())
                    d.push([data_new.getMonth() + 1 + '-' + data_new.getDate(), 0])
                  }
                }
                this.series[0].setData(d)
              })
            }, 1000)
          }
        }
      },
      title: {
        style: {display: 'none'}
      },
      xAxis: {
        categories: []
      },
      yAxis: {
        title: {
          style: {
            display: 'none'
          }
        }
      },
      credits: {
        enabled: false
      },
      tooltip: {
        pointFormat: '{point.y}次查看'
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        area: {
          color: '#fbae42',
          fillColor: '#f3f3f3',
          dataLabels: {
            enabled: false
          },
          borderWidth: 0
        },
        series: {
          marker: {
            symbol: 'url(/static/images/statisics-icon.png)'
          }
        }
      },
      series: [{
        data: []
      }]
    })
  },
  methods: {
    get_profile () {
      profile.get_profile().success((data) => {
        if (data.error_code === 0) {
          this.$set('workload', data.profile.workload)
          this.$set('completeness', data.profile.completeness)
        }
      })
    },
    open_window () {
      this.open('workload_modal')
    }
  },
  events: {
    update_workload (item) {
      let available = false
      if (item === '0') {
        available = true
        // 没有为0的状态，默认给1
        item = 1
      } else {
        available = false
      }
      profile.put_profile({workload: item, available: available}).success((data) => {
        this.close('workload_modal')
      })
    }
  }
})
