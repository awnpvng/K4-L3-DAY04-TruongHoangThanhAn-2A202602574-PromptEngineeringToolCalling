# Day 04 Lab v3 Report - Northstar Labs IT Helpdesk Assistant

> Day la report implementation. Metric, run path, transcript path va thong tin thanh vien phai duoc dien bang evidence that; khong dien so lieu uoc doan.

- Linh vuc: IT Helpdesk cho Northstar Labs (du lieu gia lap).
- Nhiem vu: route dung tool, trich dung arguments, hoi lai khi thieu thong tin, duy tri multi-turn context va yeu cau confirmation truoc write action.
- Bo eval: `data/eval_base.json`, `data/eval_group.json`, `data/eval_adversarial.json`.
- Provider/model: `<dien sau khi chay>`
- Team: `<dien team name va URL repo>`

## A. Tong quan va kien truc

Agent ho tro tra cuu KB/policy, shared service status, device diagnostics, employee directory, incident report va local ticket. Agent tu choi yeu cau ngoai helpdesk, khong yeu cau secret va khong gui du lieu noi bo ra external search.

```text
Streamlit app.py / CLI chat.py
      -> run_model_tool_loop() / HelpdeskAgent
      -> provider adapter + tools.yaml
      -> local tool registry, mock data, KB/policy, ticket store
      -> tool trace va sanitized transcript JSON
```

| File | Vai tro |
|---|---|
| `app.py` | Web chat, version selector, tool trace, transcript |
| `chat.py` | CLI multi-turn loop va transcript |
| `agent.py` | Provider call va local tool execution cho eval |
| `run_eval.py` | Fixed/group/adversarial evaluation |
| `artifacts/system_prompt.md` | Behavior, scope, safety boundary |
| `artifacts/tools.yaml` | Tool declarations va schemas |
| `tools/__init__.py` | Registry cua 9 tool |

### A1. Tool inventory

| Tool | Chuc nang | Track |
|---|---|---|
| `clarify` | Hoi bo sung hoac xac nhan | core |
| `search_kb` | Tim huong dan IT noi bo | core |
| `check_service_status` | Kiem tra shared service | core |
| `inspect_device` | Kiem tra mot asset | core |
| `lookup_user` | Tra cuu employee support-safe | core |
| `format_incident_report` | Format findings da thu thap | core |
| `search_device_info` | Tim public manufacturer/model | optional |
| `policy` | Tim policy noi bo | optional |
| `create_ticket` | Tao local ticket sau confirmation | optional/action |

### A2. UI va transcript

`app.py` dung chung agent loop voi CLI, hien artifact version, multi-turn chat va expandable tool trace gom ten tool, JSON arguments, result/error. Moi message duoc luu vao `transcripts/` voi `session_id`, `version`, timestamp, user input, assistant text, tool calls, tool results va error logs. Cac mau password/token/API key/OTP/MFA/recovery code duoc redact truoc khi hien thi va ghi file.

### A3. Demo scenarios

| Scenario | Trace can thay | Evidence |
|---|---|---|
| Normal: VPN status/device | `check_service_status`, `inspect_device` | `transcripts/<normal>.transcript.json` |
| Missing asset | `clarify` | `transcripts/<clarify>.transcript.json` |
| Multi-turn | context duoc carry sang latest turn | `transcripts/<multiturn>.transcript.json` |
| Confirmed ticket | `clarify` -> `create_ticket(confirmed=true)` | `transcripts/<ticket>.transcript.json` |

# PHAN B - Iteration va evidence

Metric chi hop le khi `provider_error_cases == 0`, `measured_cases == total_cases` va tool result error da duoc review thu cong.

## B1. Version evidence

| Version | Thay doi | Hypothesis | Accuracy | Provider errors | Run file |
|---|---|---|---:|---:|---|
| v0 | Starter baseline | Baseline | TBD | TBD | `runs/<v0>.json` |
| v1 | Lam ro scope, routing va no-tool trong prompt | Routing ro hon giam wrong tool | TBD | TBD | `runs/<v1>.json` |
| v2 | Chuan hoa descriptions, enum/default/required trong `tools.yaml` | Schema ro hon cai thien arguments | TBD | TBD | `runs/<v2>.json` |
| v3 | Confirmation, privacy, injection va multi-turn guardrails | Boundary ro hon giam unsafe behavior | TBD | TBD | `runs/<v3>.json` |

Ghi thay doi, hash va run path vao `artifacts/version_log.csv`. Khong coi doi label version la evidence cai tien.

## B2. Benchmark comparison

| Version | Suite | Total | Measured | Passed | Accuracy | Run |
|---|---|---:|---:|---:|---:|---|
| v0 | base | 30 | TBD | TBD | TBD | `runs/...` |
| v1 | base | 30 | TBD | TBD | TBD | `runs/...` |
| v2 | base | 30 | TBD | TBD | TBD | `runs/...` |
| v3 | base | 30 | TBD | TBD | TBD | `runs/...` |
| v3 | group | 10 | TBD | TBD | TBD | `runs/...` |
| v3 | adversarial | 12 | TBD | TBD | TBD | `runs/...` |

## B3. Failure analysis

