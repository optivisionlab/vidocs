import qrcode
import uuid
from weasyprint import HTML
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
os.makedirs(ASSETS, exist_ok=True)

CORNER_CSS = """
@page {
    size: A4;
    margin: 2.2cm 2cm 2cm 2cm;
}
body {
    font-family: "DejaVu Sans", sans-serif;
    font-size: 12.5pt;
    line-height: 1.5;
    color: #111;
    position: relative;
}
/* reserved marker zone: content must never enter this box */
.corner-qr {
    position: fixed;
    top: 0.4cm;
    right: 0.4cm;
    width: 1.8cm;
    height: 1.8cm;
}
.corner-qr img { width: 100%; height: 100%; }
.corner-mark {
    position: fixed;
    width: 0.5cm;
    height: 0.5cm;
    background: #000;
}
.mark-tl { top: 0.4cm; left: 0.4cm; }
.mark-bl { bottom: 0.4cm; left: 0.4cm; }
.mark-br { bottom: 0.4cm; right: 0.4cm; }

h1 { font-size: 16pt; text-align: center; margin-bottom: 2pt; }
h2 { font-size: 13pt; margin-top: 14pt; }
.meta { text-align: center; font-style: italic; margin-bottom: 14pt; }
table { border-collapse: collapse; width: 100%; margin: 10pt 0; }
th, td { border: 1px solid #333; padding: 4pt 8pt; font-size: 11.5pt; }
th { background: #f0f0f0; }
.cols { display: flex; gap: 18pt; }
.col { flex: 1; }
.sig-block { margin-top: 26pt; display: flex; justify-content: space-between; }
.sig-block div { text-align: center; width: 40%; }
"""

def make_qr(uid, page, out_path):
    data = f"uid={uid};page={page}"
    qr = qrcode.QRCode(border=1, box_size=6)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out_path)
    return data

def wrap(body_html, qr_path):
    return f"""
    <html><head><meta charset="utf-8"><style>{CORNER_CSS}</style></head>
    <body>
      <div class="corner-qr"><img src="{qr_path}"></div>
      <div class="corner-mark mark-tl"></div>
      <div class="corner-mark mark-bl"></div>
      <div class="corner-mark mark-br"></div>
      {body_html}
    </body></html>
    """

# ---------- SAMPLE 1: single-column administrative form ----------
uid1 = str(uuid.uuid4())
qr1_path = os.path.join(ASSETS, "qr1.png")
qr1_data = make_qr(uid1, 1, qr1_path)

sample1_body = """
<h1>ĐƠN XIN NGHỈ PHÉP</h1>
<div class="meta">Số: 12/2026/ĐXNP</div>

<p>Kính gửi: <b>Ban Giám đốc Công ty TNHH Công nghệ Phương Nam</b></p>
<p>Tôi tên là: <b>Nguyễn Văn An</b></p>

<table>
  <tr><th>Bộ phận</th><td>Phòng Kỹ thuật</td></tr>
  <tr><th>Chức vụ</th><td>Kỹ sư phần mềm</td></tr>
  <tr><th>Số ngày nghỉ</th><td>03 ngày (từ 05/10/2026 đến 07/10/2026)</td></tr>
  <tr><th>Lý do</th><td>Giải quyết việc gia đình</td></tr>
</table>

<p>Tôi cam kết bàn giao đầy đủ công việc trước khi nghỉ và sẽ quay lại làm việc đúng thời hạn nêu trên. Kính mong Ban Giám đốc xem xét và chấp thuận.</p>

<h2>Xác nhận</h2>
<p>Người quản lý trực tiếp đã được thông báo và không có ý kiến phản đối về thời gian nghỉ nêu trên.</p>

<div class="sig-block">
  <div><i>Người quản lý</i><br><br><br>(Ký, ghi rõ họ tên)</div>
  <div><i>Người làm đơn</i><br><br><br>Nguyễn Văn An</div>
</div>
"""

sample1_md = """# ĐƠN XIN NGHỈ PHÉP

*Số: 12/2026/ĐXNP*

Kính gửi: **Ban Giám đốc Công ty TNHH Công nghệ Phương Nam**

Tôi tên là: **Nguyễn Văn An**

| Bộ phận | Phòng Kỹ thuật |
|---|---|
| Chức vụ | Kỹ sư phần mềm |
| Số ngày nghỉ | 03 ngày (từ 05/10/2026 đến 07/10/2026) |
| Lý do | Giải quyết việc gia đình |

Tôi cam kết bàn giao đầy đủ công việc trước khi nghỉ và sẽ quay lại làm việc đúng thời hạn nêu trên. Kính mong Ban Giám đốc xem xét và chấp thuận.

## Xác nhận

Người quản lý trực tiếp đã được thông báo và không có ý kiến phản đối về thời gian nghỉ nêu trên.

*Người quản lý*
(Ký, ghi rõ họ tên)

*Người làm đơn*
Nguyễn Văn An
"""

