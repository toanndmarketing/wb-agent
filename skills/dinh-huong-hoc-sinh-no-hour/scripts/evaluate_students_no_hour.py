# -*- coding: utf-8 -*-
"""
evaluate_students_no_hour.py
Skill: dinh-huong-hoc-sinh-no-hour
Đánh giá học sinh / trẻ em khi KHÔNG CÓ GIỜ SINH dựa trên Bát Tự Tam Trụ (Tiết Khí Dương Lịch) & Thần Số Học Pythagoras.
"""
import sys
import json
import argparse
import datetime
import subprocess
from pathlib import Path

CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']

CAN_ELEMENT = {
    'Giáp': ('Dương Mộc', 'Cây đại thụ, thẳng thắn, chính trực, tự lập cao, có chí tiến thủ, tố chất thủ lĩnh'),
    'Ất': ('Âm Mộc', 'Cỏ hoa mềm mại, khéo léo, linh hoạt, thích ứng giỏi, giàu tình cảm, chu đáo'),
    'Bính': ('Dương Hỏa', 'Mặt trời rực rỡ, nhiệt tình, nồng hậu, lạc quan, biểu đạt tốt, thích tỏa sáng'),
    'Đinh': ('Âm Hỏa', 'Ngọn đèn soi rọi, tinh tế, sâu sắc, cẩn trọng, ấm áp, nhạy cảm nghệ thuật'),
    'Mậu': ('Dương Thổ', 'Đất dày núi cao, điềm tĩnh, trung thực, giữ chữ tín, kiên định, đáng tin cậy'),
    'Kỷ': ('Âm Thổ', 'Đất vườn ươm, bao dung, cẩn thận, tỉ mỉ, biết chăm sóc người khác, vun vén khéo'),
    'Canh': ('Dương Kim', 'Kim loại đao kiếm, cương trực, dũng cảm, quyết đoán, tính kỷ luật cao, rõ ràng'),
    'Tân': ('Âm Kim', 'Vàng bạc ngọc quý, tinh tế, thẩm mỹ cao, tự trọng lớn, thích sự hoàn hảo, nhạy bén'),
    'Nhâm': ('Dương Thủy', 'Nước sông lớn đại dương, thông minh, phóng khoáng, tư duy linh hoạt, nhanh trí'),
    'Quý': ('Âm Thủy', 'Nước mưa sương sớm, trực giác nhạy bén, sâu sắc, trầm tĩnh, giàu trí tưởng tượng')
}

CAN_WEAKNESS = {
    'Giáp': 'Khá cứng đầu, cái tôi lớn, không thích bị áp đặt hay so sánh',
    'Ất': 'Dễ mềm lòng, thiếu kiên quyết trong một số tình huống đòi hỏi dứt khoát',
    'Bính': 'Tính nóng, làm việc theo cảm xúc nhất thời, dễ bốc đồng mau chán',
    'Đinh': 'Hay suy nghĩ nhiều, nội tâm nhạy cảm, dễ giấu nỗi buồn',
    'Mậu': 'Hơi cứng nhắc, chậm thay đổi thích nghi với môi trường mới',
    'Kỷ': 'Hay lo toan bao đồng, dễ bị ảnh hưởng bởi tâm trạng của bạn bè',
    'Canh': 'Thẳng tính quá mức, dễ gây tranh cãi với bạn bè',
    'Tân': 'Cầu toàn, tự tạo áp lực lớn cho bản thân, sợ thất bại',
    'Nhâm': 'Hiếu động, thích tự do, khó ngồi yên gò bó trong khuôn phép quá lâu',
    'Quý': 'Sống khép kín, nhạy cảm với lời phê bình, hay lo lắng ngầm'
}

