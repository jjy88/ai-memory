
# RedNoteSellingBusiness1MdollarProject


太棒了！这是为你的项目量身定制的 GitHub 多人协作说明，适合写在 README.md 的最后一节，或者单独做成 CONTRIBUTING.md 也可以。

⸻

🤝 Git 协作说明（适用于私有项目）

🔐 主分支保护策略

我们启用了 GitHub 的主分支保护机制，确保主分支 main：
	•	❌ 不允许直接 push
	•	✅ 所有更新必须通过 Pull Request (PR)
	•	✅ 每次合并都需至少一次人工 review
	•	✅ 强制线性历史（无 merge commit）

⸻

🚧 每位协作者的开发规范

1. 创建自己的开发分支（不要直接在 main 上开发）

git checkout -b feat-your-feature-name

例子：

git checkout -b feat-chat-api
git checkout -b fix-frontend-display

命名建议：使用 feat-（新功能）、fix-（修复）、test-（测试）等前缀。

⸻

2. 推送自己的分支

git push origin feat-your-feature-name



⸻

3. 在 GitHub 发起 Pull Request

前往 GitHub 项目 → 比较你的分支 → 发起 PR 到 main
确保：
	•	✅ 描述清楚你修改了什么
	•	✅ 代码自测通过
	•	✅ 如果是重要逻辑改动，请 tag @队友 进行 review

⸻

4. 合并策略：Squash & Merge

所有 PR 合并时请使用 Squash & Merge，保持主分支 commit 历史整洁。

⸻

🧠 推荐配置（已启用）
	•	✅ main 分支不可强推、不可删除
	•	✅ 所有改动需经 PR 审核
	•	✅ 后续会接入自动化测试（例如格式检查、pytest）

⸻

📦 常见问题

问题	解决方式
clone 后不能 push 到 main	正常行为，请使用自己的分支
PR 提交失败	确保通过 review 或未启用的保护规则
我想快速同步最新代码	git pull origin main --rebase



⸻

✍️ 项目协作守则
	1.	每个人只在自己的分支开发
	2.	不 push 到 main，除非紧急 hotfix 并经同意
	3.	保持沟通、互相 review，确保项目稳步推进

⸻

如果你需要，我可以顺手再帮你生成一个 PR 模板（.github/pull_request_template.md），每次创建 PR 都自动提醒协作者填写标题、变更说明、是否测试通过等，进一步规范流程。需要的话我可以马上写！
