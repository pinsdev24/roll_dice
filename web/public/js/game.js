(function($) {

	"use strict";

	document.addEventListener('DOMContentLoaded', () => {
		const rollDiceButton = document.getElementById('rollDice');
		const endSessionButton = document.getElementById('end-session');
		const setConfigButton = document.getElementById('set-setting');
		const diceImage = document.getElementById('dice');
		const lastRolls = document.getElementById('lastRolls');
		const liveToastBtn = document.getElementById('liveToastBtn');
		let basicInstance = mdb.Alert.getInstance(document.getElementById('alert-danger'));
		console.log(basicInstance)
	
		rollDiceButton.addEventListener('click', () => {
			rollDice();
		});

		endSessionButton.addEventListener('click', async() => {
			let response =  await endSession();
			console.log(response)
		});

		document.getElementById('danger').addEventListener('click', () => {
			basicInstance.show();
		});
	
		function rollDice() {
			let counter = 0;
			const start_at = new Date()
			const interval = setInterval(() => {
				const randomFace = Math.floor(Math.random() * 6) + 1;
				diceImage.src = `images/dice_faces/dice${randomFace}.png`;
				counter++;
				if (counter >= 10) {
					clearInterval(interval);
					const finalFace = Math.floor(Math.random() * 6) + 1;
					diceImage.src = `images/dice_faces/dice${finalFace}.png`;
					const end_at = new Date();
					updateLastRolls(finalFace);
					saveGame({start: start_at.toISOString(), end: end_at.toISOString(), score: finalFace});
				}
			}, 100);
		}
	
		function updateLastRolls(face) {
			const newRoll = document.createElement('a');
			newRoll.className = 'list-group-item list-group-item-action';
			newRoll.textContent = face;
			lastRolls.insertBefore(newRoll, lastRolls.lastChild);
			if (lastRolls.children.length > 10) {
				lastRolls.removeChild(lastRolls.lastChild);
			}
		}

		async function saveGame(data) {
			try {
				const url = 'http://localhost:3000/roll-dice';
				
		
				const response = await fetch(url, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(data)
				});

				console.log(response);
		
				if (response.ok) {
					const result = await response.json();
					console.log('Success:', result);
				} else {
					console.error('Error:', response.status, response.statusText);
				}
			} catch (error) {
				console.error('Network error:', error);
			}
		}

		async function endSession() {
			try {
				const url = 'http://localhost:3000/end-session';
				
		
				const response = await fetch(url, {
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json'
					},
				});

				console.log(response);
		
				if (response.ok) {
					const result = await response.json();
					console.log('Success:', result);
				} else {
					console.error('Error:', response.status, response.statusText);
				}
			} catch (error) {
				console.error('Network error:', error);
			}
		}
		
	});

})(jQuery);