NUMEROLOGY_TRAITS = {
    1: {
        "group": "👑 Thủ Lĩnh & Độc Lập",
        "strengths": "Tự lập sớm, quyết đoán, có chí tiến thủ, cá tính mạnh, thích dẫn đầu",
        "weaknesses": "Ương bướng, cái tôi cao, ít chịu nghe lời khi bị ép buộc, thiếu kiên nhẫn",
        "potential": "Cán sự lớp, đội trưởng, quản lý nhóm, tiên phong trong hoạt động mới",
        "advice": "Giao trách nhiệm cụ thể, khen ngợi đúng lúc, tôn trọng ý kiến thay vì áp đặt"
    },
    2: {
        "group": "🤝 Hòa Nhã & Cảm Xúc",
        "strengths": "Lắng nghe tốt, tình cảm, khéo léo, hợp tác nhóm tốt, nhạy cảm với người khác",
        "weaknesses": "Dễ tự ái, rụt rè, phụ thuộc cảm xúc, ngại đối đầu hoặc thể hiện trước đám đông",
        "potential": "Kết nối bạn bè, công tác xã hội, ngôn ngữ, hoạt động gắn kết tập thể",
        "advice": "Động viên tinh thần thường xuyên, tạo môi trường an toàn, khích lệ tự tin phát biểu"
    },
    3: {
        "group": "🎨 Sáng Tạo & Hoạt Ngôn",
        "strengths": "Hài hước, hoạt ngôn, giàu trí tưởng tượng, tiếp thu nhanh bằng hình ảnh & âm thanh",
        "weaknesses": "Dễ mất tập trung, nói nhiều trong giờ học, mau chán nếu bài học khô khan",
        "potential": "Nghệ thuật, MC/Thuyết trình, ngoại ngữ, văn học, vẽ, sân khấu",
        "advice": "Học qua trò chơi/kể chuyện, rèn tính kỷ luật hoàn thành bài tập đến cùng"
    },
    4: {
        "group": "📐 Kỷ Luật & Cần Mẫn",
        "strengths": "Cẩn thận, tỉ mỉ, có trách nhiệm, chấp hành nội quy tốt, nhớ số liệu và chi tiết giỏi",
        "weaknesses": "Bảo thủ, hơi cứng nhắc, ngại thay đổi, chậm thích nghi với cái mới",
        "potential": "Toán học, khoa học tự nhiên, thủ công, sắp xếp bài vở, theo dõi nề nếp",
        "advice": "Tạo thời gian biểu rõ ràng, khuyến khích bé cởi mở trải nghiệm cái mới"
    },
    5: {
        "group": "⚡ Năng Động & Khám Phá",
        "strengths": "Linh hoạt, thích khám phá, tò mò cao, phản xạ nhanh nhạy, giàu năng lượng",
        "weaknesses": "Hiếu động, hay mất trật tự, dễ 'cả thèm chóng chán', khó ngồi yên một chỗ",
        "potential": "Thể thao, khoa học thực nghiệm, khám phá thế giới, hoạt động ngoại khóa",
        "advice": "Cho tham gia vận động giải phóng năng lượng, chia nhỏ thời gian học để tránh chán"
    },
    6: {
        "group": "❤️ Quan Tâm & Trách Nhiệm",
        "strengths": "Biết chăm sóc bạn bè, chu đáo, có khiếu thẩm mỹ, sống tình cảm với thầy cô/gia đình",
        "weaknesses": "Hay lo lắng thái quá, dễ bị tổn thương tâm lý, gánh vác việc không phải của mình",
        "potential": "Phụ trách đời sống/nề nếp lớp, hội họa, thủ công mỹ thuật, bảo vệ động vật",
        "advice": "Dạy bé biết buông bỏ bớt lo lắng, ghi nhận sự chu đáo và khen ngợi sự đóng góp"
    },
    7: {
        "group": "🔍 Trí Tuệ & Quan Sát Sâu",
        "strengths": "Tư duy logic độc lập, thích tìm tòi bản chất 'tại sao', quan sát tinh tế, học sâu",
        "weaknesses": "Trầm tính, sống khép kín, ít chia sẻ tâm tư, dễ bị hiểu lầm là khó gần",
        "potential": "Nghiên cứu, lập trình/cờ vua, toán học lý thuyết, đọc sách bách khoa",
        "advice": "Tôn trọng không gian riêng, tạo câu hỏi gợi mở tư duy, khuyến khích giao lưu bạn bè"
    },
    8: {
        "group": "🏆 Thực Tế & Bản Lĩnh",
        "strengths": "Có đầu óc tổ chức, tư duy hiệu quả, bản lĩnh, thích chinh phục mục tiêu lớn",
        "weaknesses": "Hay ganh đua, thích kiểm soát, dễ cáu gắt khi không đạt kết quả mong muốn",
        "potential": "Chỉ huy lớp, điều phối dự án nhóm, tư duy logic số học & tài chính thực tế",
        "advice": "Dạy tính khiêm tốn, giúp bé hiểu giá trị của sự nỗ lực hơn là chỉ nhìn vào điểm số"
    },
    9: {
        "group": "🌟 Lý Tưởng & Bao Dung",
        "strengths": "Rộng lượng, nhân ái, có tinh thần vì tập thể, trực giác tốt, giàu lý tưởng",
        "weaknesses": "Mơ mộng, dễ phân tâm bởi cảm xúc người khác, hay ôm đồm việc",
        "potential": "Hoạt động đội nhóm, văn học nghệ thuật, bảo vệ môi trường, ngoại ngữ",
        "advice": "Giúp bé tập trung vào từng việc thực tế trước mắt, tránh kỳ vọng quá xa vời"
    },
    11: {
        "group": "✨ Trực Giác & Truyền Cảm Hứng (Master 11)",
        "strengths": "Nhạy bén đặc biệt, trực giác cao, khả năng truyền cảm hứng, suy nghĩ sâu sắc vượt tuổi",
        "weaknesses": "Hệ thần kinh nhạy cảm, dễ căng thẳng, hay suy nghĩ nhiều, dễ bị áp lực môi trường",
        "potential": "Năng khiếu nghệ thuật độc đáo, lãnh đạo tinh thần, tư duy sáng tạo đột phá",
        "advice": "Cần môi trường học tập bình yên, tránh quát mắng gay gắt, hướng dẫn giải tỏa cảm xúc"
    },
    22: {
        "group": "🏗️ Kiến Tạo & Đỉnh Cao Thực Thi (Master 22)",
        "strengths": "Tầm nhìn lớn kết hợp năng lực thực thi thực tế, kỷ luật thép, tư duy hệ thống xuất sắc",
        "weaknesses": "Tự tạo áp lực quá lớn cho bản thân, dễ stress nếu kết quả không hoàn hảo",
        "potential": "Tổ chức sự kiện lớp, quản lý đại dự án, kiến trúc/toán tư duy cấp cao",
        "advice": "Đồng hành từng bước, nhắc nhở cân bằng giữa học tập và vui chơi giải trí"
    },
    33: {
        "group": "💖 Đại Trách Nhiệm & Yêu Thương (Master 33)",
        "strengths": "Lòng trắc ẩn bao la, năng khiếu nghệ thuật & kết nối con người đỉnh cao",
        "weaknesses": "Dễ hy sinh quyền lợi bản thân, nhạy cảm quá mức trước nỗi buồn của người khác",
        "potential": "Sứ giả hòa bình của lớp, nghệ thuật đỉnh cao, truyền thông kết nối",
        "advice": "Dạy bé tự bảo vệ giới hạn bản thân, định hướng năng lượng vào sáng tạo nghệ thuật"
    }
}

