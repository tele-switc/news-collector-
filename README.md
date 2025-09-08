# 外刊聚合 · 2025+（OpenAI 风格）

- 每天 08:00（北京时间）自动抓取：WIRED / The Economist / Scientific American / The Atlantic / NYTimes / WSJ
- 合规模式：默认仅展示标题、作者、时间、摘要、原文链接
- 全文模式（可选）：在你具备合法授权/许可的前提下，配置 Diffbot Token 并设置 FULLTEXT_WHITELIST 域名后，对这些域名展示全文

## 使用
1. 复制本仓库文件到你的 GitHub 仓库
2. Settings → Pages → 部署 docs 文件夹
3. 设置 Secrets/Variables：
   - Secrets: `DIFFBOT_TOKEN`（可选，用于全文）
   - Variables: `FULLTEXT_WHITELIST`（可选，逗号分隔域名）
4. Actions → 运行 Backfill（建议） → 等待 Daily（08:00/08:10/08:30）自动执行
5. 访问 Pages URL 查看网站

## Gift 链接
- 在 `docs/gifts.json` 中维护 `{ "<item_id>": "https://gift-link" }` 映射
- item_id = 规范化 URL 的 SHA1（页面元素复制 ID 即可）

## 重要
- 请仅在你具有相应授权时展示全文内容；否则把 FULLTEXT_WHITELIST 留空，网站会仅展示元数据。
- 若需更高覆盖率的授权来源（如 NewsCatcher/AYLIEN/Factiva/LexisNexis），可按需添加连接器。
