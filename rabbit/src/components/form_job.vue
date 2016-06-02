<template>
  <h3 class="modal-title text-info text-center" id="myModalLabel">
    <span v-show="!item.id">添加</span><span v-show="item.id">编辑</span>工作经验
  </h3>
 <form class="form-horizontal yzj-top-distance50" id="work-form">
    <div class="form-group">
      <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
        <span class="text-warning size-18">
          *
        </span>
        所在公司
      </label>
      <div class="col-xs-7">
        <input type="text" class="form-control" placeholder="公司名称为1~50字符" id="company"
        name="company" maxlength="50" minlength="1" v-model="item.company">
      </div>
    </div>
    <div class="form-group form-error" for="company">
      <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
        <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
        aria-hidden="true">
        {[v_message.company.minlength]}
        </span>
      </div>
    </div>
  <place v-bind:city_id.sync="item.city.id"></place>
  <div class="form-group">
    <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
      <span class="text-warning size-18">
        *
      </span>
      工作职位
    </label>
    <div class="col-xs-7">
      <input type="text" class="form-control" placeholder="" v-model="item.title" name="title">
    </div>
  </div>
  <div class="form-group form-error" for="title">
    <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
      <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
      aria-hidden="true">
      工作职位是必填字段
    </span>
  </div>
</div>
<role :role.sync="item.role"></role>
<work_date :start_at.sync="item.start_at" :end_at.sync="item.end_at"></work_date>
<div class="">
  <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
    &nbsp;
  </label>
  <div class="col-xs-7">
    <input type="checkbox" class="bigbox" v-model="item.working" />
    <span class="yzj-size-16">
      仍在该公司工作
    </span>
  </div>
</div>
<div class="form-group" v-show="v_message.dateErr">
    <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
    <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10" v-text="v_message.dateErr">
    </span>
  </div>
</div>
<div class="clearfix">
</div>
<div class="form-group">
  <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
    工作描述
  </label>
  <div class="col-xs-7">
    <textarea class="form-control" rows="15" v-model="item.detail">
    </textarea>
  </div>
</div>
  </form>
</template>

<script>
import place from './place.vue'
import role from './role.vue'
import work_date from './work_date.vue'
import $ from 'jquery'
import Validate from '../form/validate'

let validateObj = null
export default {
  ready () {
    let items = {
      company: {
        minlength: 1,
        maxlength: 50
      },
      title: {
        required: true
      },
      role: {
        required: true
      },
      city_id: {
        required: true
      }
    }
    validateObj = new Validate(items, $('#work-form'))
    console.log(this.item.working, 'working', typeof (this.item.working))
  },
  data () {
    return {
      company: '',
      start_at: '',
      end_at: '',
      city_id: '',
      title: '',
      role: '999',
      working: false,
      validation: {
        company: {
          minlength: 1,
          maxlength: 50
        },
        start_at: {
          required: true
        },
        end_at: {
          required: true
        },
        city_id: {
          required: true
        },
        role: {
          required: true
        },
        title: {
          required: true
        }
      },
      v_result: {
        company: { },
        start_at: { },
        end_at: { },
        city_id: { },
        role: { },
        title: { },
        v_valid: true
      },
      v_message: {
        company: {
          minlength: '公司名称为1~50字符',
          maxlength: '公司名称为1~50字符'
        },
        start_at: {
          required: '开始时间不能为空'
        },
        end_at: {
          required: '结束时间不能为空'
        },
        city_id: {
          required: '城市不能为空'
        },
        role: {
          required: '角色不能为空'
        },
        title: {
          required: '职位不能为空'
        },
        dateErr: ''
      }
    }
  },
  methods: {
    save () {
      let _self = this
      // 页面规则验证
      if (!validateObj.validate()) {
        return
      }
      // 开始日期不能大于结束日期
      if (!this.compareTime()) {
        return
      }
      if (this.item.id) {
        $.ajax({
          url: '/api/employment',
          method: 'put',
          data: {
            eid: this.item.id,
            company: this.item.company,
            city_id: this.item.city.id,
            title: this.item.title,
            start_at: this.item.start_at,
            role: this.item.role,
            end_at: this.item.end_at,
            working: typeof (this.item.working) !== 'undefined' ? this.item.working : false,
            detail: this.item.detail
          },
          dataType: 'json'
        }).success((data) => {
          if (data.error_code === 0) {
            _self.$dispatch('close_modal')
          } else {
            alert(data.msg)
          }
        })

      } else {
        $.post('/api/employment', {
          company: this.item.company,
          city_id: this.item.city.id,
          title: this.item.title,
          start_at: this.item.start_at,
          role: this.item.role,
          end_at: this.item.end_at,
          working: typeof (this.item.working) !== 'undefined' ? this.item.working : false,
          detail: this.item.detail
        }, 'json').success((data) => {
          data = $.parseJSON(data)
          if (data.error_code === 0) {
            _self.$dispatch('add_job', _self.item)
            _self.$dispatch('close_modal')
          } else {
            alert(data.msg)
          }
        })
      }
    },
    /* 比较开始时间和结束时间 */
    compareTime () {
      let start_at = (new Date(this.item.start_at + '-01')).getTime()
      let end_at = (new Date(this.item.end_at + '-01')).getTime()
      let now = (new Date()).getTime()
      this.v_message.dateErr = ''
      // 开始日期不能大于结束日期
      if (!this.item.working && start_at > end_at) {
        this.v_message.dateErr = '开始日期不能大于结束日期'
        return false
      }
      // 开始日期不能大于当前日期
      if (start_at > now) {
        this.v_message.dateErr = '开始日期不能大于当前日期'
        return false
      }
      // 结束日期不能大于当前日期
      if (!this.item.working && end_at > now) {
        this.v_message.dateErr = '结束日期不能大于当前日期'
        return false
      }
      return true
    }
  },
  props: ['item'],
  components: {
    place,
    role,
    work_date
  }
}
</script>