def parse_dob(dob_str):
    # Support DD/MM/YYYY or YYYY-MM-DD
    if '/' in dob_str:
        parts = dob_str.split('/')
        return int(parts[0]), int(parts[1]), int(parts[2])
    elif '-' in dob_str:
        parts = dob_str.split('-')
        return int(parts[2]), int(parts[1]), int(parts[0])
    raise ValueError(f"Invalid date format: {dob_str}")

def calc_tam_tru(d_int, m_int, y_int):
    d_obj = datetime.date(y_int, m_int, d_int)
    
    # Julian Day Number
    a = (14 - m_int) // 12
    y = y_int + 4800 - a
    m = m_int + 12 * a - 3
    jd = d_int + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    
    can_day = CAN[(jd + 9) % 10]
    chi_day = CHI[(jd + 1) % 12]
    
    # Year Pillar (Cutoff at Feb 4)
    lap_xuan = datetime.date(y_int, 2, 4)
    bat_tu_year = y_int if d_obj >= lap_xuan else y_int - 1
    year_can_idx = (bat_tu_year - 4) % 10
    year_chi_idx = (bat_tu_year - 4) % 12
    can_year = CAN[year_can_idx]
    chi_year = CHI[year_chi_idx]
    
    # Month Pillar
    solar_months = [
        (datetime.date(y_int, 1, 5), 'Sửu', 11),
        (datetime.date(y_int, 2, 4), 'Dần', 0),
        (datetime.date(y_int, 3, 6), 'Mão', 1),
        (datetime.date(y_int, 4, 5), 'Thìn', 2),
        (datetime.date(y_int, 5, 6), 'Tỵ', 3),
        (datetime.date(y_int, 6, 6), 'Ngọ', 4),
        (datetime.date(y_int, 7, 7), 'Mùi', 5),
        (datetime.date(y_int, 8, 8), 'Thân', 6),
        (datetime.date(y_int, 9, 8), 'Dậu', 7),
        (datetime.date(y_int, 10, 8), 'Tuất', 8),
        (datetime.date(y_int, 11, 7), 'Hợi', 9),
        (datetime.date(y_int, 12, 7), 'Tý', 10),
    ]
    
    month_chi = 'Sửu'
    month_offset = 11
    for cutoff, chi, offset in reversed(solar_months):
        if d_obj >= cutoff:
            month_chi = chi
            month_offset = offset
            break
            
    start_can_map = {0: 2, 5: 2, 1: 4, 6: 4, 2: 6, 7: 6, 3: 8, 8: 8, 4: 0, 9: 0}
    first_month_can = start_can_map[year_can_idx]
    can_month = CAN[(first_month_can + month_offset) % 10]
    
    elem_name, elem_strength = CAN_ELEMENT[can_day]
    weakness = CAN_WEAKNESS[can_day]
    
    return {
        "year_pillar": f"{can_year} {chi_year}",
        "month_pillar": f"{can_month} {month_chi}",
        "day_pillar": f"{can_day} {chi_day}",
        "day_master": can_day,
        "element": elem_name,
        "battu_strength": elem_strength,
        "battu_weakness": weakness
    }

