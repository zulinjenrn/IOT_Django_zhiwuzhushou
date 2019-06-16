//index.js
//获取应用实例
const app = getApp()
const cookieUtil = require('../../utils/cookie.js')

Page({
  data: {
    isAuthorized: false,
    constellationData: null,
    stockData: null,
    weatherData: null
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },

  updateData: function() {
    wx.showLoading({
      title: '加载中',
    })
    var that = this
    var cookie = cookieUtil.getCookieFromStorage()
    var header = {}
    header.Cookie = cookie
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/stock',
      header: header,
      
      success: function (res) {
        that.setData({
          stockData: res.data.data
        })
        wx.hideLoading()
      }
    })
  },

  onPullDownRefresh: function() {
    var that = this
    var cookie = cookieUtil.getCookieFromStorage()
    var header = {}
    header.Cookie = cookie
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/auth/status',
      header: header,
      success: function(res){
        var data = res.data.data
        if (data.is_authorized == 1){
          that.setData({
            isAuthorized: true
          })
          that.updateData()
        }else{
          that.setData({
            isAuthorized: false
          })
          wx.showToast({
            title: '请先授权登录',
          })
        }
      }
    })
  },

  onLoad: function() {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse) {
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },

  send1: function () {
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/stock',
      data: {
        get: 'off-water'
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success: function (res) {
        console.log(res.data),
          wx.showToast({
            title: '成功浇水一次',
          })
      }
    })
  },
    send2: function () {
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/stock',
      data: {
        get: 'on-shifei'
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success: function (res) {
        console.log(res.data),
          wx.showToast({
            title: '成功施肥一次',
          })
      }
    })
  },
  send0: function () {
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/stock',
      data: {
        get: 'on'
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success: function (res) {
        console.log(res.data),
          wx.showToast({
            title: '成功施肥一次',
          })
      }
    })
  },
  send3: function () {
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/stock',
      data: {
        get: 'off'
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      success: function (res) {
        console.log(res.data),
          wx.showToast({
            title: '成功施肥一次',
          })
      }
    })
  }
})