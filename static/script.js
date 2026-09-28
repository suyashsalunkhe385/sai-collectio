document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss alert banners after 4 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 400);
        }, 4000);
    });

    // Promo code handler in cart page
    const promoBtn = document.getElementById('apply-promo');
    if (promoBtn) {
        promoBtn.addEventListener('click', () => {
            const input = document.getElementById('promo-code');
            if (input.value.trim().toUpperCase() === 'FIRST10') {
                alert('Promo applied! 10% discount will reflect at checkout.');
            } else {
                alert('Invalid coupon code. Try FIRST10');
            }
        });
    }
});