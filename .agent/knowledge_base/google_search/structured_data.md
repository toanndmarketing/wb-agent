---
title: Intro to Structured Data (Dữ liệu cấu trúc Schema)
source: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data?hl=vi
last_updated: Wed, 15 Jul 2026 20:42:08 GMT
---

# 📖 Intro to Structured Data (Dữ liệu cấu trúc Schema)

> [!NOTE]
> Tài liệu chắt lọc tinh khiết từ tài liệu chính thống của Google Search Central. 
> Phục vụ làm kim chỉ nam tối ưu SEO & lập chỉ mục cho AI Agent.

# Giới thiệu về mã đánh dấu dữ liệu có cấu trúc trên Google Tìm kiếmGoogle Tìm kiếm luôn nỗ lực để hiểu được nội dung của một trang. Bạn có thể giúp chúng tôi bằng cách cung cấp gợi ý rõ ràng về ý nghĩa của trang thông qua dữ liệu có cấu trúc trên trang. Dữ liệu có cấu trúc là một định dạng chuẩn để cung cấp thông tin về một trang và phân loại nội dung trang. Ví dụ: trên một trang về công thức nấu ăn sẽ có các loại dữ liệu về nguyên liệu, thời gian nấu và nhiệt độ, lượng calo, v.v.
## Tại sao nên thêm dữ liệu có cấu trúc vào trang?Việc thêm dữ liệu có cấu trúc có thể kích hoạt các kết quả tìm kiếm hấp dẫn người dùng hơn và có thể khuyến khích họ tương tác nhiều hơn với trang web của bạn, còn gọi là kết quả nhiều định dạng. Sau đây là một số nghiên cứu điển hình về các trang web đã triển khai dữ liệu có cấu trúc:
- Rotten Tomatoes đã thêm dữ liệu có cấu trúc vào 100.000 trang riêng biệt. Nhờ đó, tỷ lệ nhấp của các trang được bổ sung dữ liệu có cấu trúc tăng 25% so với các trang không có dữ liệu có cấu trúc.
- The Food Network đã triển khai các tính năng của kết quả tìm kiếm cho 80% số trang của họ và nhận thấy số lượt truy cập tăng 35%.
- Rakuten nhận thấy rằng người dùng dành thời gian trên các trang đã triển khai dữ liệu có cấu trúc nhiều hơn 1,5 lần so với các trang không thêm dữ liệu có cấu trúc. Ngoài ra, tỷ lệ tương tác cũng cao hơn 3,6 lần trên các trang AMP có các tính năng của kết quả tìm kiếm so với các trang AMP không có những tính năng này.
- Nestlé nhận thấy các trang hiển thị dưới dạng kết quả nhiều định dạng trên Google Tìm kiếm có tỷ lệ nhấp cao hơn 82% so với các trang không hiển thị dưới dạng kết quả nhiều định dạng.
## Cách thức hoạt động của dữ liệu có cấu trúc trên Google Tìm kiếmĐọc thêm nghiên cứu điển hình về những trang web đã triển khai dữ liệu có cấu trúc.Google sử dụng dữ liệu có cấu trúc tìm thấy trên web để hiểu nội dung của trang cũng như thu thập thông tin về web và thế giới nói chung, chẳng hạn như thông tin về con người, sách hoặc công ty có trong mã đánh dấu. Ví dụ: khi một trang công thức có dữ liệu có cấu trúc JSON-LD (mô tả tên, tác giả và các thông tin khác của công thức), thì Google Tìm kiếm có thể sử dụng thông tin đó để hiển thị kết quả nhiều định dạng cho công thức:Vì dữ liệu có cấu trúc gắn nhãn cho từng thành phần riêng trong công thức, người dùng có thể tìm kiếm công thức của bạn theo nguyên liệu, lượng calo, thời gian nấu, v.v.Nếu sử dụng một Hệ thống quản lý nội dung (CMS), chẳng hạn như Wix, WordPress hoặc Shopify, thì có thể bạn không trực tiếp chỉnh sửa được mã HTML của mình. Thay vào đó, có thể CMS của bạn đã có một trang về chế độ cài đặt cho công cụ tìm kiếm hoặc bạn có thể cài đặt một trình bổ trợ để chỉ định dữ liệu có cấu trúc. Hãy tìm hướng dẫn cách thêm dữ liệu có cấu trúc vào CMS của bạn (ví dụ: tìm theo từ khoá "dữ liệu có cấu trúc Wix" hoặc "trình bổ trợ dữ liệu có cấu trúc WordPress").Dữ liệu có cấu trúc được mã hoá bằng cách sử dụng thẻ đánh dấu trên trang chứa dữ liệu đó. Dữ liệu có cấu trúc trên trang mô tả nội dung của trang đó. Đừng tạo các trang trống chỉ để chứa dữ liệu có cấu trúc và cũng đừng thêm dữ liệu có cấu trúc về thông tin mà người dùng không nhìn thấy, ngay cả khi thông tin đó chính xác. Để biết thêm các nguyên tắc về kỹ thuật và chất lượng, hãy xem Nguyên tắc chung về dữ liệu có cấu trúc.Công cụ Kiểm tra kết quả nhiều định dạng là một công cụ dễ sử dụng và hữu ích để xác thực dữ liệu có cấu trúc của bạn và xem trước một tính năng của Google Tìm kiếm trong một số trường hợp. Hãy dùng thử:
## Từ điển và định dạng dữ liệu có cấu trúc<html> <head> <title>Non-Alcoholic Piña Colada</title> <script type="application/ld+json"> { "@context": "https://schema.org/", "@type": "Recipe", "name": "Non-Alcoholic Piña Colada", "image": [ "https://example.com/photos/1x1/photo.jpg", "https://example.com/photos/4x3/photo.jpg", "https://example.com/photos/16x9/photo.jpg" ], "author": { "@type": "Person", "name": "Mary Stone" }, "datePublished": "2024-03-10", "description": "This non-alcoholic pina colada is everyone's favorite!", "recipeCuisine": "American", "prepTime": "PT1M", "cookTime": "PT2M", "totalTime": "PT3M", "keywords": "non-alcoholic", "recipeYield": "4 servings", "recipeCategory": "Drink", "nutrition": { "@type": "NutritionInformation", "calories": "120 calories" }, "aggregateRating": { "@type": "AggregateRating", "ratingValue": 5, "ratingCount": 18 }, "recipeIngredient": [ "400ml of pineapple juice", "100ml cream of coconut", "ice" ], "recipeInstructions": [ { "@type": "HowToStep", "name": "Blend", "text": "Blend 400ml of pineapple juice and 100ml cream of coconut until smooth.", "url": "https://example.com/non-alcoholic-pina-colada#step1", "image": "https://example.com/photos/non-alcoholic-pina-colada/step1.jpg" }, { "@type": "HowToStep", "name": "Fill", "text": "Fill a glass with ice.", "url": "https://example.com/non-alcoholic-pina-colada#step2", "image": "https://example.com/photos/non-alcoholic-pina-colada/step2.jpg" }, { "@type": "HowToStep", "name": "Pour", "text": "Pour the pineapple juice and coconut mixture over ice.", "url": "https://example.com/non-alcoholic-pina-colada#step3", "image": "https://example.com/photos/non-alcoholic-pina-colada/step3.jpg" } ], "video": { "@type": "VideoObject", "name": "How to Make a Non-Alcoholic Piña Colada", "description": "This is how you make a non-alcoholic piña colada.", "thumbnailUrl": [ "https://example.com/photos/1x1/photo.jpg", "https://example.com/photos/4x3/photo.jpg", "https://example.com/photos/16x9/photo.jpg" ], "contentUrl": "https://www.example.com/video123.mp4", "embedUrl": "https://www.example.com/videoplayer?video=123", "uploadDate": "2024-02-05T08:00:00+08:00", "duration": "PT1M33S", "interactionStatistic": { "@type": "InteractionCounter", "interactionType": { "@type": "WatchAction" }, "userInteractionCount": 2347 }, "expires": "2024-02-05T08:00:00+08:00" } } </script> </head> <body> </body> </html>Tài liệu này mô tả các thuộc tính bắt buộc, nên dùng hoặc không bắt buộc đối với những dữ liệu có cấu trúc mang ý nghĩa đặc biệt đối với Google Tìm kiếm. Hầu hết dữ liệu có cấu trúc trên Tìm kiếm đều dùng mã có trên schema.org, nhưng bạn nên coi tài liệu tại Trung tâm Google Tìm kiếm là nguồn tham khảo chính thức về hành vi của Google Tìm kiếm thay vì dựa vào tài liệu của schema.org. Có nhiều thuộc tính và đối tượng trên schema.org mà Google Tìm kiếm không yêu cầu. Tuy nhiên, những thuộc tính hoặc đối tượng đó có thể hữu ích cho các công cụ tìm kiếm, dịch vụ, công cụ và nền tảng khác.Bạn phải cung cấp mọi thuộc tính bắt buộc để một đối tượng đủ điều kiện xuất hiện trong Google Tìm kiếm với giao diện nâng cao. Nói chung, việc xác định thêm các tính năng được đề xuất có thể khiến thông tin của bạn dễ xuất hiện hơn trong kết quả Tìm kiếm với giao diện nâng cao. Tuy nhiên, mức độ hoàn thiện và chính xác của các thuộc tính được đề xuất thì quan trọng hơn số lượng mà bạn cung cấp. Do đó, đừng cố gắng cung cấp mọi thuộc tính được đề xuất trong khi dữ liệu lại không đầy đủ, không hợp lệ hoặc không chính xác.
```html
sameAs
```
Ngoài các thuộc tính và đối tượng nêu ở đây, Google cũng có thể sử dụng thuộc tính và những dữ liệu có cấu trúc khác trên schema.org. Một số phần tử trong số này có thể được dùng để kích hoạt các tính năng của kết quả tìm kiếm trong tương lai nếu được đánh giá là hữu ích.
### Định dạng được hỗ trợGoogle Tìm kiếm hỗ trợ dữ liệu có cấu trúc ở những định dạng sau đây, trừ trường hợp có quy định khác. Nhìn chung, bạn nên dùng định dạng dễ nhất để triển khai và duy trì (trong hầu hết trường hợp, đó là JSON-LD); Google có thể sử dụng cả 3 định dạng trên, miễn là mã đánh dấu đó hợp lệ và được triển khai đúng cách theo tài liệu của tính năng tương ứng.
```html
<script>
```
```html
<head>
```
```html
<body>
```
```html
Country
```
```html
PostalAddress
```
```html
MusicVenue
```
```html
Event
```
```html
<body>
```
```html
<head>
```
```html
<head>
```
```html
<body>
```
## Nguyên tắc về dữ liệu có cấu trúcĐịnh dạng JSON-LD* (Nên dùng) Loại ký hiệu JavaScript được nhúng trong thẻ trong các phần tử và của một trang HTML. Thẻ đánh dấu này không nằm xen kẽ với văn bản mà người dùng nhìn thấy, điều này giúp việc xác định các mục dữ liệu lồng nhau dễ dàng hơn, chẳng hạn như mục trong trong của một . Ngoài ra, Google có thể đọc dữ liệu JSON-LD khi dữ liệu đó được chèn theo phương thức động vào nội dung của trang, chẳng hạn như qua mã JavaScript hoặc các tiện ích nhúng trong hệ thống quản lý nội dung của bạn. Vi dữ liệu Là đặc tả HTML cộng đồng mở được dùng để lồng dữ liệu có cấu trúc trong nội dung HTML. Giống như RDFa, Vi dữ liệu sử dụng các thuộc tính thẻ HTML để đặt tên cho các thuộc tính bạn muốn cung cấp dưới dạng dữ liệu có cấu trúc. Vi dữ liệu thường được dùng trong phần tử , nhưng cũng có thể được dùng trong phần tử . RDFa Một tiện ích HTML5 hỗ trợ dữ liệu được liên kết bằng cách sử dụng các thuộc tính thẻ HTML tương ứng với nội dung cho người dùng thấy mà bạn muốn mô tả cho các công cụ tìm kiếm. RDFa thường được sử dụng trong cả phần và của trang HTML. Nhìn chung, bạn nên sử dụng JSON-LD cho dữ liệu có cấu trúc nếu cách thiết lập của trang web cho phép, vì đây là giải pháp dễ nhất để chủ sở hữu trang web triển khai và duy trì trên quy mô lớn (nói cách khác là ít có khả năng người dùng gặp lỗi).Hãy làm theo nguyên tắc chung về dữ liệu có cấu trúc cũng như mọi nguyên tắc cụ thể cho loại dữ liệu có cấu trúc mà bạn dùng. Nếu không, dữ liệu có cấu trúc của bạn có thể không đủ điều kiện hiển thị dưới dạng kết quả nhiều định dạng trên Google Tìm kiếm.
## Làm quen với dữ liệu có cấu trúcNếu bạn mới làm quen với dữ liệu có cấu trúc, hãy tham khảo hướng dẫn của schema.org về dữ liệu có cấu trúc cho người mới bắt đầu. Hướng dẫn này chủ yếu tập trung vào Vi dữ liệu nhưng về cơ bản thì cũng phù hợp với JSON-LD và RDFa.Khi bạn đã thông thạo kiến thức cơ bản về dữ liệu có cấu trúc, hãy khám phá danh sách tính năng của dữ liệu có cấu trúc trên Google Tìm kiếm rồi chọn một tính năng để triển khai. Mỗi hướng dẫn sẽ đi sâu vào cách triển khai dữ liệu có cấu trúc sao cho trang web của bạn đủ điều kiện xuất hiện dưới dạng một kết quả nhiều định dạng trên Google Tìm kiếm.Chọn tính năng
## Đo lường tác động của dữ liệu có cấu trúcBạn nên so sánh hiệu suất của những trang có dữ liệu có cấu trúc với những trang không có dữ liệu có cấu trúc để quyết định xem bạn có nên dành công sức cho những dữ liệu đó hay không. Cách thực hiện tốt nhất là chạy quy trình kiểm tra trước và sau khi sử dụng trên một vài trang thuộc trang web của bạn. Điều này có thể hơi phức tạp, vì lượt xem một trang có thể thay đổi vì nhiều lý do khác nhau.
1. Chọn một số trang trên trang web hiện không sử dụng dữ liệu có cấu trúc và có một vài tháng dữ liệu trong Search Console. Đảm bảo chọn các trang không bị ảnh hưởng bởi thời gian trong năm hoặc tính kịp thời của nội dung. Hãy sử dụng các trang sẽ không thay đổi nhiều nhưng vẫn đủ phổ biến để người dùng đọc thường xuyên ở mức tạo ra được dữ liệu có ý nghĩa.
1. Thêm dữ liệu có cấu trúc hoặc tính năng khác vào các trang của bạn. Dùng
1. Ghi lại hiệu suất của một vài tháng trong
