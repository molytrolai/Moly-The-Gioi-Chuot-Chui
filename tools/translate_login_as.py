#!/usr/bin/env python3
"""Translate all Chinese strings in dump_login_as/scripts to Vietnamese."""

from pathlib import Path

TRANSLATIONS = {
    # LoginOnePage.as
    "你的密码太简单啦！英文+数字更加安全哦！": "Mật khẩu quá đơn giản! Hãy kết hợp chữ cái và chữ số để an toàn hơn nhé!",
    "密码错误！": "Mật khẩu không chính xác!",
    "验证码错误！": "Mã xác nhận không đúng!",
    "只有在自己家里上网才能选择，并要牢记帐号和密码哦！": "Chỉ chọn lưu thông tin trên máy tính cá nhân để đảm bảo an toàn tài khoản nhé!",
    "密码不能为空且要大于5位！": "Mật khẩu không được để trống và phải từ 6 ký tự trở lên!",
    "帐号错误。": "Tài khoản không chính xác hoặc không tồn tại.",

    # LoginSocket.as
    "线路繁忙，请耐心等待": "Đường truyền đang bận, vui lòng kiên nhẫn chờ trong giây lát...",
    "　　现在是关园时间！": "Hiện tại vương quốc đang trong thời gian nghỉ ngơi!",
    "\\r你的帐号将被封停三十天!": "\\nTài khoản của bạn bị tạm khóa 30 ngày!",
    "\\r你的帐号将被封停十四天!": "\\nTài khoản của bạn bị tạm khóa 14 ngày!",
    "\\r你的帐号将被封停七天": "\\nTài khoản của bạn bị tạm khóa 7 ngày!",
    "\\r协议不对": "\\nGiao thức kết nối không khớp!",
    "该账号未完成身份证实名认证或为未成年人账号受防沉迷限制，请前往account.61.com或kf.61.com查询！": "Tài khoản đang bị giới hạn giờ chơi hoặc cần xác thực cư dân.",
    "\\r帐号错误。": "\\nTài khoản không chính xác.",
    "\\r你输入的昵称不合法": "\\nBiệt danh bạn nhập không hợp lệ!",
    "你输入的密码错误次数太多\\r请稍候再试。": "Bạn đã nhập sai mật khẩu quá nhiều lần.\\nVui lòng thử lại sau ít phút nhé.",
    "你的帐号已经被永久封停 \\r将无法登陆摩尔庄园。": "Tài khoản của bạn đã bị khóa vĩnh viễn,\\nkhông thể đăng nhập Vương Quốc Moly.",
    "系统错误，账号受限或正处在封停状态中，暂时无法登陆摩尔庄园。": "Hệ thống: Tài khoản bị giới hạn hoặc tạm khóa, tạm thời không thể vào Vương Quốc Moly.",
    "\\r帐号与密码不符请再试一次吧！": "\\nTài khoản hoặc mật khẩu không đúng, vui lòng thử lại!",
    "您的帐号没有激活\\n请查收邮件激活帐号！": "Tài khoản chưa được kích hoạt, vui lòng kiểm tra email kích hoạt!",
    "因长时间未登陆，我们暂时冻结了您的帐号,详情请联系kf.61.com": "Tài khoản lâu ngày không đăng nhập nên tạm thời được bảo lưu.",
    "可能服务器在维护！": "Máy chủ hiện đang bảo trì, vui lòng quay lại sau!",
    "登录服务器连接成功！IP:": "Kết nối máy chủ đăng nhập thành công! IP:",
    "连接关闭！": "Đã ngắt kết nối!",

    # LoginSelectPage.as
    "清空本地帐号不会删除帐号内物品！如果小摩尔是在学校、网吧等公共场所上网，建议将本地帐号清空，避免盗号！": "Xóa tài khoản lưu trên máy sẽ không làm mất đồ trong game! Nếu đang chơi ở nơi công cộng, bạn nên xóa lưu để tránh lộ mật khẩu nhé!",
    "是否清空本地帐号？": "Bạn có chắc chắn muốn xóa danh sách tài khoản lưu trên máy này?",

    # LoginServerPage.as
    "拉取推荐服务器列表 出错": "Không thể tải danh sách máy chủ gợi ý",
    "请输入服务器名称": "Vui lòng nhập tên máy chủ",
    "服务器不存在，请选择其它服务器！": "Máy chủ không tồn tại, vui lòng chọn máy chủ khác!",
    "请输入服务器名或编号！": "Vui lòng nhập tên hoặc số hiệu máy chủ!",
    "  抱歉": "  Rất tiếc,",
    "已满，请选择其它服务器!": " đã đầy, vui lòng chọn máy chủ khác!",

    # LoginOneAuthCode.as
    "密码错误太多，请输入验证码。": "Nhập sai mật khẩu nhiều lần, vui lòng nhập mã xác nhận.",
    "验证码输入错误。": "Mã xác nhận không đúng.",
    "帐号被封。": "Tài khoản đang bị tạm khóa.",
    "系统错误或帐号未实名认证,请登录account.61.com进行实名认证。": "Lỗi hệ thống hoặc tài khoản chưa kích hoạt.",

    # RegisterErrorCode.as
    "网络错误,请稍后再试！": "Lỗi kết nối mạng, vui lòng thử lại sau!",
    "系统错误,请稍后再试": "Lỗi hệ thống, vui lòng thử lại sau!",
    "系统错误,请稍后再试！": "Lỗi hệ thống, vui lòng thử lại sau!",
    "2次输入不相同！": "Hai lần nhập mật khẩu không khớp nhau!",
    "密码太简单！": "Mật khẩu quá đơn giản!",
    "验证码错误,请重新输入！": "Mã xác nhận sai, vui lòng nhập lại!",
}

def translate_as_files():
    as_dir = Path("work/dump_login_as/scripts")
    count = 0
    file_count = 0
    for p in as_dir.rglob("*.as"):
        try:
            content = p.read_text(encoding="utf-8")
        except:
            continue
            
        modified = False
        for zh, vi in TRANSLATIONS.items():
            if zh in content:
                content = content.replace(zh, vi)
                modified = True
                count += 1
                
        if modified:
            p.write_text(content, encoding="utf-8")
            file_count += 1
            print(f"Translated strings in {p.relative_to(as_dir)}")
            
    print(f"\nDone! Replaced {count} strings across {file_count} ActionScript files.")

if __name__ == "__main__":
    translate_as_files()
