import sys
from pathlib import Path
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def update_play_html():
    filepath = Path("web/play.html")
    content = filepath.read_text(encoding="utf-8")

    # 1. Update modal CSS
    old_css = '''.modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 20px;
    }

    .modal-overlay.open {
      display: flex;
    }

    .modal-box {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 20px;
      width: 100%;
      max-width: 480px;
      max-height: 90vh;
      overflow-y: auto;
      color: #fff;
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid #334155;
    }'''

    new_css = '''.modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 20px;
      cursor: pointer;
    }

    .modal-overlay.open {
      display: flex;
    }

    .modal-box {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 20px;
      width: 100%;
      max-width: 480px;
      max-height: 90vh;
      overflow-y: auto;
      color: #fff;
      cursor: default;
      position: relative;
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid #334155;
      position: sticky;
      top: -20px;
      background: #1e293b;
      z-index: 20;
      padding-top: 4px;
    }'''
    if old_css in content:
        content = content.replace(old_css, new_css)
    else:
        print("[WARN] old_css not found in play.html")

    # 2. Update inline onclick on overlays
    modal_maps = [
        ('id="modal-account" class="modal-overlay"', 'id="modal-account" class="modal-overlay" onclick="if(event.target===this){closeAccountModal();}"'),
        ('id="modal-gc" class="modal-overlay"', 'id="modal-gc" class="modal-overlay" onclick="if(event.target===this){closeGiftcodeModal();}"'),
        ('id="modal-lamu" class="modal-overlay"', 'id="modal-lamu" class="modal-overlay" onclick="if(event.target===this){closeSuperLamuModal();}"'),
    ]
    for old, new in modal_maps:
        if old in content:
            content = content.replace(old, new)

    # 3. Add bottom buttons to tab-content-login in play.html
    login_btn_needle = '<!-- Cổng Quản Trị Viên (Ẩn mờ kín đáo, có xác thực mã PIN) -->'
    login_btn_addition = '''<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding-top: 10px; border-top: 1px solid #334155;">
            <button type="button" class="btn-ctrl" style="background: #334155; color: #fff;" onclick="closeAccountModal()">← Trở lại</button>
            <button type="button" class="btn-ctrl" onclick="closeAccountModal()">✕ Đóng</button>
          </div>

          <!-- Cổng Quản Trị Viên (Ẩn mờ kín đáo, có xác thực mã PIN) -->'''
    if login_btn_needle in content and "✕ Đóng" not in content[:content.find(login_btn_needle)]:
        content = content.replace(login_btn_needle, login_btn_addition, 1)

    # 4. Add bottom buttons to tab-content-reg in play.html
    reg_btn_needle = '</form>\n      </div>\n\n      <!-- Tab 3: Quên / Đặt Lại Mật Khẩu Trước Khi Đăng Nhập -->'
    reg_btn_addition = '''  <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding-top: 10px; border-top: 1px solid #334155;">
            <button type="button" class="btn-ctrl" style="background: #334155; color: #fff;" onclick="openLoginTab()">← Trở lại Đăng Nhập</button>
            <button type="button" class="btn-ctrl" onclick="closeAccountModal()">✕ Đóng</button>
          </div>
        </form>
      </div>

      <!-- Tab 3: Quên / Đặt Lại Mật Khẩu Trước Khi Đăng Nhập -->'''
    if reg_btn_needle in content:
        content = content.replace(reg_btn_needle, reg_btn_addition, 1)

    # 5. Add bottom buttons to tab-content-forgot in play.html
    forgot_btn_needle = '</form>\n      </div>\n\n      <!-- Tab 4: Bảng Quản Lý Hồ Sơ Cư Dân (Hiển thị khi ĐÃ đăng nhập) -->'
    forgot_btn_addition = '''  <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding-top: 10px; border-top: 1px solid #334155;">
            <button type="button" class="btn-ctrl" style="background: #334155; color: #fff;" onclick="openLoginTab()">← Trở lại Đăng Nhập</button>
            <button type="button" class="btn-ctrl" onclick="closeAccountModal()">✕ Đóng</button>
          </div>
        </form>
      </div>

      <!-- Tab 4: Bảng Quản Lý Hồ Sơ Cư Dân (Hiển thị khi ĐÃ đăng nhập) -->'''
    if forgot_btn_needle in content:
        content = content.replace(forgot_btn_needle, forgot_btn_addition, 1)

    # 6. Add bottom buttons to tab-content-dashboard in play.html
    dash_btn_needle = '</form>\n      </div>\n\n      <!-- Tab 5: Mua Đậu & Trở Thành Hội Viên Siêu Cấp -->'
    dash_btn_addition = '''  <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding-top: 10px; border-top: 1px solid #334155;">
            <button type="button" class="btn-ctrl" style="background: #334155; color: #fff;" onclick="closeAccountModal()">← Trở lại</button>
            <button type="button" class="btn-ctrl" onclick="closeAccountModal()">✕ Đóng</button>
          </div>
        </form>
      </div>

      <!-- Tab 5: Mua Đậu & Trở Thành Hội Viên Siêu Cấp -->'''
    if dash_btn_needle in content:
        content = content.replace(dash_btn_needle, dash_btn_addition, 1)

    # 7. Global event listener upgrade in play.html
    old_listener = '''      // Modal Backdrop Click & Escape Key Listeners
      document.querySelectorAll(".modal-overlay").forEach(overlay => {
        overlay.addEventListener("click", (e) => {
          if (e.target === overlay) {
            overlay.classList.remove("open");
          }
        });
      });

      document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
          document.querySelectorAll(".modal-overlay").forEach(overlay => {
            overlay.classList.remove("open");
          });
        }
      });'''

    new_listener = '''      // Modal Backdrop Click & Escape Key Listeners
      document.addEventListener("click", (e) => {
        if (e.target && e.target.classList && e.target.classList.contains("modal-overlay")) {
          e.target.classList.remove("open");
        }
      });

      document.addEventListener("touchend", (e) => {
        if (e.target && e.target.classList && e.target.classList.contains("modal-overlay")) {
          e.target.classList.remove("open");
        }
      });

      document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
          document.querySelectorAll(".modal-overlay.open").forEach(overlay => {
            overlay.classList.remove("open");
          });
        }
      });'''
    if old_listener in content:
        content = content.replace(old_listener, new_listener)

    filepath.write_text(content, encoding="utf-8")
    print("Updated web/play.html successfully!")

update_play_html()
