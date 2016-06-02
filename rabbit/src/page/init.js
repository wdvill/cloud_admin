import $ from 'jquery'

export default {
  install (Vue, options) {
    // 鼠标划过显示删除图标
    $('.bg_hover').each(function () {
      $('.bg_hover').mouseover(function () {
        $('.dis_icon').removeClass('hide')
      })
    })

    $('.bg_hover').each(function () {
      $('.bg_hover').mouseout(function () {
        $('.dis_icon').addClass('hide')
      })
    })
    // 头部显示搜索框
    $('#show_search').click(function () {
      $('#search_box').css('display', 'block')
      $('#search_text').focus()
      $('#show_search').css('display', 'none')
    })
    $('#search_box .dropdown-menu span').each(function () {
      $(this).click(function () {
        $('#search_box .dropdown-menu span').removeClass('active')
        $(this).addClass('active')
      })
    })
    $('#search_text').keydown(function (event) {
      let keyword = $(this).val()
      let url = ''
      $('#search_box .dropdown-menu span').each(function (index, item) {
        if ($(item).html() === '找高手' && $(item).hasClass('active')) {
          url = '/freelancers/find?q=' + keyword
        } else {
          url = '/jobs/find?q=' + keyword
        }
      })
      if (event.keyCode === 13) {
        window.location.href = url
      }
    })

  }
}