def calc_numerology(d_int, m_int, y_int):
    def sum_digits(n):
        return sum(int(c) for c in str(n))
        
    def reduce_master(n):
        while n > 9:
            if n in [11, 22, 33]:
                return n
            n = sum_digits(n)
        return n
        
    rd = reduce_master(d_int)
    rm = reduce_master(m_int)
    ry = reduce_master(y_int)
    
    lp = reduce_master(rd + rm + ry)
    info = NUMEROLOGY_TRAITS.get(lp, NUMEROLOGY_TRAITS[1])
    return {
        "life_path": lp,
        "group": info["group"],
        "lp_strengths": info["strengths"],
        "lp_weaknesses": info["weaknesses"],
        "potential": info["potential"],
        "advice": info["advice"]
    }

def evaluate_single(name, dob_str, gender="Nam", dad="", mom="", phone=""):
    d_int, m_int, y_int = parse_dob(dob_str)
    bt = calc_tam_tru(d_int, m_int, y_int)
    num = calc_numerology(d_int, m_int, y_int)
    
    formatted_dob = f"{d_int:02d}/{m_int:02d}/{y_int}"
    return {
        "name": name,
        "dob": formatted_dob,
        "gender": gender,
        "dad": dad,
        "mom": mom,
        "phone": phone,
        **bt,
        **num
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Evaluate students without birth hour (Bát Tự Tam Trụ + Thần Số Học)")
    parser.add_argument('--name', type=str, help="Student name")
    parser.add_argument('--dob', type=str, help="Date of birth (DD/MM/YYYY)")
    parser.add_argument('--gender', type=str, default="Nam", help="Gender (Nam/Nữ)")
    parser.add_argument('--input', type=str, help="Input JSON file with student array")
    parser.add_argument('--output', type=str, help="Output JSON file")
    
    args = parser.parse_args()
    
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            students = json.load(f)
        results = []
        for idx, s in enumerate(students, 1):
            res = evaluate_single(
                s.get("name", f"Học sinh {idx}"),
                s.get("dob", "01/01/2019"),
                s.get("gender", "Nam"),
                s.get("dad", ""),
                s.get("mom", ""),
                s.get("phone", "")
            )
            res["stt"] = s.get("stt", idx)
            results.append(res)
            
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"Exported {len(results)} evaluated students to {args.output}")
        else:
            print(json.dumps(results, ensure_ascii=False, indent=2))
            
    elif args.name and args.dob:
        res = evaluate_single(args.name, args.dob, args.gender)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        parser.print_help()
