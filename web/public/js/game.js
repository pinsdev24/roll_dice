(function($) {

	"use strict";

	document.addEventListener('DOMContentLoaded', () => {
		const rollDiceButton = document.getElementById('rollDice');
		const diceImage = document.getElementById('dice');
		const lastRolls = document.getElementById('lastRolls');
	
		rollDiceButton.addEventListener('click', () => {
			rollDice();
		});
	
		function rollDice() {
			let counter = 0;
			const interval = setInterval(() => {
				const randomFace = Math.floor(Math.random() * 6) + 1;
				diceImage.src = `images/dice_faces/dice${randomFace}.png`;
				counter++;
				if (counter >= 10) {
					clearInterval(interval);
					const finalFace = Math.floor(Math.random() * 6) + 1;
					diceImage.src = `images/dice_faces/dice${finalFace}.png`;
					updateLastRolls(finalFace);
				}
			}, 100);
		}
	
		function updateLastRolls(face) {
			const newRoll = document.createElement('a');
			newRoll.className = 'list-group-item list-group-item-action';
			newRoll.textContent = face;
			lastRolls.insertBefore(newRoll, lastRolls.firstChild);
			if (lastRolls.children.length > 10) {
				lastRolls.removeChild(lastRolls.lastChild);
			}
		}
	});	

})(jQuery);
