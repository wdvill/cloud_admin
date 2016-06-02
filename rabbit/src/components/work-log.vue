<template>
  <ul class="work-log-component">

    <!-- 没有日志的状态 -->
    <li class="this-no-log" v-if="!logList.length">
      <p><img src="../assets/images/components/no-log-thisday.png" height="52" width="65" alt=""><span>今日尚无工作日志</span></p>
    </li>

    <!-- 有日志的状态 -->
    <template v-if="logList.length">
      <li class="hour-list" v-for="log in logList">
      <label><span v-html="log.hour | ampm"></span><br/><b aria-checked="all" class="ico-checkbox"></b></label>
        <ul class="log-list clearfix">
          <template v-for="item in log.list">
            <li class="empty-log" v-if="!item">
              <p class="log-hd"></p>
              <div class="log-bd"></div>
              <div class="log-ft"></div>
            </li>
            <li class="auto-log" v-if="item && item.is_auto">
              <suspend :item="item" :contract_id="contract_id"></suspend>
              <p class="log-hd note-star note-end">
                <span v-text="item.description"></span>
              </p>
              <div class="log-bd">
                <img :src="item.attachment" alt="工作日志截屏" onclick="window.open('/contracts/{[contract_id]}/diary/{[item.id]}')" onmouseover="$(this).parent().prev().prev().show()" onmouseout="$(this).parent().prev().prev().hide()" style="cursor:pointer">
              </div>
              <div class="log-ft">
                <b class="ico-checkbox" value="{[item.id]}"></b>
                <time v-text="item.shot_at | formatTime"></time>
                <ul class="active-state">
                  <li v-for="n in 10" :class="{'active': n < parseInt(item.activity/10, 10)}"></li>
                </ul>
              </div>
            </li>
            <li class="manual-log" v-if="item && !item.is_auto">
              <p class="log-hd note-star note-end">
                <span v-text="item.description"></span>
              </p>
              <div class="log-bd">
                <span>手动记时</span>
              </div>
              <div class="log-ft">
                <b class="ico-checkbox" value="{[item.id]}"></b>
                <time v-text="item.shot_at | formatTime">12:25</time>
              </div>
            </li>
          </template>
        </ul>
      </li>
    </template>
  </ul>
</template>
<script>
  require('../assets/sass/components/work-log.scss')
  import $ from 'jquery'
  import suspend from './work-log-suspend.vue'
  
  export default {
    data () {
      return {
        logList: []
      }
    },
    props: ['logData', 'contract_id'],
    watch: {
      'logData': function () {
        this.formatData()
        this.formatCheckBox()
      }
    },
    components: {
      suspend
    },
    methods: {
      // 格式化截屏数据
      formatData () {
        let logIndex = -1
        let logList = []
        this.logData.forEach((el) => {
          let hourIndex = el.shot_at.slice(-5, -4)
          if (logList.length) {
            let hasflag
            for (let i = 0; i < logList.length; i++) {
              hasflag = false
              if (el.hour === logList[i].hour) {
                logList[i].list[hourIndex] = el
                hasflag = true
                break
              }
            }
            if (!hasflag) {
              logIndex++
              logList[logIndex] = {}
              logList[logIndex].hour = el.hour
              logList[logIndex].list = [0, 0, 0, 0, 0, 0]
              logList[logIndex].list[hourIndex] = el
            }
          } else {
            logIndex++
            logList[logIndex] = {}
            logList[logIndex].hour = el.hour
            logList[logIndex].list = [0, 0, 0, 0, 0, 0]
            logList[logIndex].list[hourIndex] = el
          }
        })
        this.logList = logList
      },
      formatCheckBox () {
        let self = this
        $('.ico-checkbox').each(function (index, el) {
          $(el).click(function () {
            if ($(el).hasClass('ico-checkbox-checked')) {
              $(el).removeClass('ico-checkbox-checked')
              if ($(el).attr('aria-checked') === 'all') {
                $(el).parent().parent().find('.ico-checkbox').removeClass('ico-checkbox-checked')
              }
            } else {
              $(el).addClass('ico-checkbox-checked')
              if ($(el).attr('aria-checked') === 'all') {
                $(el).parent().parent().find('.ico-checkbox').addClass('ico-checkbox-checked')
              }
            }
            let list = $('.log-list').find('.ico-checkbox-checked')
            self.$dispatch('select_time', parseInt(10 * list.length, 10))
          })
        })
      }
    }
  }
</script>
