# CSVToMeshAuto

<p align="center">
  <img src="https://img.shields.io/badge/Blender-2.80%20%E2%80%93%204.x-orange?logo=blender&logoColor=white" alt="Blender">
  <img src="https://img.shields.io/badge/license-GPL%20v3-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/version-2.0.0-brightgreen.svg" alt="Version">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <b>将 RenderDoc 导出的 CSV 文件自动转换为 Blender 三维网格</b><br>
  支持位置列与 UV 列智能检测，一键导入
</p>

---

## 功能特性

| 功能 | 说明 |
|---|---|
| 位置列自动检测 | 优先匹配 `POSITION` / `SV_POSITION` → `TEXCOORD0` → 兜底使用列 2~4 |
| UV 列自动检测 | 跳过位置列后，匹配首个 `TEXCOORD` 或 `uv` 开头的列 |
| 输入校验 | 自动验证数据完整性，异常时弹出详细错误提示 |
| 进度反馈 | 导入过程显示进度条 |
| 全平台支持 | 兼容 Windows / macOS / Linux |

## 安装

1. 打开 Blender → `编辑` → `偏好设置` → `插件`
2. 点击 `安装`，选择 `CSVToMeshAuto.zip`
3. 搜索 `CSVToMeshAuto`，勾选启用
4. 在 3D 视图右侧边栏（按 `N` 键）找到 `CSVToMeshAuto` 标签页

> 如果安装后插件列表不显示，请检查 zip 内结构是否为 `CSVToMeshAuto/__init__.py`，且文件开头不能有 UTF-8 BOM。

## 快速开始

### 自动模式（推荐）

1. 保持 `自动检测` 复选框勾选（默认开启）
2. 点击 `导入 CSV`
3. 选择从 RenderDoc 导出的 CSV 文件
4. 完成 — 位置列和 UV 列自动识别

### 手动模式

当自动检测失效时（非标准 CSV 格式）：

1. 取消勾选 `自动检测`
2. 用文本编辑器打开 CSV 文件，查看第一行表头（列号从 **0** 开始）
3. 填入数值：
   - **位置列起始**：顶点 X 坐标所在列号（需连续 3 列为 X / Y / Z）
   - **UV 列起始**：UV 的 U 坐标所在列号（需连续 2 列为 U / V）
4. 点击 `导入 CSV`

## RenderDoc 导出 CSV 的正确方式

1. 在 RenderDoc 中打开捕获帧
2. 选择目标 Draw Call → `Mesh Viewer`
3. 右上角 `Export` → 选择 `CSV` 格式
4. 导出的 CSV 表头通常包含 `VTX, IDX, TEXCOORD0.x, TEXCOORD0.y, ...`

## 错误提示速查

| 提示内容 | 原因 | 解决办法 |
|---|---|---|
| 数据行数不是 3 的倍数 | CSV 行数无法整除 3，无法构成完整三角形 | 检查 RenderDoc 导出是否完整 |
| 未找到顶点位置列 | 表头中没有 POSITION / SV_POSITION / TEXCOORD0 | 切换到手动模式指定列号 |
| 位置列 / UV 列不是数字 | 指定列的内容无法解析为浮点数 | 检查列号是否正确 |
| 列数太少 | CSV 不足 5 列 | 确认文件是从 Mesh Viewer 导出 |
| 读取文件失败 | 文件损坏或编码异常 | 检查文件完整性 |

## 自动检测逻辑

1. **位置列检测**：优先匹配 POSITION / SV_POSITION → 其次 TEXCOORD0 → 兜底使用列 2~4
2. **UV 列检测**：跳过位置列后，匹配第一个 TEXCOORD 或 uv 开头的列
3. 检测结果在 Blender 底部状态栏显示

## 已知限制

- 仅取第一套 UV 通道
- 不导入法线数据（Blender 自动计算）
- 不支持自定义分隔符（仅逗号 `,`）
- 位置列必须连续 3 列，UV 列必须连续 2 列

## 兼容性

| Blender 版本 | 状态 |
|---|---|
| 2.80 ~ 2.93 | 支持 |
| 3.x | 支持 |
| 4.x | 支持 |

## 版本历史

| 版本 | 更新内容 |
|---|---|
| v2.0.0 | 位置列自动检测、输入校验、进度条、错误弹窗 |
| v1.0.0 | 初始版本，UV 列自动检测 |

## 许可证

本项目采用 [GNU General Public License v3.0](LICENSE) 许可证。

> 如果原版 CSVToMesh 插件已安装，两者可以共存，不会冲突。