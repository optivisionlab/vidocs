# Khảo sát các bộ dữ liệu OCR / Document Parsing liên quan

**Bối cảnh:** Khảo sát này phục vụ việc định vị bộ dữ liệu OCR tiếng Việt (large-scale, cấu trúc đa dạng, PDF → markdown, nhãn sinh tự động từ nguồn generate, sau đó in + scan để có ảnh thật) dự kiến nộp tại ICDAR2027.

---

## Nhóm 1 — Tiền lệ về phương pháp (nhãn sinh tự động, không gán tay)

Đây là các dự án gần nhất về **cách lấy nhãn**: nhãn được suy ra trực tiếp từ nguồn sinh ra tài liệu (LaTeX, XML...) thay vì con người gán tay hoặc OCR engine pre-label.

| Dataset | Ngôn ngữ | Quy mô | Nguồn ảnh | Cách sinh nhãn | Paper | Dataset / Code |
|---|---|---|---|---|---|---|
| **DocBank** | Anh | 500.000 trang | PDF digital-born, biên dịch từ LaTeX trên arXiv | Weak supervision: nhãn layout cấp token suy ra tự động từ mã nguồn LaTeX | https://arxiv.org/abs/2006.01038 | https://github.com/doc-analysis/DocBank |
| **Nougat (Meta AI)** | Anh (học thuật) | ~8,2 triệu trang (7.511.745 arXiv + 536.319 PMC + 446.777 IDL) | PDF digital-born (không scan) | Chuyển LaTeX/XML nguồn → markdown, ghép với trang PDF render tương ứng | https://arxiv.org/abs/2308.13418 | https://github.com/facebookresearch/nougat (mã nguồn công khai; bộ dữ liệu đầy đủ không phân phối lại do bản quyền arXiv/PMC) |

**Điểm mấu chốt:** DocBank có nhãn tự động + quy mô lớn nhưng không có markdown toàn văn (chỉ layout). Nougat có markdown toàn văn + quy mô rất lớn nhưng chỉ train trên PDF sạch — nhóm tác giả tự ghi nhận hiệu năng giảm rõ rệt khi áp dụng lên ảnh sách cũ đã scan thật.

---

## Nhóm 2 — Benchmark document-parsing / layout quốc tế

Đây là các benchmark định hình **loại task và cách đánh giá** (layout analysis, KIE, document-parsing toàn trang).

| Dataset | Ngôn ngữ | Quy mô | Loại nhãn / Task | Paper | Dataset / Code |
|---|---|---|---|---|---|
| **OmniDocBench** | Anh/Trung + đa dạng khác | 1.651 trang (1.355 trang bộ base + 3 tập "hard") | Markdown + bbox layout (15 block-level, 4 span-level) + reading order; đánh giá bằng Edit distance, BLEU, METEOR, TEDS | https://arxiv.org/abs/2412.07626 | https://github.com/opendatalab/OmniDocBench |
| **DocLayNet** | Chủ yếu Anh (95%) | 80.863 trang | Bbox layout 11 lớp, gán tay bởi chuyên gia | https://arxiv.org/abs/2206.01062 | https://github.com/DS4SD/DocLayNet |
| **PubLayNet** | Anh | >360.000 trang | Bbox layout 5 lớp (tự động khớp XML PubMed Central) | https://arxiv.org/abs/1908.07836 | https://github.com/ibm-aur-nlp/PubLayNet |
| **RVL-CDIP** | Anh | 400.000 ảnh (320K/40K/40K) | Phân loại 16 lớp tài liệu (không OCR) | (Harley et al., 2015) | https://huggingface.co/datasets/aharley/rvl_cdip |
| **FUNSD** | Anh | 199 tài liệu (149/50) | KIE 4 loại thực thể (question/answer/header/other), form scan noisy | https://arxiv.org/abs/1905.13538 | — |
| **CORD** | Indonesia | 1.000 hóa đơn (800/100/100) | KIE 30 loại thực thể, receipt | (Park et al., 2019, NeurIPS WS) | https://github.com/clovaai/cord |
| **SROIE** | Anh | 973 hóa đơn (626/347) | KIE 4 trường (company/date/address/total) | ICDAR2019 competition | https://rrc.cvc.uab.es/?ch=13 |
| **XFUND** | Đa ngôn ngữ (7 thứ tiếng) | 1.393 form (199/ngôn ngữ) | KIE đa ngôn ngữ, cùng schema FUNSD | (Xu et al., 2021) | https://github.com/doc-analysis/XFUND |

