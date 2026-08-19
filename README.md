# T9-Keyboard
T9 Keyboard. Mechanical KeySwitches, uses Circuit Python. 3D printed case and keycaps. SEEEDUINO XIAO RP2040. 9 keys. I made this because I wanted to make a normal keyboard but the microcontroller didn't have enough pins so I decided on this one. I also wanted to try handwiring.

# Wiring:
Here is the wiring diagram.
<br></br>
<img width="605" height="935" alt="Screenshot 2026-08-19 at 4 32 02 PM" src="https://github.com/user-attachments/assets/4d339f36-9a0c-4d1c-b97f-e84a1bed8820" />
<br></br>
Basically, each switch has one pin gonnected to ground and the other pin connected to any GPIO pin on the SEEEDUINO XIAO. It doesn't matter which one, you can change it very easily in the code by just updating one number:
<br></br>
<img width="551" height="202" alt="Screenshot 2026-08-19 at 4 31 31 PM" src="https://github.com/user-attachments/assets/865b9db8-03c6-463a-989e-56894ec479e2" />
<br></br>
You need to change board.D0 to board.("whichever pin").
<br></br>
The pins start at the top left at D0 and go down to the bottom left at D6, then bottom right is D7 and it goes up until D10 (11 total GPIO pins)
<br></br>
<img width="1055" height="540" alt="Screenshot 2026-08-19 at 4 34 05 PM" src="https://github.com/user-attachments/assets/629d3e25-b1e8-4825-b825-2815094a8782" />
<br></br>

# Soldering:
To solder it all, I recommend using jumper wires.
<br></br>
I cut them up into the correct length and then stripped the ends to expose the copper underneath, which I then soldered.
<br></br>
The benefit of this technique is that the wires won't unintentially come into contact and short no matter how tangled they are because they are encased in teh silicone.
<br></br>
Here is an example:
<br></br>
<img width="413" height="629" alt="Screenshot 2026-08-18 at 5 07 40 PM" src="https://github.com/user-attachments/assets/a4c00895-cd80-4a90-9c23-5ebe957e57eb" />
<img width="1204" height="923" alt="Screenshot 2026-08-18 at 5 12 09 PM" src="https://github.com/user-attachments/assets/03d5103b-7a46-4c5d-9691-a7916452fed0" />
<img width="629" height="850" alt="Screenshot 2026-08-18 at 5 07 36 PM" src="https://github.com/user-attachments/assets/e9246af3-77b0-4833-9813-e6d57cbebd38" />

# Images:
<img width="517" height="374" alt="Screenshot 2026-08-18 at 6 35 13 PM" src="https://github.com/user-attachments/assets/5b3fb1f6-516c-46ab-9931-37e62b657b90" />
<img width="1276" height="917" alt="Screenshot 2026-08-19 at 4 23 03 PM" src="https://github.com/user-attachments/assets/194b1b22-f685-4fe6-b1dc-1b7509891cad" />
