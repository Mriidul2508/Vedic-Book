document.addEventListener('DOMContentLoaded', () => {
    
    // --- MODAL LOGIC ---
    const modal = document.getElementById('infoModal');
    const closeBtn = document.getElementById('closeModalBtn');
    const cards = document.querySelectorAll('.sanskar-card');

    cards.forEach(card => {
        card.addEventListener('click', function() {
            const name = this.getAttribute('data-name');
            const nameHi = this.getAttribute('data-namehi');
            const descEn = this.getAttribute('data-descen');
            const descHi = this.getAttribute('data-deschi');
            const image = this.getAttribute('data-image');
            const mantra = this.getAttribute('data-mantra');

            document.getElementById('modalTitle').innerText = name;
            document.getElementById('modalTitleHi').innerText = nameHi;
            document.getElementById('modalDescEn').innerText = descEn;
            document.getElementById('modalDescHi').innerText = descHi;
            document.getElementById('modalImage').src = image;
            document.getElementById('modalMantra').innerText = mantra;
            modal.style.display = "block";
        });
    });

    if (closeBtn) {
        closeBtn.onclick = function() {
            modal.style.display = "none";
        }
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // --- BOOKING AVAILABILITY LOGIC ---
    const dateInput = document.getElementById('dateInput');
    const timeInput = document.getElementById('timeInput');
    const statusDiv = document.getElementById('availability-status');

    if (dateInput && timeInput) {
        function checkAvailability() {
            if (dateInput.value && timeInput.value) {
                fetch('/api/check_availability', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ date: dateInput.value, time: timeInput.value })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.available) {
                        statusDiv.innerHTML = `<span style="color:green; font-weight:bold;">Available (${data.slots_left} priests free)</span>`;
                    } else {
                        statusDiv.innerHTML = `<span style="color:red; font-weight:bold;">Slot Full. Please choose another time.</span>`;
                    }
                })
                .catch(err => console.error("Error checking availability:", err));
            }
        }
        dateInput.addEventListener('change', checkAvailability);
        timeInput.addEventListener('change', checkAvailability);
    }
});