HTML(string=wrap(sample1_body, "file://" + qr1_path)).write_pdf(os.path.join(BASE, "sample1_leave_request.pdf"))
with open(os.path.join(BASE, "sample1_leave_request.md"), "w", encoding="utf-8") as f:
    f.write(sample1_md)

# ---------- SAMPLE 2: two-column report with table ----------
uid2 = str(uuid.uuid4())
qr2_path = os.path.join(ASSETS, "qr2.png")
qr2_data = make_qr(uid2, 1, qr2_path)

sample2_body = """
<h1>BÁO CÁO DOANH THU QUÝ III/2026</h1>
<div class="meta">Phòng Kinh doanh — Công ty CP Bán lẻ Việt Thành</div>

<div class="cols">
  <div class="col">
    <h2>Tổng quan</h2>
    <p>Trong quý III năm 2026, doanh thu toàn công ty đạt mức tăng trưởng ổn định so với quý trước, chủ yếu nhờ vào việc mở rộng kênh bán hàng trực tuyến và chương trình khuyến mãi tháng 8.</p>
    <p>Khu vực miền Nam tiếp tục dẫn đầu về doanh số, trong khi khu vực miền Trung ghi nhận mức tăng trưởng nhanh nhất theo tỷ lệ phần trăm.</p>
  </div>
  <div class="col">
    <h2>Kế hoạch quý IV</h2>
    <p>Công ty dự kiến triển khai thêm hai chi nhánh mới tại Đà Nẵng và Cần Thơ, đồng thời đẩy mạnh chiến dịch quảng cáo cho mùa mua sắm cuối năm.</p>
    <p>Bộ phận kỹ thuật sẽ nâng cấp hệ thống quản lý kho nhằm giảm thời gian xử lý đơn hàng trung bình.</p>
  </div>
</div>

<h2>Số liệu chi tiết theo khu vực</h2>
<table>
  <tr><th>Khu vực</th><th>Doanh thu (tỷ đồng)</th><th>So với quý trước</th></tr>
  <tr><td>Miền Bắc</td><td>18.4</td><td>+4.2%</td></tr>
  <tr><td>Miền Trung</td><td>9.7</td><td>+11.5%</td></tr>
  <tr><td>Miền Nam</td><td>26.1</td><td>+6.8%</td></tr>
</table>
"""

sample2_md = """# BÁO CÁO DOANH THU QUÝ III/2026

*Phòng Kinh doanh — Công ty CP Bán lẻ Việt Thành*

## Tổng quan

Trong quý III năm 2026, doanh thu toàn công ty đạt mức tăng trưởng ổn định so với quý trước, chủ yếu nhờ vào việc mở rộng kênh bán hàng trực tuyến và chương trình khuyến mãi tháng 8.

Khu vực miền Nam tiếp tục dẫn đầu về doanh số, trong khi khu vực miền Trung ghi nhận mức tăng trưởng nhanh nhất theo tỷ lệ phần trăm.

## Kế hoạch quý IV

Công ty dự kiến triển khai thêm hai chi nhánh mới tại Đà Nẵng và Cần Thơ, đồng thời đẩy mạnh chiến dịch quảng cáo cho mùa mua sắm cuối năm.

Bộ phận kỹ thuật sẽ nâng cấp hệ thống quản lý kho nhằm giảm thời gian xử lý đơn hàng trung bình.

## Số liệu chi tiết theo khu vực

| Khu vực | Doanh thu (tỷ đồng) | So với quý trước |
|---|---|---|
| Miền Bắc | 18.4 | +4.2% |
| Miền Trung | 9.7 | +11.5% |
| Miền Nam | 26.1 | +6.8% |
"""

HTML(string=wrap(sample2_body, "file://" + qr2_path)).write_pdf(os.path.join(BASE, "sample2_quarterly_report.pdf"))
with open(os.path.join(BASE, "sample2_quarterly_report.md"), "w", encoding="utf-8") as f:
    f.write(sample2_md)

print("Sample 1 UUID:", uid1, "| QR payload:", qr1_data)
print("Sample 2 UUID:", uid2, "| QR payload:", qr2_data)

import json
with open(os.path.join(BASE, "uid_map.json"), "w") as f:
    json.dump({uid1: "sample1_leave_request", uid2: "sample2_quarterly_report"}, f, indent=2)

print("Done.")
