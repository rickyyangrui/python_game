#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx

class CalcFrame(wx.Frame):
  
    def __init__(self, title):
        super(CalcFrame, self).__init__(None, title=title, 
            size=(300, 250))
            
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):
        # 定义BoxSizer，这个东西可以允许我们以行或列放置控件。我们先放个TextCtrl文本框，再放个GridSizer用来放置按钮
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.textprint = wx.TextCtrl(self, style=wx.TE_RIGHT)
        self.equation=""
        vbox.Add(self.textprint, 1, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=4)
        
        # gridsizer允许我们以二维布局控件。四个参数分别是
        # rows, 行数 | cols, 列数 |  vgap, 格子之间垂直间隔 | hgap, 格子之间水平间隔
        gridBox = wx.GridSizer(5, 4, 5, 5)

        labels=['AC','DEL','pi','CLOSE','7','8','9','/','4','5','6',
                '*','1','2','3','-','0','.','=','+']
        
        # 计算器的重点在于Button的回调函数,点击不同按钮我们希望根据按钮的label选择不同的回调函数进行绑定。
        # 因此我们可以这样实现放置按钮到gridbox
        for label in labels:
            buttonIterm = wx.Button(self,label=label)
            self.createHandler(buttonIterm,label)
            gridBox.Add(buttonIterm, 1, wx.EXPAND)
           
        vbox.Add(gridBox, proportion=7, flag=wx.EXPAND)
        self.SetSizer(vbox)

    # 创建按钮处理方法
    # 根据label的不同，我们把按钮分别绑定到5个不同的回调函数上
    def createHandler(self,button,labels):
        item = "DEL AC = CLOSE"
        if labels not in item:
            self.Bind(wx.EVT_BUTTON,self.OnAppend,button)
        elif labels == 'DEL':
            self.Bind(wx.EVT_BUTTON,self.OnDel,button)
        elif labels == 'AC':
            self.Bind(wx.EVT_BUTTON,self.OnAc,button)
        elif labels == '=':
            self.Bind(wx.EVT_BUTTON,self.OnTarget,button)
        elif labels == 'CLOSE':
            self.Bind(wx.EVT_BUTTON,self.OnExit,button)
    # 回调函数，添加运算符与数字
    def OnAppend(self,event):
        eventbutton = event.GetEventObject()
        label = eventbutton.GetLabel()
        self.equation += label
        self.textprint.SetValue(self.equation)
    def OnDel(self,event):
        self.equation = self.equation[:-1]
        self.textprint.SetValue(self.equation)
    def OnAc(self,event):
        self.textprint.Clear()
        self.equation=""
    def OnTarget(self,event):
        string = self.equation
        try:
            target = eval(string)
            self.equation = str(target)
            self.textprint.SetValue(self.equation)
        except SyntaxError:
            dlg = wx.MessageDialog(self,u'格式错误，请输入正确的等式!',
                                u'请注意', wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            
    def OnExit(self,event):
        self.Close()
        
if __name__ == '__main__':
  
    app = wx.App()
    CalcFrame(title='Calculator')
    app.MainLoop()
