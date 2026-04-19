# English Words Forced Learning

一个“强制重复记忆”英语单词的小项目：
- 展示英文单词；
- 你必须输入中文翻译；
- 输入错误会被重复加入队列；
- 连续错到阈值前不会放过，直到真正记住。

## 技术栈
- Python 3.10+
- FastAPI + Jinja2
- 纯 HTML/CSS（无前端构建步骤）
- Pytest（基础单元测试）

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

打开浏览器访问：`http://127.0.0.1:8000`

## 数据文件
默认词库在：

- `app/data/words.json`

格式示例：

```json
[
  {"word": "apple", "translation": "苹果"},
  {"word": "library", "translation": "图书馆"}
]
```

## 测试

```bash
pytest
```

## 说明
- 项目使用 cookie 区分学习会话（同一浏览器用户一份进度）。
- 若要重新开始可点页面的“重置学习进度”。
- 当前实现是轻量内存会话，重启服务后会话会清空。
