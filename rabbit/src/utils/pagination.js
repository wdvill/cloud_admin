const pageNum = 10

function Pagination (array) {
  this.array = array
  this.currentPage = 0
}

Pagination.prototype.more = function () {
  if (this.array.length > pageNum * this.currentPage) {
    return {
      array: this.array.slice(this.currentPage++ * pageNum, pageNum * this.currentPage),
      more: this.array.length > this.currentPage * pageNum
    }
  } else {
    return {}
  }
}

export default {
  'Pagination': Pagination
}
