CS2 Toolbox · 🔥 专为CS2玩家打造的快捷沟通工具箱​
A lightweight desktop tool for CS2 players to send preset messages quickly via buttons or hotkeys, improving in-game communication efficiency.​
✨ 核心功能 | Core Features​
快捷话术发送：内置常用游戏话术，点击即发，支持自定义添加/删除​
一键开火喊话：顺序/随机两种轮播模式，F2快捷键快速触发，适配对战场景​
文本批量管理：支持TXT文件导入词汇，自动保存历史数据，下次启动无缝加载​
便捷快捷键：F1（显隐窗口）、F2（开火喊话）、ESC（退出程序）​
博客直达：一键访问作者个人博客，快速获取更多资源​
简洁UI：深色主题设计，游戏内不刺眼，控件清晰易操作​
📸 界面展示 | Screenshot​
![CS2 Toolbox Interface](http://youke.xn--y7xa690gmna.cn/s1/2026/01/20/696fa39dca614.webp)（替换为你的实际界面截图链接）​
🛠️ 技术栈 | Tech Stack​
开发语言：Python 3.x​
GUI框架：Tkinter（原生轻量，无额外依赖）​
核心依赖：pyperclip（剪贴板操作）、Pillow（图片处理，已移除背景功能）​
打包工具：PyInstaller（Windows平台EXE打包）​
兼容系统：Windows 10/11（32/64位）​
📥 下载与使用 | Download & Usage​
方式1：直接下载EXE（推荐）​
前往 Releases 页面下载最新版EXE文件​
右键EXE文件 → 以管理员身份运行（必须，否则无法正常发送文本）​
无需安装，启动即可使用所有功能​
方式2：源码运行​
​
代码块​
​
方式3：自行打包为EXE​
​
代码块​
​
⌨️ 快捷键说明 | Hotkeys​
​
​
​
	
​
​
F1​
	
显示/隐藏窗口（游戏内快速切换，不遮挡视野）​
F2​
	
触发一键开火喊话（游戏内快速调用预设文本）​
ESC​
	
安全退出程序（自动保存所有文本配置）​
​
⚠️ 注意事项 | Notes​
必须以管理员身份运行程序，否则无法正常向CS2窗口发送文本​
游戏内使用时，请确保CS2窗口处于前台状态​
文本配置文件（cs2_msg.txt、cs2_fire_config.txt）自动生成于程序运行目录，可手动编辑​
自定义文本支持中文、英文等字符，无长度限制​
图标打包失败时，可参考 图标问题解决方案​
🔧 常见问题 | FAQ​
Q1：打包后EXE没有自定义图标？​
A：确保图标为标准ICO格式（256x256像素），使用绝对路径指定图标，打包命令添加--noupx 参数禁用压缩。具体步骤：​
用在线工具（convertio）将图片转为标准ICO​
使用绝对路径打包：pyinstaller -F -w --icon=绝对路径\cs2_icon.ico --noupx cs2_toolbox.py​
若仍无效，可使用 Resource Hacker 手动替换EXE图标​
Q2：游戏内无法发送文本？​
A：1. 确认程序以管理员身份运行；2. 确保CS2窗口处于前台；3. 检查快捷键是否冲突（关闭其他占用F1/F2的程序）​
📝 版本日志 | Changelog​
v1.0.0（初始版本）​
实现核心话术发送、添加、删除、导入功能​
支持开火喊话顺序/随机轮播模式​
添加F1/F2/ESC快捷键支持​
内置作者博客直达按钮，优化弹窗提示​
移除背景图功能，简化UI，提升稳定性​
👨‍💻 作者信息 | Author​
作者：初开​
个人博客：chukai.cc​
GitHub：LIUQiu111​
📜 许可证 | License​
本项目采用 MIT 许可证开源，允许个人和商业使用，二次开发或分发时请保留作者信息和版权声明。​
MIT License © 2024 初开​
🌟 支持与反馈​
如果觉得这个工具对你有帮助，欢迎 Star 和 Fork 本仓库！​
如有功能建议或Bug反馈，可通过以下方式联系我：​
GitHub Issues：提交Issue​
个人博客：chukai.cc
