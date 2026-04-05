document.addEventListener('DOMContentLoaded', () => {
    const usernameInput = document.getElementById('username');
    const verifyBtn = document.getElementById('verifyBtn');
    const statusMsg = document.getElementById('statusMsg');
    const drawerForm = document.getElementById('drawerForm');
    const submitBtn = drawerForm.querySelector('button[type="submit"]');

    // --- 1. VERIFICATION LOGIC (Add Mode) ---
    
    // Show/Hide Verify button based on input length
    usernameInput.addEventListener('input', (e) => {
        const val = e.target.value.trim();
        statusMsg.innerText = ""; // Clear status while typing
        
        if (val.length > 2) {
            verifyBtn.classList.remove('hidden');
        } else {
            verifyBtn.classList.add('hidden');
            submitBtn.disabled = true; // Block submit if name is too short
        }
    });

    verifyBtn.addEventListener('click', async () => {
        const username = usernameInput.value.trim();
        statusMsg.innerText = "Checking...";
        statusMsg.className = "status-msg";

        try {
            // Updated to pass the username as a query parameter
            const response = await fetch(`/uh/verify-username/?username=${encodeURIComponent(username)}`);
            const data = await response.json();

            if (data.exists) {
                statusMsg.innerText = "✅ User found! You can add them.";
                statusMsg.className = "status-msg success";
                submitBtn.disabled = false; // Enable "Add Staff"
            } else {
                statusMsg.innerText = "❌ User does not exist.";
                statusMsg.className = "status-msg error";
                submitBtn.disabled = true;
            }
        } catch (err) {
            statusMsg.innerText = "Server error. Try again.";
            console.error(err);
        }
    });

    // --- 2. DELETE LOGIC (Selection Mode) ---
    
    // This connects to the "btn-delete" in your staff list
    const deleteBtn = document.querySelector('.btn-delete');
    
    if (deleteBtn) {
        deleteBtn.addEventListener('click', () => {
            // Get selected card data (from our previous selection logic)
            const selectedCard = document.querySelector('.clickable-card.selected');
            
            if (!selectedCard) {
                return alert("Please select a staff member to remove.");
            }

            const staffId = selectedCard.dataset.id;
            const staffName = selectedCard.dataset.name || "this user";

            // Trigger the global confirmation modal
            const modal = document.getElementById('confirmModal');
            const modalOverlay = document.getElementById('modalOverlay');
            
            document.getElementById('modalMessage').innerText = `Revoke access for ${staffName}?`;
            
            modal.classList.add('show');
            modalOverlay.classList.add('show');

            // Set the target URL for the "Confirm" button in the modal
            window.pendingDeleteUrl = `/uh/remove-staff/${staffId}/`;
        });
    }
});

