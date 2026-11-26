# 指定功能图解手册 · Task First Manual

把“这产品有几十个功能，我只想用其中两个”变成一份能拿在手上照做的中文指南。适用于实体设备、软件和需要配套使用的多个产品。

**[看一份做好的三步图解 →](examples/labels/README.md)**　打开随附的标签预览器，照三张图把「工具箱」改成四张，再切换方案验一次。

**[看一份实体产品操作卡 →](examples/watch-593/README.md)**　用卡西欧 593 手表演示“只调一个小时”，对照实体按键和屏幕闪动位置。

## 用法

安装后，在 Codex 里直接说：

> 用 $task-first-manual 给我做一份中文图解。我用的是［产品、型号或版本］，只想做［功能］。我最容易卡在［位置，如有］。我要［手机上看 / 一张打印卡 / 完整 PDF］。

只知道目标也可以开始，例如“我只想让录音笔录一段，再找到刚才的录音”。有铭牌照片、界面截图或原厂手册可以一起提供。已经在上下文里确认过的型号、附件和阅读习惯可以沿用。

## 安装到 Codex

下载或克隆本仓库。在 macOS 或 Linux 上，从仓库根目录执行以下命令。若同名技能已存在，命令会停下，供你比较版本。

```sh
skill_root="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skill_root" &&
  mkdir "$skill_root/task-first-manual" &&
  cp -R skills/task-first-manual/. "$skill_root/task-first-manual/"
```

也可以手动把完整的 `skills/task-first-manual` 文件夹放进 Codex 的 `skills` 目录。新建对话后用 `$task-first-manual` 调用。其他支持 Markdown 指令的助手可以直接读取[技能入口](skills/task-first-manual/SKILL.md)，并保留旁边的 `references` 目录。

## 这套方法怎样决定写什么

|制作时先问|它会改变手册里的什么|
|---|---|
|读者最后想看到什么？|从目标倒推操作顺序，保留必需的前置条件。|
|手里到底是哪一款、哪一套？|先对车型、设备、账号或配置档逐一配对，再分配步骤。|
|读者的手和眼此刻在哪里？|图上圈具体位置，正文写手势和印字，下一行给可观察的反馈。|
|怎么知道保存了、连上了、真的起作用了？|分别写读回、连接和实际动作；涉及实体运行时标明待实测之处。|
|一页看得懂，为什么下一页卡住？|拿读者认可的一页作样本，逐步检查其余页面，再打开最终成品看图注与圈位。|

[操作卡模板](skills/task-first-manual/references/operation-card.md)可直接改写。[审阅与修订表](skills/task-first-manual/references/review.md)适合在读者指出错配、漏图和步骤跳跃时使用。

本仓库的技能、示例程序、截图和文档以 [MIT 许可证](LICENSE)发布。使用技能制作其他产品手册时，该产品的图片与资料仍按各自授权使用。
