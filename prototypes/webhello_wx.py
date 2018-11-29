# First things, first. Import the wxPython package.
import wx
import wx.html2 
import AppKit
import time

# fix issue with non-ssl URLs
# https://github.com/paulhammond/webkit2png/pull/91/commits/9a96ac8977c386a84edb674ca1518e90452cee88
AppKit.NSBundle.mainBundle().infoDictionary()['NSAppTransportSecurity'] = dict(NSAllowsArbitraryLoads = True)

# Next, create an application object.
app = wx.App()

# Then a frame.
frm = wx.Frame(None, title="Hello World")
browser = wx.html2.WebView.New(frm)

def onload(event):
    browser = event.GetEventObject()
    browser.RunScript("next_script();")
    time.sleep(5)

browser.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, onload, id=wx.ID_ANY)

browser.LoadURL("http://localhost:8000/")

# Show it.
frm.Show()

# Start the event loop.
app.MainLoop()