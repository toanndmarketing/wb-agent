---
title: Consolidate Duplicate URLs (Tối ưu hóa Canonical)
source: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls?hl=vi
last_updated: Wed, 15 Jul 2026 20:42:06 GMT
---

# 📖 Consolidate Duplicate URLs (Tối ưu hóa Canonical)

> [!NOTE]
> Tài liệu chắt lọc tinh khiết từ tài liệu chính thống của Google Search Central. 
> Phục vụ làm kim chỉ nam tối ưu SEO & lập chỉ mục cho AI Agent.

# Cách chỉ định URL chính tắc bằng rel="canonical" và các phương thức khácBạn có thể dùng một số phương thức để cho Google Tìm kiếm biết lựa chọn ưu tiên của mình về việc chỉ định một URL chính tắc cho các trang trùng lặp hoặc rất giống nhau. Các phương thức này được sắp xếp theo mức độ ảnh hưởng đến quy trình chuẩn hoá:
- 
- 
```html
link
```
```html
rel="canonical"
```
- Lệnh chuyển hướng: Một tín hiệu mạnh cho thấy mục tiêu của lệnh chuyển hướng sẽ trở thành trang chính tắc. Chú thích : Một tín hiệu mạnh cho thấy URL được chỉ định sẽ trở thành URL chính tắc. Đưa vào sơ đồ trang web: Một tín hiệu yếu giúp cho URL có trong sơ đồ trang web sẽ trở thành trang chính tắc. Xin lưu ý rằng bạn có thể sử dụng nhiều phương thức cùng lúc và kết hợp các phương thức đó để đạt được hiệu quả cao hơn. Tức là việc bạn sử dụng từ hai phương thức trở lên sẽ làm tăng khả năng URL chính tắc mà bạn ưu tiên được xuất hiện trong kết quả tìm kiếm.Tuy bạn nên dùng những phương thức này, nhưng không phương thức nào là bắt buộc. Trang web của bạn vẫn có thể hoạt động tốt mà không cần chỉ định URL ưu tiên làm URL chính tắc. Đó là vì nếu bạn không chỉ định URL chính tắc, Google sẽ xác định phiên bản URL phù hợp nhất một cách khách quan để cho người dùng thấy trên Tìm kiếm.
```html
<head>
```
## Lý do nên chỉ định một URL chính tắcNếu sử dụng Hệ thống quản lý nội dung (CMS), chẳng hạn như WordPress, Wix, hoặc Blogger, thì có thể bạn không trực tiếp chỉnh sửa được mã HTML của mình. Thay vào đó, có thể CMS của bạn có một trang cài đặt cho công cụ tìm kiếm hoặc có một cơ chế khác để giúp công cụ tìm kiếm biết được URL chính tắc. Hãy tìm hướng dẫn về cách sửa đổi cho trang của bạn trên CMS đó (ví dụ: tìm kiếm "wordpress thiết lập phần tử chính tắc").Nhìn chung, không nhất thiết phải chỉ định một URL ưu tiên làm URL chính tắc. Tuy nhiên, bạn nên cho Google biết rõ ràng đâu là trang chính tắc trong một nhóm trang trùng lặp hoặc tương tự nhau, vì một số lý do sau:
- 
```html
https://www.example.com/dresses/green/green-dress.html
```
```html
https://example.com/dresses/cocktail?gclid=ABCD
```
- 
```html
https://example.com/dresses/cocktail?gclid=ABCD
```
```html
https://www.example.com/dresses/green/green-dress.html
```
- 
- 
## Các phương pháp hay nhấtĐể chỉ định URL mà bạn muốn mọi người nhìn thấy trong kết quả tìm kiếm. Bạn muốn mọi người truy cập trang sản phẩm bán váy màu xanh lục thông qua thay vì . Để hợp nhất tín hiệu của các trang tương tự hoặc trùng lặp. Việc này giúp các công cụ tìm kiếm hợp nhất tín hiệu thu thập được qua các URL đơn lẻ (chẳng hạn như các đường liên kết đến những URL đó) thành duy nhất một URL được ưu tiên. Tức là các tín hiệu từ các trang web khác đến sẽ được hợp nhất với các đường liên kết đến nếu trang đó trở thành trang chính tắc. Để đơn giản hoá việc theo dõi chỉ số cho một nội dung. Nếu bạn có nhiều URL, việc hợp nhất các chỉ số cho một nội dung cụ thể sẽ trở nên khó khăn hơn. Để tránh tốn thời gian thu thập dữ liệu trên các trang trùng lặp. Để có thể khai thác tối đa Googlebot cho trang web của mình, bạn nên để Googlebot dành thời gian thu thập dữ liệu các trang mới (hoặc vừa cập nhật) trên trang web của mình thay vì thu thập dữ liệu các phiên bản trùng lặp của cùng một nội dung.Đối với tất cả phương pháp chuẩn hoá, hãy làm theo các phương pháp hay nhất sau:
- 
- 
- 
```html
rel="canonical"
```
- 
- 
```html
rel="canonical"
```
- 
```html
noindex
```
```html
link
```
```html
rel="canonical"
```
- Nếu bạn đang dùng
```html
hreflang
```
- Liên kết đến URL chính tắc thay vì đến URL trùng lặp khi liên kết bên trong trang web của bạn.
    Việc duy trì liên kết với URL mà bạn chọn là URL chính tắc sẽ giúp Google
