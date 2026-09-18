// Auto-fade flash messages after a few seconds so old login/register
// errors don't linger forever on the screen.
document.addEventListener("DOMContentLoaded", () => {
  const flashes = document.querySelectorAll(".flash");
  flashes.forEach((el) => {
    setTimeout(() => {
      el.style.transition = "opacity 0.6s ease";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 600);
    }, 5000);
  });
});