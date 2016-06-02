<template>
<div class="canlendar_box">
  <div class="show_box" v-show="is_week">
    <a class="btn_left" @click="change_week(-7)"></a>
    <div class="date_box">
      {[begin_week]}&nbsp;至&nbsp;{[end_week]}
      <img @click="show_calendar" class='calendar_icon' src="/static/images/calendar_icon.png" >
    </div>
    <a class="btn_right" @click="change_week(7)"></a>
  </div>
  <div class="show_box" v-show="!is_week">
    <div class="date_box date_value">
      {[value]}
      <img @click="show_calendar" class='calendar_icon' src="/static/images/calendar_icon.png" >
    </div>
  </div>
  <div class="calendar" v-show="show" :style="{'left':x+'px','top':y+'px'}" transition="calendar" transition-mode="out-in" v-on:mouseout.self="modal_hide()" v-on:mouseover="modal_show()">
    <div class="calendar-tools">
      <i class="fa fa-angle-left float left" @click="prev">&lt;</i>
      <i class="fa fa-angle-right float right" @click="next">&gt</i>
        <div class="text-center">
          <input type="number" v-model="year" value="{[year]}" @change="up_date(year,month)" min="1970" max="2100" maxlength="4" number>
          / {[months[month]]}
        </div>
    </div>
    <table cellpadding="5">
      <thead>
        <tr>
          <td v-for="week in weeks" class="week">{[week]}</td>
        </tr>
      </thead>
        <tr v-for="(k1, day) in days">
          <td v-for="(k2, child) in day" :class="{'today':child.today,'disabled':child.disabled}" @click="select_date($event, k1, k2)">
            {[child.day.getDate()]}
          </td>
        </tr>
    </table>
  </div>
