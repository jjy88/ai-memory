# 贡献指南

感谢您对 AI Memory 项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告 Bug

如果您发现了 bug，请[创建一个 issue](https://github.com/jjy88/ai-memory/issues/new)，并包含以下信息：

- Bug 的详细描述
- 复现步骤
- 预期行为
- 实际行为
- 您的环境信息（操作系统、Python 版本等）

### 提交功能请求

我们欢迎新功能的建议！请[创建一个 issue](https://github.com/jjy88/ai-memory/issues/new)，并说明：

- 功能的详细描述
- 使用场景
- 可能的实现方案

### 提交代码

1. **Fork 项目**

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **编写代码**
   - 遵循现有代码风格
   - 添加必要的测试
   - 更新相关文档

4. **运行测试**
   ```bash
   pytest
   flake8 . --max-line-length=127
   ```

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **推送到 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**

## 代码规范

### Python 代码风格

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- 使用 4 空格缩进
- 最大行长度 127 字符
- 使用有意义的变量名和函数名

### Commit 消息规范

使用语义化提交消息：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具链更新

示例：
```
feat: add JWT authentication system
fix: resolve file upload size limit issue
docs: update API documentation
```

## 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_auth_api.py

# 生成覆盖率报告
pytest --cov=. --cov-report=html
```

### 编写测试

- 为新功能添加测试
- 确保测试覆盖率不降低
- 测试应该独立且可重复

## 文档

- 更新 README.md（如有需要）
- 为新 API 添加 docstring
- 更新 API 文档

## 开发环境设置

1. **克隆仓库**
   ```bash
   git clone https://github.com/jjy88/ai-memory.git
   cd ai-memory
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov flake8
   ```

4. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件
   ```

5. **运行应用**
   ```bash
   python main.py
   ```

## 代码审查

所有提交都会经过代码审查：

- 代码质量
- 测试覆盖率
- 文档完整性
- 性能影响

## 社区准则

- 尊重他人
- 建设性反馈
- 欢迎新手
- 保持友好和专业

## 许可证

通过贡献代码，您同意您的贡献将按照 MIT 许可证进行许可。

## 问题？

如有任何问题，请：
- 创建 [GitHub Issue](https://github.com/jjy88/ai-memory/issues)
- 查看现有讨论

感谢您的贡献！🎉
