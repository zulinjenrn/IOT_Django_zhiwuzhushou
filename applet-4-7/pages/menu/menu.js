// pages/menu/menu.js

const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    grids: [{
      "name": "应用1"
    }, {
      "name": "应用2"
    }], // 九宫格内容
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    this.updateMenuData()
  },

  /**
   * 请求后台，更新menu数据
   */
  updateMenuData: function() {
    var that = this
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/menu',
      success: function(res) {
        var menuData = res.data.data
        that.setData({
          grids: menuData
        })
      }
    })
  },

  onNavigatorTap: function(e) {
    var index = e.currentTarget.dataset.index
    var item = this.data.grids[index]
    console.log(item)
    if (item.app.application == 'Illumination') {
      console.log('-------------')
      wx.navigateTo({
        url: '../Illumination/Illumination',
      })
    } else if (item.app.application == 'soilmoisture') {
      wx.navigateTo({
        url: '../soilmoisture/soilmoisture',
      })
    } else if (item.app.application == 'temperature') {
      wx.navigateTo({
        url: '../temperature/temperature'
      })
    } else if (item.app.application == 'fertility') {
      wx.navigateTo({
        url: '../fertility/fertility'
      })
    } else if (item.app.application == 'caution') {
      wx.navigateTo({
        url: '../caution/caution',
      })
    } else if (item.app.application == 'monitor') {
      wx.navigateTo({
        url: '../monitor/monitor',
      })
    }
  }
})