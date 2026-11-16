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

// Handles form submission via AJAX (fetch) so the page doesn't fully reload
function initAsrFormSubmit() {
	const form = document.getElementById("asrForm");
	if (!form) return; // Guard in case this script loads on a page without the ASR form

	form.addEventListener("submit", async function (e) {
		e.preventDefault();

		const submitBtn = form.querySelector('button[type="submit"]');
		const originalBtnText = submitBtn.textContent;
		submitBtn.disabled = true;
		submitBtn.textContent = "Transcribing...";

		// Remove any previous result/error block before showing a new one
		const existingResult = document.getElementById("asrResultBlock");
		if (existingResult) existingResult.remove();

		try {
			const formData = new FormData(form);
			const response = await fetch(window.location.href, {
				method: "POST",
				headers: { "X-Requested-With": "XMLHttpRequest" },
				body: formData,
			});

			const data = await response.json();
			const resultDiv = document.createElement("div");
			resultDiv.id = "asrResultBlock";

			if (data.error) {
				resultDiv.style.cssText =
					"margin-top: 25px; padding: 15px; background: #fef2f2; border-left: 4px solid #dc2626; border-radius: 4px;";
				resultDiv.innerHTML =
					'<strong style="color: #991b1b;">Error:</strong><p style="margin-top: 5px; color: #334155;">' +
					data.error +
					"</p>";
			} else if (data.transcript) {
				resultDiv.style.cssText =
					"margin-top: 25px; padding: 15px; background: #f1f5f9; border-left: 4px solid #991b1b; border-radius: 4px;";
				resultDiv.innerHTML =
					"<strong>Transcription (" +
					data.selected_language +
					'):</strong><p style="margin-top: 8px; color: #334155; font-size: 1.05rem;">' +
					data.transcript +
					"</p>";
			}

			form.insertAdjacentElement("afterend", resultDiv);
		} catch (err) {
			const resultDiv = document.createElement("div");
			resultDiv.id = "asrResultBlock";
			resultDiv.style.cssText =
				"margin-top: 25px; padding: 15px; background: #fef2f2; border-left: 4px solid #dc2626; border-radius: 4px;";
			resultDiv.innerHTML =
				'<strong style="color: #991b1b;">Error:</strong><p style="margin-top: 5px; color: #334155;">Request failed: ' +
				err.message +
				"</p>";
			form.insertAdjacentElement("afterend", resultDiv);
		} finally {
			submitBtn.disabled = false;
			submitBtn.textContent = originalBtnText;
		}
	});
}
document.addEventListener("DOMContentLoaded", initAsrFormSubmit);