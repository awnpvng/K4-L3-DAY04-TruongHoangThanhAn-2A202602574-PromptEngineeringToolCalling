# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm: Trương Hoàng Thành An
- Người đại diện / MSSV: Trương Hoàng Thành An / 2A202602574
- Tên repo: `K4-L3-DAY04-TruongHoangThanhAn-2A202602574-PromptEngineeringToolCalling`
- URL repo, nhánh nộp, commit chốt: https://github.com/awnpvng/K4-L3-DAY04-TruongHoangThanhAn-2A202602574-PromptEngineeringToolCalling, branch main
- Deadline áp dụng và link thông báo đổi hạn nếu có:

## Thành viên

| Họ và tên              | MSSV        | GitHub                                                 | Vai trò và công việc                                                                                                                                                        | File/commit/PR                                                                                                                                                                        |
| ------------------------- | ----------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Trương Hoàng Thành An | 2A202602574 | [awnpvng](https://github.com/awnpvng)                   | **Agent Core Lead & Prompt/Tool Declarations:** quản lý tối ưu hóa agent v0-v3, tinh chỉnh system prompt và tool declarations, tích hợp và quản lý versioning | `starter_v0/artifacts/system_prompt*.md`, `starter_v0/artifacts/tools*.yaml`, `starter_v0/artifacts/version_log.csv`, `starter_v0/runs/`                                      |
| Nguyễn Thị Minh Tiến   | 2A202602997 | [MinhTienNguyen05](https://github.com/MinhTienNguyen05) | **Safety & Eval Dataset Engineer:** xây dựng bộ eval nhóm, phân tích adversarial/safety, phát triển và kiểm thử bonus tool                                     | `starter_v0/data/eval_group.json`, `starter_v0/data/eval_bonus_warranty.json`, `starter_v0/analysis/adversarial_safety_analysis.md`, `starter_v0/tools/check_asset_warranty/` |
| Phan Thị Khánh Linh     | 2A202602360 | [khanhlinh-2005](https://github.com/khanhlinh-2005)     | **UI, Integration & Final Report:** xây Streamlit UI, tích hợp agent loop, hiển thị tool trace, lưu transcript và hoàn thiện report                              | `starter_v0/app.py`, `starter_v0/requirements.txt`, `README.md`, `starter_v0/artifacts/REPORT.md`                                                                             |

## Nhận xét chung

- **Kết quả và bằng chứng:**

  - Hoàn thành 10 eval cases cho nhóm (5 single-turn + 5 multi-turn) trong `eval_group.json`
  - Xây dựng bonus tool `check_asset_warranty` để kiểm tra bảo hành thiết bị
  - Viết phân tích safety cho 12 adversarial cases trong `adversarial_safety_analysis.md`
  - Tích hợp bonus tool vào tools registry và tools.yaml
  - Chạy eval base với custom provider (Qwen): 20/30 cases PASS (66.67%)
  - Tích hợp Streamlit UI để chạy chat multi-turn, chọn provider/version và hiển thị tool trace.
  - Bổ sung transcript JSON có session ID, version, tool calls, tool results và error logs.
- **Thay đổi hiệu quả nhất:**

  - Tạo bonus tool `check_asset_warranty` cung cấp chức năng mới ngoài luồng cơ bản
  - 10 eval cases bao phủ đủ các failure_type: wrong_tool, wrong_arg_value, missing_info, out_of_scope, unnecessary_tool, wrong_boundary
- **Giới hạn còn lại:**

  - Chưa chạy eval group cases và adversarial với custom provider (do thời gian)
  - Cần chạy thêm transcript và demo để hoàn thiện
- **Cách phân công và tích hợp:**

  - Trương Hoàng Thành An: Safety & Eval, Dataset và Bonus Tool.
  - Phan Thị Khánh Linh: UI, Integration và Final Report.
  - Hai phần được tích hợp qua tool registry, agent loop, Streamlit UI và evidence trong report.

## INDIVIDUAL

### Trương Hoàng Thành An — 2A202602574

- **Phần việc và file/commit/PR:**

  - Tạo `starter_v0/data/eval_group.json` - 10 eval cases (5 single-turn + 5 multi-turn)
  - Xây dựng `starter_v0/tools/check_asset_warranty/` - Bonus tool kiểm tra bảo hành (TOOL.md, __init__.py, tool.py)
  - Tạo `starter_v0/data/eval_bonus_warranty.json` - 5 test cases cho bonus tool
  - Viết `starter_v0/analysis/adversarial_safety_analysis.md` - Phân tích 12 adversarial cases
  - Cập nhật `starter_v0/tools/__init__.py` - Đăng ký bonus tool
  - Cập nhật `starter_v0/artifacts/tools.yaml` - Khai báo bonus tool
  - Tạo `starter_v0/providers/custom_provider.py` - Provider cho Qwen/Moonshot
  - Tạo `starter_v0/runs/v0_B_base_custom_20260915T192321182963.json` - Run eval base với Qwen
- **Quyết định, khó khăn và cách xử lý:**

  - Khó khăn: Gemini API key bị PERMISSION_DENIED và rate limit
  - Quyết định: Tạo custom provider cho Qwen sử dụng OpenAI-compatible API
  - Cách xử lý: Dùng `OPENAI_API_KEY` + `OPENAI_BASE_URL` + `MODEL=qwen3.7-flash`
- **Điều đã học:**

  - Hiểu cách thiết kế eval cases cho agent với nhiều failure types khác nhau
  - Học cách xây dựng bonus tool mới theo contract đúng
  - Nắm vững các attack vectors trong adversarial testing (prompt injection, role spoofing, data exfiltration)
  - Hiểu cách tạo custom provider cho OpenAI-compatible API
- **AI/công cụ đã dùng và cách kiểm tra:**

  - Claude Code (current) - Để viết code và phân tích
  - Cách kiểm tra: Chạy `python3 -c "from tools.check_asset_warranty.tool import check_asset_warranty; print(check_asset_warranty('LT-204'))"`
- **Thời điểm đã tự nộp URL repo chung trên VLearn:**

  - 21h00 ngày 15/09/2026

### Nguyễn Thị Minh Tiến — 2A202602997

- **Phần việc và file/commit/PR:**

  - Xây dựng `starter_v0/data/eval_group.json` với 10 case tự viết: 5 single-turn và 5 multi-turn.
  - Xây dựng `starter_v0/data/eval_bonus_warranty.json` với 5 case kiểm thử chức năng bonus.
  - Viết `starter_v0/analysis/adversarial_safety_analysis.md` và phân tích 12 case an toàn.
  - Xây dựng `starter_v0/tools/check_asset_warranty/` gồm `TOOL.md`, `__init__.py` và `tool.py`.
  - Cập nhật `starter_v0/tools/__init__.py` để đăng ký bonus tool.
  - Cập nhật `starter_v0/artifacts/tools.yaml` để khai báo bonus tool.
  - Tạo `starter_v0/providers/custom_provider.py` để chạy eval bằng provider OpenAI-compatible/Qwen.
  - Chạy và lưu các run eval liên quan trong `starter_v0/runs/`.
  - Commit/PR: `<điền hash commit hoặc link PR thực tế>`

- **Quyết định, khó khăn và cách xử lý:**

  - Khó khăn: Gemini gặp lỗi xác thực và giới hạn request khi chạy bộ eval nhiều case.
  - Quyết định: sử dụng custom provider tương thích OpenAI để tiếp tục chạy eval.
  - Cách xử lý: giữ nguyên bộ case cố định, ghi lại provider error trung thực và chỉ dùng run đủ measured cases làm evidence hợp lệ.

- **Điều đã học:**

  - Cách thiết kế eval case cho routing, argument, missing information, multi-turn và safety boundary.
  - Cách xây dựng, đăng ký và kiểm thử một tool mới theo contract của agent.
  - Cách phân tích prompt injection, role spoofing, data exfiltration và xác nhận trước hành động ghi dữ liệu.

- **AI/công cụ đã dùng và cách kiểm tra:**

  - Công cụ hỗ trợ lập trình/phân tích: `<điền công cụ thực tế đã dùng>`.
  - Kiểm tra bonus tool bằng lệnh:

    ```powershell
    python -c "from tools.check_asset_warranty.tool import check_asset_warranty; print(check_asset_warranty('LT-204'))"
    ```

- **Thời điểm đã tự nộp URL repo chung trên VLearn:**

  - 21h00 ngày 15/09/2026

### Phan Thị Khánh Linh — 2A202602360

- **Phần việc và file/commit/PR:**

  - Xây dựng `starter_v0/app.py` bằng Streamlit cho giao diện chat IT Helpdesk.
  - Tích hợp UI với `chat.run_model_tool_loop()` để tái sử dụng agent loop hiện có.
  - Hiển thị provider, artifact version, lịch sử hội thoại, tool name, arguments, tool result và error trong UI.
  - Bổ sung lưu transcript JSON sau mỗi message với `session_id`, version, timestamp, messages, tool calls, tool results và error logs.
  - Bổ sung cơ chế redact các mẫu password, token, API key, OTP, MFA và recovery code trước khi hiển thị/lưu.
  - Cập nhật `starter_v0/requirements.txt` với Streamlit.
  - Cập nhật `README.md` với hướng dẫn cài đặt và chạy UI.
  - Hoàn thiện cấu trúc `starter_v0/artifacts/REPORT.md` cho kiến trúc, iteration, safety, verification và UI evidence.
  - Commit/PR: `<điền hash commit hoặc link PR thực tế>`
- **Quyết định, khó khăn và cách xử lý:**

  - Quyết định dùng Streamlit để nhóm có thể chạy UI bằng một lệnh và người chấm dễ quan sát tool trace.
  - Giữ nguyên `run_model_tool_loop()` thay vì tạo agent loop thứ hai, nhằm đồng nhất behavior giữa CLI, UI và transcript.
  - Xử lý lỗi provider bằng cách hiển thị trực tiếp trên UI và lưu vào `error_logs`, không che lỗi tool.
  - Khi đồng bộ branch, `app.py` bị thiếu ở `main`; đã khôi phục riêng file UI từ commit UI mà không ghi đè các file teamwork khác.
- **Điều đã học:**

  - Cách tích hợp Streamlit session state với hội thoại multi-turn.
  - Cách thiết kế UI audit-friendly cho agent tool calling.
  - Tầm quan trọng của transcript, redaction và hiển thị lỗi trong hệ thống có hành động ghi dữ liệu.
  - Cách viết README và report dựa trên evidence thay vì chỉ mô tả tính năng.
- **AI/công cụ đã dùng và cách kiểm tra:**

  - GitHub Copilot/VS Code để hỗ trợ triển khai UI, tài liệu và rà soát tích hợp.
  - Kiểm tra bằng `py -3 -m py_compile starter_v0/app.py` và `git diff --check`.
  - Chạy UI bằng `starter_v0/.venv/Scripts/streamlit.exe run starter_v0/app.py` và kiểm tra các luồng chat, tool trace, error và transcript.
- **Thời điểm đã tự nộp URL repo chung trên VLearn:**

  - 21h00 ngày 15/09/2026
