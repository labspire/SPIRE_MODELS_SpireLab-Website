function generateStars() {
	const container = document.getElementById("starsContainer");
	if (!container) return;

	const fragment = document.createDocumentFragment();
	const starCount = 95;

	for (let i = 0; i < starCount; i++) {
		const star = document.createElement("div");
		star.className = "star twinkle";

		const x = Math.random() * 100;
		const y = Math.random() * 57;
		const size = Math.random() * 1.8 + 0.4;
		const duration = Math.random() * 3 + 2;
		const delay = Math.random() * 4;

		star.style.cssText = `
          left: ${x}%;
          top: ${y}%;
          width: ${size}px;
          height: ${size}px;
          animation-duration: ${duration}s;
          animation-delay: ${delay}s;
        `;

		if (Math.random() < 0.12) {
			star.style.boxShadow = "0 0 6px 1px rgba(255,255,255,.95)";
		}
		fragment.appendChild(star);
	}
	container.appendChild(fragment);
}
document.addEventListener("DOMContentLoaded", generateStars);

// Handles microphone recording for the ASR live transcription demo
function initAsrMic() {
	const micButton = document.getElementById("micButton");
	const micStatus = document.getElementById("micStatus");
	const fileInput = document.getElementById("audioFileInput");

	if (!micButton) return; // Guard in case this script loads on a page without the mic button

	let mediaRecorder = null;
	let audioChunks = [];
	let isRecording = false;

	micButton.addEventListener("click", async function () {
		if (!isRecording) {
			// Start recording
			try {
				const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
				mediaRecorder = new MediaRecorder(stream);
				audioChunks = [];

				mediaRecorder.ondataavailable = function (e) {
					audioChunks.push(e.data);
				};

				mediaRecorder.onstop = function () {
					const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
					const audioFile = new File([audioBlob], "recording.webm", { type: "audio/webm" });

					// Put the recorded file into the file input so the existing form submit works unchanged
					const dataTransfer = new DataTransfer();
					dataTransfer.items.add(audioFile);
					fileInput.files = dataTransfer.files;

					micStatus.textContent = 'Recording captured. Click "Transcribe Audio" to submit.';
					stream.getTracks().forEach((track) => track.stop());
				};

				mediaRecorder.start();
				isRecording = true;
				micButton.textContent = "⏹ Stop Recording";
				micButton.style.background = "#991b1b";
				micStatus.textContent = "Recording... click again to stop.";
			} catch (err) {
				micStatus.textContent = "Microphone access denied or unavailable: " + err.message;
			}
		} else {
			// Stop recording
			mediaRecorder.stop();
			isRecording = false;
			micButton.textContent = "🎤 Record from Microphone";
			micButton.style.background = "#334155";
		}
	});
}
document.addEventListener("DOMContentLoaded", initAsrMic);



