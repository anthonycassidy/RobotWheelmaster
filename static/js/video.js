document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video-feed');
    
    // Check if video feed is working
    video.onerror = () => {
        document.getElementById('video-status').innerHTML = 
            '<div class="alert alert-danger">Video feed unavailable</div>';
    };
    
    video.onload = () => {
        document.getElementById('video-status').innerHTML = 
            '<div class="alert alert-success">Video feed active</div>';
    };
});
