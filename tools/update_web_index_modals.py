import sys
from pathlib import Path
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def update_index_html():
    filepath = Path("web/index.html")
    content = filepath.read_text(encoding="utf-8")

    # 1. Update all modal overlays to have inline onclick backdrop closing
    modal_maps = [
        ('id="modal-account" class="modal-overlay"', 'id="modal-account" class="modal-overlay" onclick="if(event.target===this){closeAccountModal();}"'),
        ('id="modal-gc" class="modal-overlay"', 'id="modal-gc" class="modal-overlay" onclick="if(event.target===this){closeGiftcodeModal();}"'),
        ('id="modal-lamu" class="modal-overlay"', 'id="modal-lamu" class="modal-overlay" onclick="if(event.target===this){closeSuperLamuModal();}"'),
        ('id="modal-lookup" class="modal-overlay"', 'id="modal-lookup" class="modal-overlay" onclick="if(event.target===this){closeLookupModal();}"'),
        ('id="modal-news" class="modal-overlay"', 'id="modal-news" class="modal-overlay" onclick="if(event.target===this){closeNewsModal();}"'),
        ('id="modal-kingdom" class="modal-overlay"', 'id="modal-kingdom" class="modal-overlay" onclick="if(event.target===this){closeKingdomInfoModal();}"'),
    ]
    for old, new in modal_maps:
        if old in content:
            content = content.replace(old, new)

    # 2. Add bottom buttons to tab-content-login if not present
    login_btn_needle = '<!-- Cổng Quản Trị Viên (Ẩn mờ kín đáo, có xác thực mã PIN) -->'
    login_btn_addition = '''<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding-top: 10px; border-top: 1px solid #334155;">
            <button type="button" class="nav-btn" style="background: #334155; color: #fff;" onclick="closeAccountModal()">← Trở lại</button>
            <button type="button" class="nav-btn" onclick="closeAccountModal()">✕ Đóng</button>
          </div>

          <!-- Cổng Quản Trị Viên (Ẩn mờ kín đáo, có xác thực mã PIN) -->'''
    if login_btn_needle in content and "✕ Đóng" not in content[:content.find(login_btn_needle)]:
        content = content.replace(login_btn_needle, login_btn_addition, 1)

    # 3. Add bottom buttons to tab-content-reg if not present
    reg_btn_needle = '</form>\n      </div>\n\n      <!-- Tab 3: Quên / Đặt Lại Mật Khẩu Trước Khi Đăng Nhập -->'
    reg_btn_addition = '''  <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding-top: 10px; border-top: 1px solid #334155;">
            <button type="button" class="nav-btn" style="background: #334155; color: #fff;" onclick="openLoginTab()">← Trở lại Đăng Nhập</button>
            <button type="button" class="nav-btn" onclick="closeAccountModal()">✕ Đóng</button>
          </div>
        </form>
      </div>

      <!-- Tab 3: Quên / Đặt Lại Mật Khẩu Trước Khi Đăng Nhập -->'''
    if reg_btn_needle in content:
        content = content.replace(reg_btn_needle, reg_btn_addition, 1)

    # 4. Add bottom buttons to tab-content-forgot if not present
    forgot_btn_needle = '</form>\n      </div>\n\n      <!-- Tab 4: Bảng Quản Lý Hồ Sơ Cư Dân (Hiển thị khi ĐÃ đăng nhập) -->'
    forgot_btn_addition = '''  <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding-top: 10px; border-top: 1px solid #334155;">
            <button type="button" class="nav-btn" style="background: #334155; color: #fff;" onclick="openLoginTab()">← Trở lại Đăng Nhập</button>
            <button type="button" class="nav-btn" onclick="closeAccountModal()">✕ Đóng</button>
          </div>
        </form>
      </div>

      <!-- Tab 4: Bảng Quản Lý Hồ Sơ Cư Dân (Hiển thị khi ĐÃ đăng nhập) -->'''
    if forgot_btn_needle in content:
        content = content.replace(forgot_btn_needle, forgot_btn_addition, 1)

    # 5. Add bottom buttons to tab-content-dashboard if not present
    dash_btn_needle = '</form>\n      </div>\n\n      <!-- Tab 5: Mua Đậu & Trở Thành Hội Viên Siêu Cấp -->'
    dash_btn_addition = '''  <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding-top: 10px; border-top: 1px solid #334155;">
            <button type="button" class="nav-btn" style="background: #334155; color: #fff;" onclick="closeAccountModal()">← Trở lại</button>
            <button type="button" class="nav-btn" onclick="closeAccountModal()">✕ Đóng</button>
          </div>
        </form>
      </div>

      <!-- Tab 5: Mua Đậu & Trở Thành Hội Viên Siêu Cấp -->'''
    if dash_btn_needle in content:
        content = content.replace(dash_btn_needle, dash_btn_addition, 1)

    # 6. Global event listener upgrade at the bottom
    old_listener = '''    // --- Global Modal Backdrop Click & Escape Key Auto-Close ---
    document.querySelectorAll(".modal-overlay").forEach(overlay => {
      overlay.addEventListener("click", function(e) {
        if (e.target === this) {
          this.classList.remove("open");
        }
      });
    });

    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape") {
        document.querySelectorAll(".modal-overlay.open").forEach(modal => modal.classList.remove("open"));
      }
    });'''

    new_listener = '''    // --- Global Modal Backdrop Click & Escape Key Auto-Close ---
    document.addEventListener("click", function(e) {
      if (e.target && e.target.classList && e.target.classList.contains("modal-overlay")) {
        e.target.classList.remove("open");
      }
    });

    document.addEventListener("touchend", function(e) {
      if (e.target && e.target.classList && e.target.classList.contains("modal-overlay")) {
        e.target.classList.remove("open");
      }
    });

    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape") {
        document.querySelectorAll(".modal-overlay.open").forEach(modal => modal.classList.remove("open"));
      }
    });'''
    if old_listener in content:
        content = content.replace(old_listener, new_listener)

    filepath.write_text(content, encoding="utf-8")
    print("Updated web/index.html successfully!")

update_index_html()
