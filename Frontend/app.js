// frontend/app.js

document.getElementById('tweet-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const tweetText = document.getElementById('tweet-text').value;
    const scheduleTime = document.getElementById('schedule-time').value;
  
    if (!tweetText || !scheduleTime) {
      alert("Please fill in both fields.");
      return;
    }
  
    try {
      // Log raw time value
      console.log('Raw time:', scheduleTime);
      
      const formattedTime = scheduleTime.slice(0, 16); // Take only YYYY-MM-DDTHH:MM part
      console.log('Formatted time:', formattedTime);
      
      const scheduleData = {
        text: tweetText,
        time: formattedTime
      };
      console.log('Sending data:', scheduleData);
      
      const response = await fetch('http://127.0.0.1:5000/schedule', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(scheduleData),
      });
      
      const data = await response.json();
      console.log('Response:', data);
      
      document.getElementById('response-message').innerText = data.message;
    } catch (error) {
      console.error("Detailed error:", error);
      document.getElementById('response-message').innerText = "Error: " + error.message;
    }
});
  
document.getElementById('test-tweet-btn').addEventListener('click', async () => {
    try {
        const dataToSend = { text: "Test tweet from scheduler app" };

        const response = await fetch('http://127.0.0.1:5000/test-tweet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to send tweet');
        }

        const data = await response.json();
        document.getElementById('test-response').innerText = data.message;
        console.log('Test tweet response:', data);
    } catch (error) {
        console.error('Error sending test tweet:', error);
        document.getElementById('test-response').innerText = 'Error: ' + error.message;
    }
});
  