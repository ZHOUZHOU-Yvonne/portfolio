Page({
  data: {
    id: null,
    service: {
      name: '服务项目',
      price: '99',
      desc: '详细的服務描述信息，包括服务内容、时长、注意事项等。',
      cover: '/images/service1.jpg'
    },
    date: '',
    time: '',
    name: '',
    phone: '',
    remark: ''
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ id: options.id })
      // 加载对应服务详情
      // wx.request({ url: `https://api.example.com/services/${options.id}`, ... })
    }
  },

  onDateChange(e) { this.setData({ date: e.detail.value }) },
  onTimeChange(e) { this.setData({ time: e.detail.value }) },
  onNameInput(e) { this.setData({ name: e.detail.value }) },
  onPhoneInput(e) { this.setData({ phone: e.detail.value }) },
  onRemarkInput(e) { this.setData({ remark: e.detail.value }) },

  onSubmit() {
    const { service, date, time, name, phone, remark } = this.data
    if (!date || !time) {
      wx.showToast({ title: '请选择预约时间', icon: 'none' })
      return
    }
    if (!name.trim()) {
      wx.showToast({ title: '请输入姓名', icon: 'none' })
      return
    }
    if (!/^1[3-9]\d{9}$/.test(phone)) {
      wx.showToast({ title: '请输入有效手机号', icon: 'none' })
      return
    }

    // 提交预约到服务器
    wx.showLoading({ title: '提交中...' })

    // 模拟提交 - 实际使用时替换为真实API
    setTimeout(() => {
      wx.hideLoading()
      wx.showModal({
        title: '预约成功',
        content: `已预约 ${service.name}\n${date} ${time}\n我们会尽快与您联系`,
        showCancel: false,
        success: () => wx.navigateBack()
      })
    }, 1000)

    // 真实API调用（取消注释使用）：
    // wx.request({
    //   url: 'https://your-api.com/bookings',
    //   method: 'POST',
    //   data: { serviceId: this.data.id, date, time, name, phone, remark },
    //   success: res => {
    //     wx.hideLoading()
    //     wx.showToast({ title: '预约成功', icon: 'success' })
    //     setTimeout(() => wx.navigateBack(), 1500)
    //   }
    // })
  }
})
