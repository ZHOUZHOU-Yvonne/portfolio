App({
  onLaunch() {
    // 初始化云开发（如需使用云数据库，取消注释）
    // wx.cloud.init({ env: 'your-env-id' })
    this.globalData = {
      companyName: '您的企业名称',
      phone: '400-xxx-xxxx',
      services: []
    }
  }
})
