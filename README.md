# 批量筛选清理群成员
一个用于批量清理QQ群内(划水)成员的爬虫脚本,基于python和selenium

[教程](https://blog.csdn.net/Fandes_F/article/details/119302183)
# 用法
"手动登录后,(设置其他筛选条件)按alt+s可以自动下滑加载全部成员页面(也可以自己用鼠标滚动加载)," 

"加载完页面后,按alt+z开始筛选(没有加载的页面将不会处理),会先筛选出所有符合条件的人," 

"然后以20/批量选中并弹出删除按钮(qq只允许同一批量删除最多20人)" 

"手动确认后按F4键继续选中下一批...一一确认即可" 

"然后手动确认删除(也不是不可以做到自动点击删除,只是手动删除比较谨慎一点...毕竟群命关天)"


# 依赖
pynput#用于快捷键设置方便操作,可以换成其他模块

selenium

于Windows10 python3.7.8下测试一切正常!