- Nếu đang sử dụng tính năng kết xuất phía máy khách bằng JavaScript, bạn cần đảm bảo rằng
    thông tin về URL chính tắc phải rõ ràng nhất có thể. Cách tốt nhất để thực hiện việc này là
## So sánh các phương thức chuẩn hoáKhông dùng tệp robots.txt để chỉ định phiên bản chính tắc. Google vẫn có thể lập chỉ mục các URL bị chặn trong robots.txt mà không cần nội dung của các URL đó. Không dùng công cụ xoá URL để chỉ định trang chính tắc. Công cụ này sẽ ẩn tất cả phiên bản của một URL khỏi kết quả Tìm kiếm. Không chỉ định nhiều URL làm URL chính tắc cho cùng một trang bằng cách dùng nhiều kỹ thuật chuẩn hoá (ví dụ: đừng chỉ định một URL trong sơ đồ trang web nhưng lại dùng để chỉ định một URL khác cho chính trang đó). Không chỉ định một phân mảnh của URL làm URL chính tắc, vì Google thường không hỗ trợ các phân mảnh của URL. Hãy thêm một đường liên kết trên chính trang chính tắc (còn gọi là trang chính tắc tự tham chiếu). Bạn không nên sử dụng để ngăn việc lựa chọn trang chính tắc trong một trang web, vì việc này sẽ hoàn toàn khiến trang đó bị chặn khỏi Tìm kiếm. Mã chú thích là giải pháp ưu tiên. các phần tử , hãy nhớ chỉ định trang chính tắc bằng cùng ngôn ngữ, hoặc ngôn ngữ thay thế phù hợp nhất có thể nếu không có trang chính tắc cho ngôn ngữ đó.Bảng sau đây so sánh các phương thức chuẩn hoá, nêu bật ưu và nhược điểm của từng phương thức trong việc duy trì, cũng như mức độ hiệu quả trong nhiều tình huống.
```html
rel="canonical" link
```
```html
<link>
```
Phương thức và nội dung mô tả Phần tử Thêm một phần tử vào mã lập trình của mọi trang trùng lặp để trỏ đến trang chính tắc.
- Có thể ánh xạ vô số trang trùng lặp.
- Đối với các trang web lớn hoặc thường xuyên thay đổi URL, việc duy trì hệ thống ánh xạ có thể sẽ phức tạp.
- Chỉ áp dụng cho các trang HTML chứ không áp dụng cho tệp (chẳng hạn như PDF). Trong những trường hợp như vậy, bạn có thể dùng tiêu đề HTTP
```html
rel="canonical"
```
```html
rel="canonical"
```
```html
rel="canonical"
```
- Không làm tăng kích thước trang.
- Có thể ánh xạ vô số trang trùng lặp.
- Đối với các trang web lớn hoặc thường xuyên thay đổi URL, việc duy trì hệ thống ánh xạ có thể sẽ phức tạp.Ưu điểm: Nhược điểm: Sơ đồ trang web Chỉ định trang chính tắc của bạn trong sơ đồ trang web.Ưu điểm:
- Triển khai và duy trì đơn giản, đặc biệt là trên các trang web lớn.Nhược điểm:
- Google vẫn phải xác định các phiên bản trùng lặp của mọi trang chính tắc mà bạn khai báo trong sơ đồ trang web.
- Tín hiệu gửi tới Googlebot sẽ không mạnh bằng kỹ thuật ánh xạ
```html
rel="canonical"
```
## Sử dụng chú thích
```html
link
```
```html
rel="canonical"
```
. Lệnh chuyển hướng Dùng lệnh chuyển hướng vĩnh viễn để cho Google biết rằng URL chuyển hướng là phiên bản kém hơn so với URL mà URL đó chuyển hướng đến. Chỉ sử dụng lệnh chuyển hướng này khi ngừng sử dụng một trang trùng lặp. Phiên bản AMP Nếu bạn có một phiên bản là trang AMP, hãy làm theo nguyên tắc dành cho AMP để chỉ định trang chính tắc và phiên bản AMP.
```html
rel
```
```html
link
```
```html
rel="canonical"
```
```html
rel="canonical"
```
```html
hreflang
```
```html
lang
```
```html
media
```
```html
type
```
```html
link
```
```html
link
```
```html
rel="alternate"
```
```html
hreflang
```
Google hỗ trợ các chú thích canonical tường minh theo mô tả trong RFC 6596. Các chú thích đề xuất các phiên bản thay thế của một trang sẽ bị bỏ qua; cụ thể thì các chú thích có thuộc tính , , và sẽ không được sử dụng cho quy trình chuẩn hoá. Thay vào đó, hãy sử dụng các chú thích thích hợp để chỉ định phiên bản thay thế của một trang; ví dụ: cho các chú thích về ngôn ngữ và quốc gia.
```html
link
```
```html
rel="canonical"
```
- 
```html
link
```
```html
rel="canonical"
```
- 
```html
rel="canonical"
```
```html
link
```
```html
link
```
```html
rel="canonical"
```
Phần tử trong HTML Tiêu đề HTTP Bạn nên chọn một trong những cách này. Tuy được hỗ trợ, nhưng việc sử dụng cả hai phương thức cùng lúc sẽ dễ xảy ra lỗi hơn (ví dụ: có thể bạn cung cấp một URL trong tiêu đề HTTP và một URL khác trong phần tử ).
### Phần tử
```html
link
```
```html
rel="canonical"
```
```html
link
```
```html
rel="canonical"
```
```html
head
```
Phần tử (còn gọi là phần tử chính tắc) là một phần tử dùng trong phần của đoạn mã HTML để cho biết rằng một trang khác đang đại diện cho nội dung trên trang.
```html
https://example.com/dresses/green-dresses
```
1. Thêm phần tử
```html
<link>
```
```html
rel="canonical"
```
```html
<head>
```
```html
<html>
<head>
<title>Explore the world of dresses</title>
<link rel="canonical" href="https://example.com/dresses/green-dresses" />
<!-- other elements -->
</head>
<!-- rest of the HTML -->
```
```html
rel="canonical"
```
1. Nếu trang chính tắc có biến thể dành cho thiết bị di động trên một URL riêng, hãy thêm phần tử
```html
link
```
```html
rel="alternate"
```
Bạn cũng nên thêm chính yếu tố liên kết tự tham chiếu này vào trang chính tắc. vào đó, trỏ đến phiên bản trang dành cho thiết bị di động:
```html
<html>
<head>
<title>Explore the world of dresses</title>
<link rel="alternate" media="only screen and (max-width: 640px)"  href="https://m.example.com/dresses/green-dresses">
<link rel="canonical" href="https://example.com/dresses/green-dresses" />
<!-- other elements -->
</head>
<!-- rest of the HTML -->
```
1. Thêm
```html
hreflang
```
```html
link
```
```html
rel="canonical"
```
hoặc phần tử bất kỳ nào khác phù hợp với trang. Đối với phần tử , hãy dùng đường dẫn tuyệt đối thay vì đường dẫn tương đối. Tuy Google có hỗ trợ đường dẫn tương đối, nhưng bạn không nên sử dụng các đường dẫn này, vì về lâu dài, các đường dẫn này có thể gây ra vấn đề (ví dụ: nếu bạn vô tình cho phép chúng tôi thu thập dữ liệu trên trang web thử nghiệm của bạn).
```html
https://www.example.com/dresses/green/green-dress.html
```
```html
/dresses/green/green-dress.html
```
```html
link element
```
```html
rel="canonical"
```
```html
<head>
```
```html
<head>
```
```html
link
```
```html
rel="canonical"
```
### Tiêu đề HTTP
```html
rel="canonical"
```
```html
link
```
```html
rel="canonical"
```
Nếu có thể thay đổi cấu hình của máy chủ, bạn có thể sử dụng tiêu đề HTTP có thuộc tính mục tiêu theo định nghĩa trong RFC5988 thay vì phần tử HTML để chỉ định URL chính tắc cho một tài liệu được Tìm kiếm hỗ trợ, bao gồm cả tài liệu không phải HTML như tệp PDF.Google chỉ hỗ trợ phương thức này cho các kết quả tìm kiếm trang web.
```html
rel="canonical"
```
```html
.docx
```
```html
.docx
```
Nếu xuất bản nội dung ở nhiều định dạng tệp (ví dụ: PDF hoặc Microsoft Word), mỗi định dạng trên một URL riêng, bạn có thể trả về tiêu đề HTTP để cho Googlebot biết đâu là URL chính tắc đối với tệp không phải HTML. Ví dụ: Để cho biết rằng bản PDF của tài liệu mới là phiên bản chuẩn hoá, bạn có thể thêm tiêu đề HTTP này cho phiên bản của nội dung:
```html
HTTP/1.1 200 OK
Content-Length: 19
...
Link: <https://www.example.com/downloads/white-paper.pdf>; rel="canonical"
...
```
```html
link
```
```html
rel="canonical"
```
```html
rel="canonical"
```
Tương tự như phần tử , hãy sử dụng URL tuyệt đối trong tiêu đề HTTP .
## Dùng sơ đồ trang webChọn một URL chính tắc cho mỗi trang của bạn rồi gửi những URL đó trong một sơ đồ trang web. Tất cả trang có trong sơ đồ trang web đều được đề xuất là trang chính tắc. Google sẽ quyết định trang nào (nếu có) là trang trùng lặp, dựa trên mức độ giống nhau của nội dung.Việc cung cấp URL chính tắc ưu tiên trong sơ đồ trang web là một cách đơn giản để xác định trang chính tắc cho một trang web lớn. Đồng thời, sơ đồ trang web cũng là một cách hữu ích để cho Google biết đâu là trang quan trọng nhất trên trang web của bạn.
## Sử dụng lệnh chuyển hướngHãy sử dụng phương thức này khi bạn muốn loại bỏ các trang trùng lặp hiện tại. Mọi phương thức chuyển hướng vĩnh viễn đều có cùng tác động đến Google Tìm kiếm. Tuy nhiên, cần lưu ý rằng thời gian để công cụ tìm kiếm nhận thấy còn tuỳ theo phương thức chuyển hướng.Để có tác động nhanh nhất, hãy sử dụng lệnh chuyển hướng HTTP (còn gọi là lệnh chuyển hướng phía máy chủ).Giả sử người dùng có thể truy cập trang của bạn qua nhiều URL:
- 
```html
https://example.com/home
```
- 
```html
https://home.example.com
```
- 
```html
https://www.example.com
```
Hãy chọn một trong những URL đó làm URL chính tắc và dùng lệnh chuyển hướng để chuyển lưu lượng truy cập từ những URL khác đến URL mà bạn ưu tiên.
## Các tín hiệu khác
```html
hreflang
```
Ngoài các phương thức được cung cấp rõ ràng, Google cũng sử dụng một nhóm tín hiệu chuẩn hoá thường dựa trên chế độ thiết lập trang web: ưu tiên HTTPS hơn HTTP, và URL trong các cụm .
### Ưu tiên HTTPS hơn HTTP để làm URL chính tắcKhi chọn trang chính tắc, Google ưu tiên các trang HTTPS hơn các trang HTTP, trừ trường hợp có vấn đề hoặc tín hiệu xung đột, chẳng hạn như sau:
- Trang HTTPS có một chứng chỉ SSL không hợp lệ.
- Trang HTTPS chứa yếu tố phụ thuộc không an toàn (ngoài hình ảnh).
- Trang HTTPS chuyển hướng người dùng đến hoặc qua một trang HTTP.
- Trang HTTPS có một
```html
link
```
```html
rel="canonical"
```
trỏ đến trang HTTP. Theo mặc định, hệ thống của chúng tôi ưu tiên trang HTTPS hơn trang HTTP. Tuy nhiên, bạn có thể đảm bảo chúng tôi sẽ chọn trang HTTPS bằng cách thực hiện một trong những thao tác sau:
- Thêm lệnh chuyển hướng từ trang HTTP đến trang HTTPS.
- Thêm
```html
link
```
```html
rel="canonical"
```
- Triển khaitừ trang HTTP sang trang HTTPS. HSTS (cơ chế Bảo mật truyền tải nghiêm ngặt HTTP). Để ngăn Google chọn nhầm trang HTTP làm trang chính tắc, hãy tránh những phương pháp sau đây:
- Tránh dùng chứng chỉ TLS/SSL không hợp lệ và tránh chuyển hướng HTTPS đến HTTP vì những việc này là tín hiệu rất mạnh khiến Google ưu tiên HTTP hơn. Việc triển khai HSTS cũng không thể ngăn sự ưu tiên này.
- Đừng đưa phiên bản HTTP của các trang vào sơ đồ trang web hay
```html
hreflang
```
- Tránh triển khai chứng chỉ SSL/TLS sang nhầm biến thể máy chủ. Ví dụ:
```html
example.com
```
```html
subdomain.example.com
```
### Ưu tiên URL trong các cụm
```html
hreflang
```
chú thích thay cho phiên bản HTTPS. phân phát chứng chỉ cho . Chứng chỉ này phải khớp với URL trang web hoàn chỉnh của bạn hoặc phải là chứng chỉ đại diện có thể dùng cho nhiều miền con trên một miền.
```html
hreflang
```
```html
https://example.com/de-de/cats
```
```html
https://example.com/de-ch/cats
```
```html
hreflang
```
```html
https://example.com/de-at/cats
```
```html
de-de
```
```html
de-ch
```
```html
/de-at/
```
```html
hreflang
```
Để hỗ trợ nỗ lực bản địa hoá của trang web, khi chuẩn hoá, Google ưu tiên những URL thuộc các cụm . Ví dụ: nếu và trỏ qua lại với nhau bằng chú thích , nhưng không trỏ đến , các trang cho và sẽ được ưu tiên chọn làm trang chính tắc thay vì trang (không xuất hiện trong cụm ).Đọc thêm về cách khắc phục sự cố và vấn đề về việc chuẩn hoá.
