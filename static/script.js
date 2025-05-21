function changeExercise() {
    let selectedExercise = document.getElementById("exercise-select").value;

    // Show/hide containers based on selected exercise
    const singleRepContainer = document.querySelector('.single-rep-container');
    const doubleRepContainer = document.querySelector('.double-rep-container');

    if (selectedExercise === 'squat') {
        singleRepContainer.style.display = 'block';
        doubleRepContainer.style.display = 'none';
    } else {
        singleRepContainer.style.display = 'none';
        doubleRepContainer.style.display = 'flex'; // or 'block' depending on your layout
    }
    fetch("/select_exercise", {
        method: "POST",
        body: new URLSearchParams({ exercise: selectedExercise }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    }).then(() => {
        // Refresh video feed after exercise selection
        document.getElementById("video-feed").src = "/video_feed?" + new Date().getTime();
    });
}

function updateReps() {
    fetch('/get_reps')
        .then(response => response.json())
        .then(data => {
            leftData = data[0];
            rightData = data[1];
            // document.getElementById('rep-count').textContent = data.left_counter;
            document.getElementById('left-rep-count').textContent = leftData.left_counter;
            document.getElementById('right-rep-count').textContent = rightData.right_counter;
            document.getElementById('left-stage').textContent = leftData.left_stage || '-';
            document.getElementById('right-stage').textContent = rightData.right_stage || '-';
            document.getElementById('rep-display').innerText =
                `Reps: ${data.left_counter}, Stage: ${data.stage || '-'}`;                    
        });
}

setInterval(updateReps, 1000); // Update every 1 second
