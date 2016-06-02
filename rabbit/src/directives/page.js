import $ from 'jquery'
export default {
  install (Vue, options) {
    Vue.directive('page', {
      data: null,
      params: ['query'],
      acceptStatement: true,
      update: function (pageObject) {
        let self = this
        str = ''
        if (!pageObject) {
          return
        }
        let maxPage = Math.ceil(pageObject.itemsCount / pageObject.pageSize)
        console.log(maxPage)
        let pageNo = pageObject.pageNo
        let str = '<nav class="sabrosus"><ul class="pagination">'
        if (maxPage > 10) {
          if (pageNo > 3) {
            str += '<li><a href="javascript:;">《</a></li>'
            str += '<li><span>......</span></li>'
          }
          for (let i = pageNo <= 2 ? 1 : pageNo - 2; i <= (pageNo >= maxPage - 2 ? maxPage : pageNo + 2); i++) {
            if (i === 1) {
              if (pageNo === 1) {
                str += '<li  class="disabled"><span>《</span></li>'
                str += '<li class="active"><span>' + i + '</span></li>'
              } else {
                str += '<li><a href="javascript:;">《</a></li>'
                str += '<li><a href="javascript:;">' + i + '</a></li>'
              }
            } else if (i === maxPage) {
              if (pageNo === maxPage) {
                str += '<li class="active"><span >' + i + '</span></li>'
                str += '<li class="disabled"><span>》</span></li>'
              } else {
                str += '<li><a href="javascript:;">' + i + '</a></li>'
                str += '<li><a href="javascript:;">》</a></li>'
              }
            } else {
              if (pageNo === i) {
                str += '<li class="active"><span>' + i + '</span></li>'
              } else {
                str += '<li><a href="javascript:;" >' + i + '</a></li>'
              }
            }
          }
          if (pageNo < maxPage - 2) {
            str += '<li><span>......</span></li>'
            str += '<li><a href="javascript:;">》</a></li>'
          }
        } else if (maxPage <= 10 && maxPage > 1) {
          console.log(10, 'page')
          for (let i = 1; i <= maxPage; i++) {
            if (i === 1) {
              if (pageNo === 1) {
                str += '<li class="disabled"><span>《</span></li>'
                str += '<li class="active"><span >' + i + '</span></li>'
              } else {
                str += '<li><a href="javascript:;">《</a></li>'
                str += '<li><a href="javascript:;">' + i + '</a></li>'
              }
            } else if (i === maxPage) {
              if (pageNo === maxPage) {
                str += '<li  class="active"><span >' + i + '</span></li>'
                str += '<li class="disabled"><span >》</span></li>'
              } else {
                str += '<li><a href="javascript:;">' + i + '</a></li>'
                str += '<li><a href="javascript:;">》</a></li>'
              }
            } else {
              if (pageNo === i) {
                str += '<li class="active"><span>' + i + '</span></li> '
              } else {
                str += '<li> <a href="javascript:;" >' + i + '</a></li> '
              }
            }
          }
        }
        str += '</ul></nav>'
        this.el.innerHTML = str
        $(this.el).find('nav[class=sabrosus]').find('a').on('click', function () {
          let text = $(this).html()
          let pageNo = pageObject.pageNo
          if ($.trim(text) === '《') {
            pageObject.pageNo = pageNo - 1
          } else if ($.trim(text) === '》') {
            pageObject.pageNo = pageNo + 1
          } else {
            pageObject.pageNo = parseInt(text, 10)
          }
          self.params.query.call(self)
        })
      }
    })
  }
}
