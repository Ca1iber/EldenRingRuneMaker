# EldenRingRuneMaker

法环蒙格温王朝刷魂辅助脚本。按一次 `Win+N` 开始循环，再按一次会停止；停止不会打断当前刷魂周期，会在当前周期执行完后停下。

## 使用前准备

1. 第一个物品栏放置黄金角币或黄金鸡爪，用于提高刷魂效率。
2. 建议装备金色粪金龟护符；可搭配献斗剑护符、圣对蝎护符，提高神躯化剑战技伤害。
3. 传送到“通往蒙格温王朝的道路上”赐福。
4. 右手手持神躯化剑。
5. 脚本运行期间保持游戏窗口在前台，不要切到其他程序。

## 安装

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 运行

```bash
python ERScript.py
```

运行后：

- `Win+N`：开始/停止刷魂循环。
- 系统托盘 `Start / Stop`：开始/停止刷魂循环。
- 系统托盘 `Exit`：退出脚本。

## 开发说明

刷魂动作序列定义在 `RUNE_FARM_SEQUENCE` 中。当前重构保留了原始脚本的按键顺序和每段 `sleep` 时长，仅将热键监听、托盘、循环控制和动作执行拆分，便于维护和测试。

运行测试：

```bash
python -m unittest discover -s tests
```
