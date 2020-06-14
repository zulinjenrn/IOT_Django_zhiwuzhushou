// pages/homepage/homepage.js

const app = getApp()
const cookieUtil = require('../../utils/cookie.js')

Page({
  formSubmit: function (e) {
    var nickname = app.globalData.userInfo.nickName
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/authorization/addshebei',
      data: {
        'shebeiid': e.detail.value.shebeiid,
        'status': e.detail.value.status,
        'nickname': nickname
      },
      method: 'POST',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
        wx.showToast({
          title: '请求成功',
        })
      }
    })
  }
})