# conform 组件
>文件路径：src/components/confirm.vue

1、页面html引用
```
<confirm :title="title" :msg="msg" modal-id="eduModal" :ok-fn.sync="delete"></confirm>
```

2、js 引用
```
1、 引入(注意路径)
import confirm from './confirm.vue'

2、vue里面组件申明
data: {
  
},
components: {
  confirm
}
```

3、参数说明
```
@params {
 	modalId{String} 容器的id
 	title{String} 标题
 	msg{String} 内容
 	okFn{Function} 点击确定的操作函数
}
```

4、触发弹窗确认框
```
<img src="/static/images/del-btn-icon.png" data-toggle="modal" data-target="#modalId">
在容器上添加’data-toggle="modal" data-target="#modalId"‘，注意:modalId是你定义的id.
```
***
`如果使用有疑问，请拨打110报警`