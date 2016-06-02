<template>
  <dt>*&nbsp;存入托管</dt>
  <dd>
    <input type="radio" name="deposit" value="fixed" v-model="deposit_type" v-on:click="show_v"/>
    为这个项目托管全部预算资金
  </dd>
  <dd>
    <input type="radio" name="deposit" value="milestone" v-model="deposit_type" v-on:click="show_v"/>
    为第一个里程碑存入较少的钱
  </dd>
  <dt v-show="deposit_type == 'fixed'">*&nbsp;预算</dt>
  <dd v-show="deposit_type == 'fixed'">
    <div class="row">
      <div class="col-xs-4">
        <span>1500元</span>
      </div>
      <div class="col-xs-4">
        <a href="#"><img src="/static/images/edit-btn-icon.png">&nbsp;&nbsp;编辑</a>
      </div>
    </div>
  </dd>
  <dt v-show="deposit_type == 'fixed'">*&nbsp;项目结束时间</dt>
  <dd v-show="deposit_type == 'fixed'">
    <div class="row">
      <div class="col-xs-4">
        <input type="text" class="form-control" data-provide="datepicker"/>
      </div>
    </div>
  </dd>
</template>

