function changeExercise() {
    let selectedExercise = document.getElementById("exercise-select").value;

    fetch("/select_exercise", {
        method: "POST",
        body: new URLSearchParams({ exercise: selectedExercise }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    }).then(() => {
        // Refresh video feed after exercise selection
        document.getElementById("video-feed").src = "/video_feed?" + new Date().getTime();
    });
}
