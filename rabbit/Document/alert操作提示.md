# alert 提示

## 一、alert 组件方式
>文件路径：src/components/strap-alert.vue

1、页面html引用
```
<strap-alert :msg="alert.msg" :title="alert.title" :show-type="alert.showType" :show-alert.sync="alert.showAlert"></strap-alert>
```

2、js 引用
```
1、 引入
import strapAlert from 'strap_alert.vue'

2、vue里面组件申明
data:{
	alert: {
		msg: '',
		title: '',
		showType: '',
		showAlert: '',
	}
},
components: {
  strapAlert
}
```

3、参数说明
```
showType：{String} 显示的类别：success(成功的情况)、danger(失败的情况)
title: {String} 提示的title
msg: {String} 提示的内容(必填)
showAlert: {Boolean} 是否显示提示
callback: {Function} 回调函数(非必填）
```

4、触发显示
```
设置showAlert为true
```


## 二、Js 方法调用方式
>文件路径：/static/common/js/yunwork.js

1、页面引入js文件
```
<script src="/static/common/js/yunwork.js"></script>
```
2、调用函数
```
YWORK.alert('danger', '错误提示', CODE[result.error_code]);
其中参数
@params {
 	type{String} 类型[success,danger]
 	title{String} 标题
 	content{String} 内容
 	cb{Function} 毁掉函数(非必填）
}
```
***
`如果使用有疑问，请拨打110报警`