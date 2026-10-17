/**
 * Moly Vietnam 2.0 - Bottom Dock & Popup Manager
 * Ergonomic Mobile Popups, Scroll Fade Effect & Light-Dismiss
 */
(function() {
  window.toggleDockPopup = function(popupId, event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    const targetPopup = document.getElementById(popupId);
    if (!targetPopup) return;

    const isOpen = targetPopup.classList.contains("open");
    window.closeAllDockPopups();

    if (!isOpen) {
      targetPopup.classList.add("open");
      const triggerBtn = event ? event.currentTarget : null;
      if (triggerBtn) {
        triggerBtn.classList.add("active");
      }
      if (window.MolyAudio && typeof window.MolyAudio.playPop === "function") {
        window.MolyAudio.playPop();
      }
    }
  };

  window.closeAllDockPopups = function() {
    document.querySelectorAll(".moly-dock-popup.open").forEach(function(popup) {
      popup.classList.remove("open");
    });
    document.querySelectorAll(".moly-dock-btn.active").forEach(function(btn) {
      btn.classList.remove("active");
    });
  };

  // Light-dismiss on click outside
  document.addEventListener("click", function(e) {
    if (!e.target.closest(".moly-dock-tab-item, .moly-dock-popup")) {
      window.closeAllDockPopups();
    }
  });

  // Light-dismiss on Escape key
  document.addEventListener("keydown", function(e) {
    if (e.key === "Escape") {
      window.closeAllDockPopups();
    }
  });

  // Scroll Fade In / Fade Out effect on both Mobile & Desktop
  let dockScrollTimeout = null;
  window.addEventListener("scroll", function() {
    const dock = document.getElementById("moly-main-dock");
    if (!dock) return;
    
    dock.classList.add("moly-dock-scrolling");
    window.closeAllDockPopups();

    clearTimeout(dockScrollTimeout);
    dockScrollTimeout = setTimeout(function() {
      dock.classList.remove("moly-dock-scrolling");
    }, 220);
  }, { passive: true });
})();
