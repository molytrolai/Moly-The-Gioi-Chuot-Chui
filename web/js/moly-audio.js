/**
 * Moly Vietnam 2.0 - Interactive Web Audio Engine
 * Zero-latency synthesized sound effects via Web Audio API.
 * No external sound files needed. 100% reliable across all browsers & devices.
 */
(function() {
  let audioCtx = null;
  let isSoundEnabled = localStorage.getItem("moly_sound_enabled") !== "false";

  function getAudioContext() {
    if (!audioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) {
        audioCtx = new AudioContextClass();
      }
    }
    if (audioCtx && audioCtx.state === "suspended") {
      audioCtx.resume();
    }
    return audioCtx;
  }

  const MolyAudio = {
    isEnabled() {
      return isSoundEnabled;
    },

    toggle() {
      isSoundEnabled = !isSoundEnabled;
      localStorage.setItem("moly_sound_enabled", isSoundEnabled ? "true" : "false");
      this.updateUI();
      if (isSoundEnabled) {
        this.playPop();
      }
      return isSoundEnabled;
    },

    setSound(enabled) {
      isSoundEnabled = !!enabled;
      localStorage.setItem("moly_sound_enabled", isSoundEnabled ? "true" : "false");
      this.updateUI();
    },

    playPop() {
      if (!isSoundEnabled) return;
      const ctx = getAudioContext();
      if (!ctx) return;
      try {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sine";
        const now = ctx.currentTime;
        osc.frequency.setValueAtTime(450, now);
        osc.frequency.exponentialRampToValueAtTime(750, now + 0.05);
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.06);
      } catch (e) {
        // audio error ignored
      }
    },

    playClick() {
      if (!isSoundEnabled) return;
      const ctx = getAudioContext();
      if (!ctx) return;
      try {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "triangle";
        const now = ctx.currentTime;
        osc.frequency.setValueAtTime(900, now);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.03);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.03);
      } catch (e) {}
    },

    playChime() {
      if (!isSoundEnabled) return;
      const ctx = getAudioContext();
      if (!ctx) return;
      try {
        const now = ctx.currentTime;
        const freqs = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6 arpeggio
        freqs.forEach((freq, idx) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = "sine";
          const start = now + idx * 0.06;
          osc.frequency.setValueAtTime(freq, start);
          gain.gain.setValueAtTime(0.12, start);
          gain.gain.exponentialRampToValueAtTime(0.001, start + 0.25);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(start);
          osc.stop(start + 0.25);
        });
      } catch (e) {}
    },

    playWarn() {
      if (!isSoundEnabled) return;
      const ctx = getAudioContext();
      if (!ctx) return;
      try {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sawtooth";
        const now = ctx.currentTime;
        osc.frequency.setValueAtTime(220, now);
        osc.frequency.exponentialRampToValueAtTime(160, now + 0.12);
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.12);
      } catch (e) {}
    },

    updateUI() {
      document.querySelectorAll(".moly-sound-btn").forEach(btn => {
        if (isSoundEnabled) {
          btn.innerHTML = `<span class="sound-icon">🔊</span> <span class="sound-text">Âm thanh: Bật</span>`;
          btn.classList.add("sound-on");
          btn.classList.remove("sound-off");
        } else {
          btn.innerHTML = `<span class="sound-icon">🔇</span> <span class="sound-text">Âm thanh: Tắt</span>`;
          btn.classList.add("sound-off");
          btn.classList.remove("sound-on");
        }
      });
    },

    initAutoSounds() {
      document.addEventListener("click", (e) => {
        const target = e.target.closest("button, .btn, .tab-btn, .nav-item, .card-btn, a[href^='#']");
        if (target) {
          if (target.classList.contains("moly-sound-btn")) {
            // Handled by toggle
            return;
          }
          if (target.dataset.sound === "chime" || target.classList.contains("btn-success") || target.classList.contains("btn-warning")) {
            this.playChime();
          } else if (target.classList.contains("tab-btn")) {
            this.playClick();
          } else {
            this.playPop();
          }
        }
      });
      this.updateUI();
    }
  };

  window.MolyAudio = MolyAudio;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => MolyAudio.initAutoSounds());
  } else {
    MolyAudio.initAutoSounds();
  }
})();