**Điểm mấu chốt:** OmniDocBench là tiền lệ gần nhất về *mục tiêu task* (ảnh trang → markdown, đa dạng thể loại) nhưng không có bản tiếng Việt và là tập **eval** (không phải tập train quy mô lớn). Các bộ còn lại quy mô nhỏ hoặc chỉ layout/KIE, không phải document-parsing toàn văn.

---

## Nhóm 3 — Bộ dữ liệu tiếng Việt hiện có

| Dataset | Quy mô | Nội dung / Nguồn ảnh | Loại nhãn | Paper | Dataset |
|---|---|---|---|---|---|
| **UIT-DODV** | Không rõ số trang cụ thể (cần xem paper gốc) | Bài báo khoa học tiếng Việt; ảnh gồm PDF gốc + chụp bằng smartphone + scan bằng máy quét vật lý | Page object detection (bbox vùng: text/hình/bảng...) | https://doi.org/10.1007/978-3-030-89128-2_37 | https://uit-together.github.io/datasets/ |
| **Viet-Doc-VQA / Viet-Doc-VQA-II** (từ Vintern-1B) | >116.000 trang | Sách giáo khoa Việt Nam lớp 1–12, nhiều môn học | VQA (câu hỏi – trả lời), không phải transcription toàn trang | https://arxiv.org/abs/2408.12480 | Chưa xác nhận công khai độc lập (thuộc hệ sinh thái Vintern) |
| **MC-OCR 2021** | 2.436 hóa đơn | Hóa đơn tiếng Việt chụp bằng điện thoại (nhăn, mờ, ánh sáng phức tạp) | 2 task: đánh giá chất lượng ảnh (IQA) + KIE 4 trường | https://people.cs.umu.se/sonvx/files/MCOCR_Preprint.pdf | https://competitions.codalab.org/competitions/27798 |
| **VNOnDB (HANDS-VNOnDB)** | 1.146 đoạn văn viết tay | Chữ viết tay tiếng Việt trực tuyến (online handwriting) | Transcription cấp dòng/nét/ký tự | — | — |
| **UIT-HWDB** | Không xác định trong tóm tắt truy cập được | Ảnh chữ viết tay tổng hợp | Transcription, unconstrained handwriting recognition | — | — |
| **ViOCRVQA** | 28.282 ảnh bìa sách, 123.781 cặp hỏi-đáp | Bìa sách tiếng Việt | VQA | — | — |
| **ViTextVQA** | >16.000 ảnh, >50.000 câu hỏi | Ảnh cảnh thường có chữ (scene text) | VQA | https://arxiv.org/abs/2404.10652 | — |

**Nguồn tổng hợp/khảo sát nền:** *A Survey on Vietnamese Document Analysis and Recognition: Challenges and Future Directions* — https://arxiv.org/abs/2506.05061 (khảo sát này trực tiếp xác nhận sự khan hiếm dữ liệu quy mô lớn cho OCR tiếng Việt là một thách thức mở, và ghi nhận sinh dữ liệu tổng hợp là một hướng giải quyết đang được nghiên cứu).

---

## Phân tích khoảng trống & định vị đóng góp

