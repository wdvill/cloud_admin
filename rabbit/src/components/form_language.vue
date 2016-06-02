<template>
  <form class="form-horizontal" id="modal-lang">
    <div class="form-group">
       <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16 text-info">输入语言名称</label>
       <div class="col-xs-7">
         <select class="form-control select-control" v-model="item.name" :disabled="item.name">
           <option value="Chinese">汉语</option>
           <option value="Japanese">日语</option>
           <option value="Korean">韩语</option>
           <option value="French">法语</option>
           <option value="Spanish">西班牙语</option>
         </select>
       </div>
    </div>
    <div class="col-xs-offset-1 col-xs-2 yzj-size-16 text-right">
     <h4 class="yzj-top-distance40 text-info">
      <strong>选择水平</strong>
    </h4>
  </div>
  <div class="clearfix"></div>
  <div class="yzj-top-distance40">
   <div class="col-xs-2 clear-both text-right">
     <input type="radio" name="language" class="language" value="1" v-model="item.level"/>
   </div>
   <div class="col-xs-8">
    <p class="yzj-size-16 text-muted">初始水平</p>
    <p class="yzj-size-14 text-primary yzj-top-distance10">只能通过书写简单沟通</p>
  </div>
  <div class="clearfix"></div>
  <div class="yzj-top-distance30">
    <div class="col-xs-2 clear-both text-right">
      <input type="radio" name="language" class="language" value="2" v-model="item.level"/>
    </div>
    <div class="col-xs-8">
      <p class="yzj-size-16 text-muted">可以对话</p>
      <p class="yzj-size-14 text-primary yzj-top-distance10">可以和雇主针对于项目进行沟通交谈</p>
    </div>
  </div>
  <div class="clearfix"></div>
  <div class="yzj-top-distance30">
    <div class="col-xs-2 clear-both text-right">
      <input type="radio" name="language" class="language" value="3" v-model="item.level"/>
    </div>
    <div class="col-xs-8">
      <p class="yzj-size-16 text-muted">流利沟通</p>
      <p class="yzj-size-14 text-primary yzj-top-distance10">可以完美掌握这门语言完成指令</p>
    </div>
  </div>
  <div class="clearfix"></div>
  <div class="yzj-top-distance30">
    <div class="col-xs-2 clear-both text-right">
      <input type="radio" name="language" class="language" value="4" v-model="item.level"/>
    </div>
    <div class="col-xs-8">
      <p class="yzj-size-16 text-muted">母语或双语</p>
      <p class="yzj-size-14 text-primary yzj-top-distance10">可以使用这门语言完成指令，包括各种词汇，成语，口语</p>
    </div>
  </div>
  <div class="clearfix"></div>
</form>
</template>
<script>
export default {
  created () {
    if (this.item.name) {
      console.log('edit language', this.item.name)
    }
    console.log(this.item.name, 'nono 0000')
  },
  data () {
    return {
      name: '',
      level: '1'
    }
  },
  methods: {
    save () {
      let row = {}
      if (this.item.name && this.item.level) {
        row[this.item.name] = this.item.level
      }
      this.$dispatch('add_language', row)
      this.$dispatch('close_modal')
    }
  },
  props: ['item']

}
</script>
