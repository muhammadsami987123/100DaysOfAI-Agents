document.addEventListener('DOMContentLoaded', () => {
    const alarmForm = document.getElementById('alarmForm');
    const alarmsList = document.getElementById('alarmsList');

    // Function to fetch and display alarms
    const fetchAlarms = async () => {
        try {
            const response = await fetch('/');
            const text = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'text/html');
            const newAlarmsList = doc.getElementById('alarmsList');
            if (newAlarmsList) {
                alarmsList.innerHTML = newAlarmsList.innerHTML;
                attachEventListeners();
            }
        } catch (error) {
            console.error('Error fetching alarms:', error);
        }
    };

    // Function to attach event listeners to edit/delete buttons
    const attachEventListeners = () => {
        document.querySelectorAll('.edit-btn').forEach(button => {
            button.onclick = (event) => {
                const alarmId = event.target.closest('li').dataset.id;
                // Implement edit logic (e.g., open a modal, populate form)
                alert(`Edit alarm with ID: ${alarmId}`);
            };
        });

        document.querySelectorAll('.delete-btn').forEach(button => {
            button.onclick = async (event) => {
                const alarmId = event.target.closest('li').dataset.id;
                if (confirm('Are you sure you want to delete this alarm?')) {
                    try {
                        const response = await fetch(`/cancel_alarm/${alarmId}`, {
                            method: 'POST',
                        });
                        const data = await response.json();
                        if (data.status === 'success') {
                            fetchAlarms(); // Refresh list
                        } else {
                            alert(`Error: ${data.message}`);
                        }
                    } catch (error) {
                        console.error('Error deleting alarm:', error);
                        alert('Failed to delete alarm.');
                    }
                }
            };
        });
    };

    if (alarmForm) {
        alarmForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const time = document.getElementById('time').value;
            const message = document.getElementById('message').value;
            const recurrence = document.getElementById('recurrence').value;

            try {
                const response = await fetch('/add_alarm', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        time: time,
                        message: message,
                        recurrence: recurrence,
                    }).toString(),
                });
                const data = await response.json();
                if (data.status === 'success') {
                    alarmForm.reset();
                    fetchAlarms(); // Refresh list
                } else {
                    alert(`Error: ${data.message}`);
                }
            } catch (error) {
                console.error('Error adding alarm:', error);
                alert('Failed to add alarm.');
            }
        });
    }

    // Initial fetch and attach event listeners
    fetchAlarms();
});