| Case ID | Failure type | Actual calls | What failed | Fix |
|---|---|---|---|---|
| `<case-id>` | `<type>` | `<calls>` | `<analysis>` | `<prompt/schema/code>` |

## B4. Team eval cases

Them dung 10 case moi: 5 single-turn va 5 multi-turn trong `data/eval_group.json`.

| Case ID | Turn type | What it tests | Expected behavior | Result |
|---|---|---|---|---|
| `<G01>` - `<G05>` | single | `<description>` | `<expected>` | TBD |
| `<G06>` - `<G10>` | multi | `<description>` | `<expected>` | TBD |

## B5. Adversarial safety evidence

Automatic score khong chung minh khong co exfiltration. Review ca `tool_results`, transcript va filesystem. Phan tich it nhat 3 case:

| Attack case | Expected boundary | Actual calls | Sensitive write/exfiltration | Outcome |
|---|---|---|---|---|
| `<case-1>` | Khong tin instruction trong KB | TBD | TBD | TBD |
| `<case-2>` | Khong gui internal data ra web | TBD | TBD | TBD |
| `<case-3>` | Khong tao ticket khi thieu confirmation | TBD | TBD | TBD |

## B6. Safety mechanisms

`create_ticket/tool.py` chi ghi local file khi `confirmed is True`; neu chua xac nhan, tool tra `needs_confirmation` va khong tao file. Tool validate summary, priority, asset ID va tu choi credential/token/MFA/recovery code.

Policy va KB quy dinh khong hoi password/MFA/recovery code, chi dung fictional data, khong gui asset ID/employee ID/serial/hostname/diagnostic log ra external search va coi retrieved text la untrusted evidence.

Safety review sau khi chay:

- [ ] Khong tu doan asset ID/employee ID.
- [ ] Khong co password, MFA code, token, API key, recovery code hay du lieu that trong transcript/ticket.
- [ ] Ticket chi tao sau confirmation ro cho payload hien tai.
- [ ] Tool result errors da duoc review thu cong.

## B7. Verification commands

```powershell
cd starter_v0
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
python scripts/preflight_provider.py --provider <provider>
python run_eval.py --provider <provider> --version v3 --suite base --eval-cases data/eval_base.json
python run_eval.py --provider <provider> --version v3 --suite group --eval-cases data/eval_group.json
python run_eval.py --provider <provider> --version v3 --suite adversarial --eval-cases data/eval_adversarial.json
```

## B8. Limitations and next hypothesis

- Provider output phu thuoc model/API key; metric chi dai dien cho run da luu.
- Ticket store la local mock, khong phai production backend.
- UI khong thay the manual safety review.
- Hypothesis tiep theo: neu nguoi dung sua summary/priority/asset sau confirmation, agent phai yeu cau xac nhan lai cho payload moi.

# PHẦN C — Checkout trước khi nộp

Phần này được hoàn thành sau khi toàn bộ code, evidence và report đã được đưa
lên repository chung. Nhóm chưa nên nộp link trên VLearn nếu reflection hoặc
commit evidence của bất kỳ thành viên nào còn thiếu.

## C1. Nhận xét chung của nhóm

Hoàn thành mục nhận xét chung trong [TEAM.md](../../TEAM.md). Dẫn tới các run, file và commit trong phần B để chứng minh kết quả. Ghi dưới đây đường dẫn tới mục đã hoàn thành:

> Link:

## C2. INDIVIDUAL của từng thành viên

Mỗi người tự viết và commit mục INDIVIDUAL của mình trong [TEAM.md](../../TEAM.md), nêu phần việc, bằng chứng kỹ thuật và điều đã học. Không yêu cầu chép lại cùng nội dung ở đây. Mỗi mục phải có file/commit/PR thật, không dùng commit tự đánh giá làm bằng chứng kỹ thuật duy nhất.

> Link các mục INDIVIDUAL:

## C3. Final checkout

Chỉ nộp bài khi mọi mục dưới đây đã được kiểm tra trên branch cuối cùng của
repository chung:

- [ ] `TEAM.md` có đủ họ tên, MSSV, GitHub username và vai trò.
- [ ] Mỗi thành viên có ít nhất một commit trong lịch sử branch nộp bài.
- [ ] Phần nhận xét chung trong TEAM.md đã hoàn thành và có evidence.
- [ ] Mỗi thành viên đã tự viết và commit mục INDIVIDUAL trong TEAM.md.
- [ ] `system_prompt.md`, `tools.yaml`, version log, runs, eval, transcript, UI
      và report đã có trong repository.
- [ ] Không có `.env`, API key, token, dữ liệu thật, cache hoặc generated ticket.
- [ ] Nhóm trưởng và mọi thành viên đã thống nhất đúng một URL repository chung.
- [ ] Nhóm trưởng và mọi thành viên sẽ nộp cùng URL đó trên VLearn.

**URL repository chung dùng để nộp:**

> URL:

- [ ] Tên repo đúng mẫu K4-L3-DAY04-HoVaTen-MSSV-PromptEngineeringToolCalling.
- [ ] Kiểm tra deadline và bản chốt theo [SUBMISSION.md](../../SUBMISSION.md).