</div>
</template>
<script>
  import $ from 'jquery'
  export default {
    props: {
      show: {
        type: Boolean,
        default: false
      },
      value: {
        type: String,
        twoWay: true,
        default: ''
      },
      x: {
        type: Number,
        default: 0
      },
      y: {
        type: Number,
        default: 28
      },
      begin_week: {
        type: String,
        twoWay: true,
        default: ''
      },
      end_week: {
        type: String,
        twoWay: true,
        default: ''
      },
      min: {
        type: String,
        default: ''
      },
      max: {
        type: String,
        default: ''
      },
      is_week: {
        type: Boolean,
        default: false
      }
    },
    data: () => {
      return {
        year: 0,
        month: 0,
        day: 0,
        days: [],
        today: 0,
        weeks: ['日', '一', '二', '三', '四', '五', '六'],
        months: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
      }
    },
    created () {
      let now = new Date()
      this.year = now.getFullYear()
      this.month = now.getMonth()
      this.day = now.getDate()
      this.today = parseInt(now.getTime(), 10)
      this.up_date(this.year, this.month)
    },
    watch: {
      year () {
        this.up_date(this.year, this.month)
      },
      month () {
        this.up_date(this.year, this.month)
      },
      min () {
        this.up_date(this.year, this.month)
      },
      max () {
        this.up_date(this.year, this.month)
      }
    },
    methods: {
      up_date (y, m) {
        let firstDayOfMonth = new Date(y, m, 1).getDay() // 当月第一天是周几
        let lastDateOfLastMonth = new Date(y, m, 0).getDate() // 上月最后一天的日期
        let lastDateOfMonth = new Date(y, m + 1, 0).getDate() // 当月最后一天的日期
        let lastDayOfMonth = new Date(y, m + 1, 0).getDay() // 当月最后一天是周几
        let prevs = []
        let nows = []
        let nexts = []
        this.days = [] // 初始化日期
        for (let i = firstDayOfMonth - 1; i >= 0; i--) {
          prevs.push({day: new Date(y, m - 1, lastDateOfLastMonth - i), today: this.is_now(this, new Date(y, m - 1, lastDateOfLastMonth - i)), disabled: this.is_up(this, new Date(y, m - 1, lastDateOfLastMonth - i))})
        }
        for (let i = 1; i <= 6 - lastDayOfMonth; i++) {
          nexts.push({day: new Date(y, m + 1, i), today: this.is_now(this, new Date(y, m + 1, i)), disabled: this.is_up(this, new Date(y, m + 1, i))})
        }
        for (let i = 1; i <= lastDateOfMonth; i++) {
          nows.push({day: new Date(y, m, i), today: this.is_now(this, new Date(y, m, i)), disabled: this.is_up(this, new Date(y, m, i))})
        }
        let daylist = [...new Set(prevs), ...new Set(nows), ...new Set(nexts)]
        let len = daylist.length
        for (let i = 0; i < len / 7; i++) {
          this.days.push(daylist.splice(0, 7))
        }
      },
      is_now (obj, date) {
        return (new Date(obj.today).getFullYear() === date.getFullYear() && new Date(obj.today).getMonth() === date.getMonth() && new Date(obj.today).getDate() === date.getDate())
      },
      is_up (obj, date) {
        if (obj.min !== '') {
          let begin = new Date(obj.min.substring(0, 4), obj.min.substring(5, 7) - 1, obj.min.substring(8, 10))
          return begin.getTime() >= date.getTime() || obj.today <= date.getTime()
        } else if (obj.max !== '') {
          let end = new Date(obj.max.substring(0, 4), obj.max.substring(5, 7) - 1, obj.max.substring(8, 10))
          return end.getTime() <= date.getTime()
        } else {
          return obj.today <= parseInt(date.getTime(), 10)
        }
      },
      prev () {
        if (this.month === 0) {
          this.month = 11
          this.year = this.year - 1
        } else {
          this.month = this.month - 1
        }
      },
      next () {
        if (this.month === 11) {
          this.month = 0
          this.year = this.year + 1
        } else {
          this.month = this.month + 1
        }
      },
      change_week (num) {
        let begin = new Date(this.begin_week.substring(0, 4), this.begin_week.substring(5, 7) - 1, this.begin_week.substring(8, 10))
        let end = new Date(this.end_week.substring(0, 4), this.end_week.substring(5, 7) - 1, this.end_week.substring(8, 10))
        if (end.getTime() > this.today && num > 0) {
          return
        }
        let target_begin = new Date(begin.getTime() + (num * 24 * 3600 * 1000))
        let target_end = new Date(end.getTime() + (num * 24 * 3600 * 1000))
        this.begin_week = target_begin.getFullYear() + '年' + this.months[target_begin.getMonth()] + '月' + this.formate_day(target_begin.getDate()) + '日'
        this.end_week = target_end.getFullYear() + '年' + this.months[target_end.getMonth()] + '月' + this.formate_day(target_end.getDate()) + '日'
      },
      select_date (e, k1, k2) {
        let that = this
        that.day = parseInt(e.target.innerHTML, 10)
        if (that.day > 20 && k1 === 0) {
          that.month = that.month - 1
        } else if (that.day < 7 && (k1 === 4 || k1 === 5)) {
          this.month = this.month + 1
        }
        // that.today = parseInt(new Date(that.year, that.month, that.day), 10)
        if (that.is_week) {
          that.formate_week(that)
        } else {
          that.formate_date(that)
        }
        this.show = false
      },
      formate_day (data) {
        return (data < 10 ? '0' + data : data)
      },
      formate_date (obj) {
        obj.value = obj.year + '年' + obj.months[obj.month] + '月' + obj.formate_day(obj.day) + '日'
      },
      formate_week (obj) {
        let week = new Date(obj.year, obj.month, obj.day)
        let begin = new Date(week.getTime() - (week.getDay() - 1) * 24 * 3600 * 1000)
        let end = new Date(week.getTime() + (7 - week.getDay()) * 24 * 3600 * 1000)
        obj.begin_week = begin.getFullYear() + '年' + obj.months[begin.getMonth()] + '月' + obj.formate_day(begin.getDate()) + '日'
        obj.end_week = end.getFullYear() + '年' + obj.months[end.getMonth()] + '月' + obj.formate_day(end.getDate()) + '日'
      },
      show_calendar () {
        if (this.show === true) {
          this.show = false
        } else {
          this.show = true
        }
      },
      modal_hide () {
        let that = this
        if (that.show) {
          $(document).one('click.fool', (e) => {
            if (e.type === 'click') {
              that.show = false
            }
          })
        }
      },
      modal_show () {
        $(document).unbind('click.fool')
      }
    }
  }
