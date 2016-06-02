<template>
  <div class="form-group">
    <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
      项目图片
    </label>
    <div class="col-xs-2">
      <img :src="path" width="100" height="100" />
    </div>
    <div class="col-xs-5 clear-left">
      <p class="yzj-size-12 text-primary yzj-top-distance10">
        支持JPG,JPEG,GIF,PNG,BMP格式，且不超过
        <span class="text-warning">
          5M
        </span>
      </p>
      <div class="inputfileload pull-left yzj-top-distance15">
        <div class="uploadphoto">
          上传文件
        </div>
        <input type="file" class="inputfile" id="picture" name="photo" v-on:change="uploadFile($event)">
      </div>
    </div>
  </div>
</template>

<script>
  import $ from 'jquery'
  import Cookies from 'js-cookie'
  export default {
    data () {
      return {
        path: '/static/images/add-project-img.png'
      }
    },
    methods: {
      uploadFile (event) {
        let fileo = event.target.files[0]
        let _self = this
        if (fileo.size > 5 * 1024 * 1024) {
          this.errPicture = '图片太大'
          return
        } else {
          this.errPicture = ''
        }
        let data = new FormData()
        data.append('file', fileo)
        data.append('t', 'portfolio')
        data.append('_xsrf', Cookies.get('_xsrf'))
        $.ajax({
          type: 'POST',
          url: '/api/attachment',
          cache: false,
          dataType: 'json',
          data: data,
          processData: false,
          contentType: false,
          success: (data) => {
            if (data.error_code === 0) {
              _self.attachment_id = data.attachment_id
              _self.path = data.path
              _self.$dispatch('upload_completed', data.attachment_id, data.path)
            }
          }
        })
      }
    },
    watch: {
      picturepath (value) {
        if (value && value.path) {
          this.path = value.path
        } else {
          this.path = '/static/images/add-project-img.png'
        }
      }
    },
    props: ['picturepath']
  }
</script>
