# 任務管理系統 系統設計

完整的任務管理系統說明文檔。

## 系統概述

這是一個基於 YAML 格式的分層任務管理系統，專為 LLM Agent 協作和人工管理設計。

### 核心特點

- **YAML 格式** - 每個任務為獨立檔案，結構清晰，易於人類閱讀與 Agent 編輯
- **UUID 識別** - 每個任務全域唯一
- **分層目錄** - 按 `project/module` 組織結構，避免單一目錄檔案過多
- **原子性** - 檔案層級的鎖定與操作，減少協作衝突
- **Schema 強制性** - 透過 JSON Schema 確保所有 Agent 輸出的任務格式統一

## 檔案結構

### 目錄佈局

```
pog-task/
├── README.md                       # 系統總覽
├── task.schema.json                # 任務內容的 JSON Schema
├── pog-task.py                     # 任務校驗工具
├── pog-task-agent-instructions.md  # Agent 操作指南
├── pog-task-design.md              # 本文件 - 系統設計
└── list/                           # 實際任務列表
    └── {project}/
        └── {module}/
            ├── {task-title}.yaml
            └── record/{uuid}/record.md
```

### 檔案路徑與命名規則

**格式**：`pog-task/list/{project}/{module}/{task-title}.yaml`

| 元件 | 說明 | 範例 |
|------|------|------|
| `{project}` | 專案前綴 | `pog`, `common`, `alpha` |
| `{module}` | 模組名稱 | `improve`, `core`, `activate`, `01-auth` |
| `{task-title}` | 任務標題 | `整合支付 API`, `修復登入 Bug` |

**規則**：
- `{project}` 與 `{module}` 使用小寫與連字符
- `{task-title}` 建議維持與任務對象中的 `title` 一致（可做檔名安全處理）

## 任務校驗 (Validation)

為了維護數據完整性，系統引入了 `task.schema.json`。

### 校驗方式

開發者或 Agent 可以執行：
```bash
python3 pog-task.py
```

該腳本會：
1. 讀取 `task.schema.json`。
2. 掃描 `list/` 下所有 `.yaml` 檔案。
3. 輸出每個檔案的校驗結果（OK 或具體的 SCHEMA ERROR）。

## YAML 文件內容結構

每個 YAML 文件代表一個任務對象。

### 任務對象 (Task Object)

**基本結構範例**:
```yaml
type: "task"
id: "9d8f6c3a-2e1b-4f5a-8b3c-1d5e7f9a2b4c"
title: "設計任務管理功能"
status: "in_review"
created_at: "2026-02-04T15:05:00+08:00"
category: "design"
priority: "high"
# ... 其他欄位
```

**完整欄位說明請參考**: [Agent 指南](./pog-task-agent-instructions.md)

## 嵌套任務

### 父子關係

**父任務** 標識其為頂層或在 checklist 中描述子項。
**子任務** 透過 `parent_task` 欄位引用父任務的 UUID：
```yaml
id: "child-uuid"
parent_task: "parent-uuid"
```

## 任務記錄 (Record)

### 路徑結構

```
pog-task/list/{project}/{module}/record/{task-uuid}/record.md
```

用於記錄詳細的執行過程、原始 Prompt、技術決策和產出物。

## 狀態轉換與優先級

請參考 [README.md](./README.md) 或 [Agent 指南](./pog-task-agent-instructions.md) 了解詳細的業務邏輯。

## 最佳實踐

1. **一事一簽** - 每個任務必須有獨立的 YAML 檔案。
2. **校驗先行** - 提交或更新任務後務必執行 `pog-task.py`。
3. **目錄正確** - 確保任務放置在正確的專案與模組目錄下。