</script>
<style>
.canlendar_box{height:31px; position:relative;}
.show_box{height:31px; overflow:hidden;}
.show_box .btn_left{height:31px; width:17px; background:url('/static/images/left_icon.png') no-repeat center center; float:left; cursor:pointer;}
.show_box .btn_right{height:31px; width:17px; background:url('/static/images/right_icon.png') no-repeat center center; float:left; cursor:pointer;}
.show_box .btn_left:hover{background:url('/static/images/left_now_icon.png') no-repeat center center;}
.show_box .btn_right:hover{background:url('/static/images/right_now_icon.png') no-repeat center center;}
.show_box .date_box{height:31px; line-height:31px; font-size:16px; color:#666; float:left; margin:0 40px;}
.show_box .date_box img{float:right; width:23px; height:21px; margin:5px 0 5px 15px; cursor:pointer;}
.show_box .date_value{margin:0;}
.calendar {
  width: 300px;
  padding: 10px;
  background: #fff;
  position: absolute;
  border: 1px solid #DEDEDE;
  border-radius: 2px;
  opacity:.95;
  transition: all .5s ease;
  z-index: 101;
}
 
.calendar-enter, .calendar-leave {
  opacity: 0;
  transform: translate3d(0,-10px, 0);
}

.calendar:before {
  position: absolute;
  left:30px;
  top: -10px;
  content: "";
  border:5px solid rgba(0, 0, 0, 0);
  border-bottom-color: #DEDEDE;
}
.calendar:after {
  position: absolute;
  left:30px;
  top: -9px;
  content: "";
  border:5px solid rgba(0, 0, 0, 0);
  border-bottom-color: #fff;
}
.calendar-tools{
  height:32px;
  font-size: 20px;
  line-height: 32px;
  color:#5e7a88;
}
.calendar-tools .float.left{
  float:left;
}
.calendar-tools .float.right{
  float:right;
}
.calendar-tools input{
  font-size: 20px;
  line-height: 32px;
  color: #5e7a88;
  width: 70px;
  text-align: center;
  border:none;
  background-color: transparent;
}
.calendar-tools>i{
  margin:0 16px;
  line-height: 32px;
  cursor: pointer;
  color:#707070;
}
.calendar-tools>i:hover{
  color:#5e7a88;
}
.calendar table {
  clear: both;
  width: 100%;
  margin-bottom:10px;
  border-collapse: collapse;
  color: #444444;
}
.calendar td {
  margin:2px !important;
  padding:8px 0;
  width: 14.28571429%;
  text-align: center;
  vertical-align: middle;
  font-size:16px;
  line-height: 125%;
  cursor: pointer;
}
.calendar td:hover{
  background:#f3f8fa;
}
.calendar td.week{
  pointer-events:none !important;
  cursor: default !important;
}
.calendar td.disabled {
  color: #c0c0c0;
  pointer-events:none !important;
  cursor: default !important;
}
.calendar td.today {
  background-color: #5e7a88;
  color: #fff;
  font-size:16px;
}
.calendar thead td {
  text-transform: uppercase;
}
.calendar .timer{
  margin:10px 0;
  text-align: center;
}
.calendar .timer input{
  border-radius: 2px;
  padding:5px;
  font-size: 14px;
  line-height: 18px;
  color: #5e7a88;
  width: 50px;
  text-align: center;
  border:1px solid #efefef;
}
.calendar .timer input:focus{
  border:1px solid #5e7a88;
}
.calendar .lunar{
  font-size:11px;
  line-height: 150%;
  color:#aaa;
}
.calendar td.today{
  color:#fff;
}
</style>