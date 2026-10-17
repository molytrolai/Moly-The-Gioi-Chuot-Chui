/**
 * Moly Kingdom Ambient Particles (Fairy Dust & Fireflies)
 * High-performance background visual atmosphere.
 */
(function() {
  function initAmbientCanvas() {
    let canvas = document.getElementById("moly-ambient-canvas");
    if (!canvas) {
      canvas = document.createElement("canvas");
      canvas.id = "moly-ambient-canvas";
      canvas.style.position = "fixed";
      canvas.style.top = "0";
      canvas.style.left = "0";
      canvas.style.width = "100%";
      canvas.style.height = "100%";
      canvas.style.pointerEvents = "none";
      canvas.style.zIndex = "0";
      canvas.style.opacity = "0.75";
      document.body.insertBefore(canvas, document.body.firstChild);
    }

    const ctx = canvas.getContext("2d");
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener("resize", () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const count = Math.min(35, Math.floor(width / 35));

    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        r: Math.random() * 2.2 + 0.8,
        color: i % 3 === 0 ? "rgba(250, 204, 21, " : (i % 3 === 1 ? "rgba(245, 158, 11, " : "rgba(167, 139, 250, "),
        dx: (Math.random() - 0.5) * 0.45,
        dy: -(Math.random() * 0.4 + 0.15),
        pulse: Math.random() * Math.PI,
        pulseSpeed: 0.02 + Math.random() * 0.03
      });
    }

    let isVisible = true;
    document.addEventListener("visibilitychange", () => {
      isVisible = !document.hidden;
    });

    function render() {
      if (isVisible) {
        ctx.clearRect(0, 0, width, height);
        for (let i = 0; i < particles.length; i++) {
          const p = particles[i];
          p.x += p.dx;
          p.y += p.dy;
          p.pulse += p.pulseSpeed;

          if (p.x < 0) p.x = width;
          if (p.x > width) p.x = 0;
          if (p.y < 0) p.y = height;

          const alpha = 0.25 + 0.45 * Math.sin(p.pulse);
          if (alpha > 0.05) {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.color + alpha + ")";
            ctx.shadowColor = p.color + "0.8)";
            ctx.shadowBlur = p.r * 3;
            ctx.fill();
            ctx.shadowBlur = 0;
          }
        }
      }
      requestAnimationFrame(render);
    }

    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAmbientCanvas);
  } else {
    initAmbientCanvas();
  }
})();
