# B站热门视频数据采集与分析

一个基于 B站热门榜开放接口的个人练手项目：**采集 → 入库 → 清洗 → 分析宽表**全流程。

## 功能特性

- 多页爬取 B站热门榜（每页 20 条，默认 25 页 = 500 条），抓取字段：分区、标题、简介、作者、播放 / 评论 / 点赞 / 收藏 / 分享 / 投币
- `INSERT ... ON DUPLICATE KEY UPDATE` 增量更新：重复运行只刷新播放量、点赞等可变指标，不产生重复数据
- Pandas 缺失值清洗：简介为空 / `-` 统一填充占位文案；借助「临时表 + `UPDATE JOIN`」把清洗结果回写源表，不破坏主键与字段约束
- 派生指标加工：播放量、点赞量换算成「万」并保留两位小数，输出中文分析宽表 `videos_data`
- 使用 uv 管理依赖（`pyproject.toml` / `uv.lock`）

## 项目结构

```
pj2__pachong
├── pachong/              # 爬虫包
│   ├── __init__.py
│   └── pac.py            # Bpachong(page)：多页抓取热门榜，返回视频 dict 列表
├── connet_sql.py         # 连接 MySQL，爬取并增量写入 videos 原始表
├── pandas_clean.py       # pandas 清洗 + 回写源表 + 生成 videos_data 分析宽表
├── fsql.sql              # 建库建表脚本（首次初始化用，会 drop 重建）
├── README.md
├── .gitignore
├── pyproject.toml        # 项目配置与依赖声明
└── uv.lock
```

## 环境要求

- Python >= 3.14
- uv（可选，推荐）
- 本地 MySQL 8.x，默认账号 `root` / 密码 `mysql`（见脚本内连接配置）

## 快速开始

```bash
# 1. 安装依赖
uv sync

# 2. 初始化数据库（首次/重置时执行，会 drop 并重建 videos、videos_data）
mysql -u root -p < fsql.sql

# 3. 爬取热门榜并写入原始表
python connet_sql.py

# 4. 清洗缺失值 + 生成分析宽表
python pandas_clean.py
```

## 表结构

### videos（原始表，脚本建表）
| 字段 | 类型 | 说明 |
|---|---|---|
| aid | char(15) PK | 视频唯一 ID |
| tname | varchar(20) | 分区 |
| title | varchar(150) | 标题 |
| deses | varchar(500) | 简介（清洗目标列） |
| author | varchar(50) | UP 主 |
| view / reply / ulike / favorite / share / coin | int | 播放 / 评论 / 点赞 / 收藏 / 分享 / 投币 |

### videos_data（分析宽表，Pandas 自动建表）
aid、观看量（万）、分享、评论、点赞（万）、收藏、类别、标题、投币、视频简介

## 数据口径说明

- `观看量（万） = view / 10000`，`点赞（万） = ulike / 10000`，均保留两位小数
- 收藏 / 分享 / 评论 / 投币保留原始整数
- 清洗规则：简介为 `NULL` / 空字符串 / `-` 时，填充为「该视频的简介为空！」
