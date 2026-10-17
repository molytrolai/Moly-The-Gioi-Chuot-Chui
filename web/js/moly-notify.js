/**
 * Moly Vietnam 2.0 - Universal Glassmorphic Alert & Notification System
 * Replaces native browser alert/confirm with luxury frosted glass popups and toasts.
 */
(function() {
  // Inject Notification Container and Styles
  const style = document.createElement("style");
  style.textContent = `
    .moly-alert-overlay {
      position: fixed;
      inset: 0;
      background: rgba(10, 16, 30, 0.45);
      backdrop-filter: blur(8px) saturate(130%);
      -webkit-backdrop-filter: blur(8px) saturate(130%);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 999999;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.22s ease;
      overflow: hidden;
      overscroll-behavior: contain;
    }
    .moly-alert-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }
    .moly-alert-modal {
      background: linear-gradient(135deg, rgba(22, 34, 52, 0.94) 0%, rgba(14, 22, 36, 0.98) 100%);
      backdrop-filter: blur(28px) saturate(190%);
      -webkit-backdrop-filter: blur(28px) saturate(190%);
      border: 1px solid rgba(255, 255, 255, 0.25);
      border-top: 1px solid rgba(255, 255, 255, 0.65);
      border-radius: 20px;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.75), 0 0 30px rgba(246, 168, 40, 0.3), inset 0 1px 2px rgba(255, 255, 255, 0.45);
      width: 90%;
      max-width: 440px;
      padding: 24px;
      text-align: center;
      transform: scale(0.92) translateY(12px);
      transition: transform 0.24s cubic-bezier(0.16, 1, 0.3, 1);
      box-sizing: border-box;
      overscroll-behavior: contain;
    }
    .moly-alert-overlay.open .moly-alert-modal {
      transform: scale(1) translateY(0);
    }
    .moly-alert-icon {
      width: 58px;
      height: 58px;
      border-radius: 50%;
      margin: 0 auto 16px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.6);
    }
    .moly-alert-icon.success {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.3), rgba(5, 150, 105, 0.6));
      border: 2px solid #34d399;
      color: #34d399;
    }
    .moly-alert-icon.error {
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.3), rgba(185, 28, 28, 0.6));
      border: 2px solid #f87171;
      color: #f87171;
    }
    .moly-alert-icon.warning {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.3), rgba(217, 119, 6, 0.6));
      border: 2px solid #fbbf24;
      color: #fbbf24;
    }
    .moly-alert-icon.info {
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(29, 78, 216, 0.6));
      border: 2px solid #60a5fa;
      color: #60a5fa;
    }
    .moly-alert-title {
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 10px;
      text-shadow: 0 2px 8px rgba(0,0,0,0.6);
    }
    .moly-alert-msg {
      font-size: 14px;
      color: #cbd5e1;
      line-height: 1.55;
      margin-bottom: 22px;
      word-break: break-word;
      text-align: left;
      background: rgba(15, 23, 42, 0.55);
      padding: 12px 14px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .moly-alert-actions {
      display: flex;
      gap: 12px;
      justify-content: center;
    }
    .moly-alert-btn {
      flex: 1;
      padding: 11px 20px;
      border-radius: 9999px;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid rgba(255, 255, 255, 0.3);
      border-top: 1px solid rgba(255, 255, 255, 0.7);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      user-select: none;
    }
    .moly-alert-btn-primary {
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.35) 0%, rgba(255, 255, 255, 0.08) 50%, rgba(0, 0, 0, 0.15) 100%),
                  linear-gradient(135deg, #f59e0b 0%, #ea580c 100%);
      color: #ffffff;
      box-shadow: 0 4px 16px rgba(234, 88, 12, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.8);
    }
    .moly-alert-btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(234, 88, 12, 0.7), 0 0 20px rgba(253, 224, 71, 0.8);
      border-color: #fde047;
    }
    .moly-alert-btn-secondary {
      background: rgba(30, 41, 59, 0.8);
      color: #cbd5e1;
    }
    .moly-alert-btn-secondary:hover {
      background: rgba(51, 65, 85, 0.9);
      color: #ffffff;
    }

    /* Floating Toast System */
    .moly-toast-container {
      position: fixed;
      top: 24px;
      right: 24px;
      z-index: 1000000;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    }
    .moly-toast {
      background: linear-gradient(135deg, rgba(20, 30, 48, 0.95) 0%, rgba(12, 18, 30, 0.98) 100%);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.22);
      border-top: 1px solid rgba(255, 255, 255, 0.6);
      border-radius: 9999px;
      padding: 10px 20px;
      color: #ffffff;
      font-size: 13.5px;
      font-weight: 600;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6), 0 0 20px rgba(246, 168, 40, 0.25);
      display: flex;
      align-items: center;
      gap: 10px;
      opacity: 0;
      transform: translateY(-14px) scale(0.95);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      pointer-events: auto;
    }
    .moly-toast.show {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  `;
  document.head.appendChild(style);

  // Modal DOM
  let alertOverlay = null;
  let alertIcon = null;
  let alertTitle = null;
  let alertMsg = null;
  let alertConfirmBtn = null;
  let alertCancelBtn = null;
  let activeCallback = null;

  function initAlertModal() {
    if (alertOverlay) return;
    alertOverlay = document.createElement("div");
    alertOverlay.className = "moly-alert-overlay";
    alertOverlay.innerHTML = `
      <div class="moly-alert-modal" role="dialog" aria-modal="true">
        <div class="moly-alert-icon" id="moly-alert-icon">✨</div>
        <h3 class="moly-alert-title" id="moly-alert-title">Thông Báo Vương Quốc</h3>
        <div class="moly-alert-msg" id="moly-alert-msg"></div>
        <div class="moly-alert-actions">
          <button type="button" class="moly-alert-btn moly-alert-btn-secondary" id="moly-alert-cancel" style="display: none;">Hủy Bỏ</button>
          <button type="button" class="moly-alert-btn moly-alert-btn-primary" id="moly-alert-confirm">Đã Hiểu</button>
        </div>
      </div>
    `;
    document.body.appendChild(alertOverlay);

    alertIcon = alertOverlay.querySelector("#moly-alert-icon");
    alertTitle = alertOverlay.querySelector("#moly-alert-title");
    alertMsg = alertOverlay.querySelector("#moly-alert-msg");
    alertConfirmBtn = alertOverlay.querySelector("#moly-alert-confirm");
    alertCancelBtn = alertOverlay.querySelector("#moly-alert-cancel");

    alertConfirmBtn.addEventListener("click", () => {
      closeAlert(true);
    });

    alertCancelBtn.addEventListener("click", () => {
      closeAlert(false);
    });

    alertOverlay.addEventListener("click", (e) => {
      if (e.target === alertOverlay) {
        closeAlert(false);
      }
    });

    document.addEventListener("keydown", (e) => {
      if (alertOverlay.classList.contains("open")) {
        if (e.key === "Escape") closeAlert(false);
        if (e.key === "Enter") closeAlert(true);
      }
    });
  }

  function closeAlert(isConfirmed) {
    if (!alertOverlay) return;
    alertOverlay.classList.remove("open");
    if (activeCallback) {
      const cb = activeCallback;
      activeCallback = null;
      cb(isConfirmed);
    }
  }

  // Toast Container
  let toastContainer = null;
  function getToastContainer() {
    if (!toastContainer) {
      toastContainer = document.createElement("div");
      toastContainer.className = "moly-toast-container";
      document.body.appendChild(toastContainer);
    }
    return toastContainer;
  }

  const MolyNotify = {
    alert(message, title, type = "info") {
      return new Promise((resolve) => {
        initAlertModal();
        
        let detectedType = type;
        const msgStr = String(message || "");
        if (msgStr.includes("✅") || msgStr.toLowerCase().includes("thành công") || msgStr.toLowerCase().includes("hoàn tất")) {
          detectedType = "success";
        } else if (msgStr.includes("❌") || msgStr.includes("từ chối") || msgStr.toLowerCase().includes("thất bại") || msgStr.toLowerCase().includes("lỗi")) {
          detectedType = "error";
        } else if (msgStr.includes("⚠️") || msgStr.toLowerCase().includes("cảnh báo") || msgStr.toLowerCase().includes("chú ý")) {
          detectedType = "warning";
        }

        alertIcon.className = "moly-alert-icon " + detectedType;
        if (detectedType === "success") alertIcon.textContent = "✅";
        else if (detectedType === "error") alertIcon.textContent = "❌";
        else if (detectedType === "warning") alertIcon.textContent = "⚠️";
        else alertIcon.textContent = "🏰";

        alertTitle.textContent = title || (detectedType === "error" ? "Thông Báo Xử Lý" : (detectedType === "success" ? "Thành Công" : "Thông Báo Hệ Thống"));
        alertMsg.innerHTML = msgStr.replace(/\n/g, "<br>");
        
        alertCancelBtn.style.display = "none";
        alertConfirmBtn.textContent = "Đã Hiểu";
        alertConfirmBtn.focus();

        activeCallback = () => resolve(true);
        alertOverlay.classList.add("open");

        if (window.MolyAudio) {
          if (detectedType === "success") window.MolyAudio.playChime();
          else if (detectedType === "error") window.MolyAudio.playWarn();
          else window.MolyAudio.playPop();
        }
      });
    },

    confirm(message, title = "Xác Nhận Hành Động") {
      return new Promise((resolve) => {
        initAlertModal();

        alertIcon.className = "moly-alert-icon warning";
        alertIcon.textContent = "❓";
        alertTitle.textContent = title;
        alertMsg.innerHTML = String(message || "").replace(/\n/g, "<br>");

        alertCancelBtn.style.display = "inline-block";
        alertCancelBtn.textContent = "Hủy Bỏ";
        alertConfirmBtn.textContent = "Xác Nhận";
        alertConfirmBtn.focus();

        activeCallback = (result) => resolve(!!result);
        alertOverlay.classList.add("open");

        if (window.MolyAudio) {
          window.MolyAudio.playPop();
        }
      });
    },

    toast(message, type = "info", duration = 3000) {
      const container = getToastContainer();
      const toast = document.createElement("div");
      toast.className = "moly-toast";
      
      let icon = "✨";
      if (type === "success") icon = "✅";
      if (type === "error") icon = "❌";
      if (type === "warning") icon = "⚠️";

      toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
      container.appendChild(toast);

      requestAnimationFrame(() => {
        toast.classList.add("show");
      });

      if (window.MolyAudio) {
        window.MolyAudio.playPop();
      }

      setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 250);
      }, duration);
    }
  };

  // Gracefully intercept standard browser alert
  window.originalAlert = window.alert;
  window.alert = function(msg) {
    MolyNotify.alert(msg);
  };

  window.MolyNotify = MolyNotify;
})();