### 1. Đánh đổi chưa được giải quyết giữa "quy mô" và "chất lượng nhãn"
- Gán tay (DocLayNet, FUNSD, CORD, UIT-DODV): chuẩn nhưng quy mô nhỏ.
- Auto-label quy mô lớn nhưng thiếu một trong hai: DocBank thiếu markdown toàn văn; Nougat có markdown nhưng chỉ train trên PDF sạch, tự thừa nhận giảm hiệu năng trên ảnh scan thật.
- **→ Đóng góp:** pipeline gen layout → PDF → markdown ground truth tự động → in + scan thật, đạt đồng thời cả ba: quy mô lớn, nhãn chính xác tuyệt đối, ảnh đầu vào là suy giảm thật (không phải PDF sạch, không phải nhiễu mô phỏng).

### 2. Các bộ tiếng Việt đều hẹp về loại tài liệu (domain)
UIT-DODV chỉ bài báo khoa học, Viet-Doc-VQA chỉ sách giáo khoa, MC-OCR chỉ hóa đơn, VNOnDB/UIT-HWDB chỉ viết tay, ViOCRVQA chỉ bìa sách. Chưa có bộ nào phủ nhiều thể loại tài liệu hành chính/doanh nghiệp/pháp lý trong cùng một schema thống nhất.
- **→ Đóng góp:** vì sinh từ template, mở rộng thể loại chỉ cần thêm template HTML mới, không bị giới hạn bởi việc phải sưu tầm đủ loại tài liệu thật.

### 3. Sai lệch loại task: phần lớn dữ liệu tiếng Việt là VQA, không phải page-to-markdown
ViOCRVQA, ViTextVQA, Viet-Doc-VQA đều dạng hỏi-đáp, không đánh giá khả năng parsing toàn trang như OmniDocBench làm cho tiếng Anh.
- **→ Đóng góp:** tái hiện đúng paradigm OmniDocBench (ảnh trang → markdown) nhưng cho tiếng Việt — khoảng trống task rõ ràng nhất để trình bày với reviewer.

### 4. Không bộ nào cho phép thí nghiệm có kiểm soát giữa bản sạch và bản suy giảm thật
Ngay cả OmniDocBench cũng chỉ là sưu tầm ảnh có sẵn, không có cặp "cùng nội dung — 1 bản digital sạch + 1 bản sau in/scan thật" để tách bạch khó khăn do ngôn ngữ/nội dung với khó khăn do nhiễu vật lý.
- **→ Đóng góp:** giữ lại cả bản PDF gốc lẫn bản đã scan của cùng nội dung → tạo được tập con "sim-to-real" độc quyền, hiện chưa dataset lớn nào công bố công khai theo cách này.

### 5. Nhiễu tiếng Việt có đặc thù riêng (dấu thanh) mà augmentation mô phỏng dễ bỏ sót
Dấu thanh tiếng Việt nhỏ và rất nhạy cảm với mờ, độ phân giải thấp, ánh sáng không đều và nén ảnh — đây là lỗi đặc trưng ngôn ngữ mà augmentation nhân tạo khó tái hiện đúng bản chất vật lý.
- **→ Đóng góp:** in + scan thật tạo nhiễu thật lên dấu thanh (từ mực in/máy scan), cho tín hiệu khó đúng bản chất hơn so với augmentation tổng hợp thuần túy.

### 6. Vấn đề bản quyền / PII
Nhiều dataset lớn (Nougat dùng arXiv, RVL-CDIP là tài liệu thuốc lá giải mật) phải xử lý cẩn thận về pháp lý khi công bố. Vì nội dung tự sinh (không crawl từ nguồn thật), bộ dữ liệu đề xuất gần như miễn nhiễm với vấn đề bản quyền/PII — điểm cộng cho khả năng công bố công khai (open-release) tại ICDAR.

---

## Kết luận

Chưa có bộ dữ liệu tiếng Việt nào kết hợp đồng thời: (1) nhiều loại tài liệu đa dạng ngoài textbook/receipt, (2) nhãn transcription toàn trang dạng markdown, (3) quy mô lớn (nhờ nhãn tự động), và (4) ảnh đầu vào là suy giảm thật qua in+scan (không chỉ digital-born, không chỉ gán tay tốn kém). Đây là luận điểm novelty chính cho phần Related Work / Contribution của bài nộp ICDAR2027.
