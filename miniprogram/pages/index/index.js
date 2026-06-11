Page({
  data: {
    company: {
      name: '您的企业名称',
      slogan: '专业 · 高效 · 值得信赖',
      banner: '/images/banner.jpg',
      phone: '13800000000',
      about: '我们是一家专注于为客户提供优质服务的企业。拥有专业团队和丰富经验。'
    },
    quickActions: [
      { id: 1, name: '在线预约', icon: '/images/icon-book.png', action: 'book' },
      { id: 2, name: '联系我们', icon: '/images/icon-contact.png', action: 'contact' },
      { id: 3, name: '公司地址', icon: '/images/icon-location.png', action: 'location' },
      { id: 4, name: '全部服务', icon: '/images/icon-service.png', action: 'service' }
    ],
    services: [
      { id: 1, name: '服务项目一', desc: '专业服务描述，展示核心优势', price: '99', cover: '/images/service1.jpg' },
      { id: 2, name: '服务项目二', desc: '专业服务描述，展示核心优势', price: '199', cover: '/images/service2.jpg' },
      { id: 3, name: '服务项目三', desc: '专业服务描述，展示核心优势', price: '299', cover: '/images/service3.jpg' }
    ]
  },

  onLoad() {
    // 此处可以从服务器或云数据库加载数据
    // wx.request({ url: 'https://your-api.com/company', success: res => this.setData({ company: res.data }) })
  },

  onAction(e) {
    const action = e.currentTarget.dataset.action
    switch(action) {
      case 'book':
        wx.navigateTo({ url: '/pages/detail/detail' })
        break
      case 'contact':
        wx.makePhoneCall({ phoneNumber: this.data.company.phone })
        break
      case 'location':
        wx.openLocation({ latitude: 39.9, longitude: 116.4, name: this.data.company.name })
        break
      case 'service':
        wx.pageScrollTo({ selector: '.service-list', duration: 300 })
        break
    }
  },

  onServiceTap(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({ url: `/pages/detail/detail?id=${id}` })
  },

  onCall() {
    wx.makePhoneCall({ phoneNumber: this.data.company.phone })
  }
})
