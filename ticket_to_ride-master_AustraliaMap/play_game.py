#!/usr/bin/python
import time
from ai.cf_ai.cf_adversarial_ai import AdversarialAI
from ai.random_ai import RandomAI
from ai.cf_ai.cf_random_ai import CFRandomAI
from ai.cf_ai.cf_base_ai import CFBaseAI
from ai.cf_ai.cf_action_eval_ai import CFActionEvalAI
from ai.cf_ai.cf_combined_ai import CFCombinedAI
from drivers.driver import Driver
from drivers.log_driver import LogDriver
from game import Game
from game.classes import FailureCause, Colors
from human_player.console_player import ConsolePlayer
from human_player.TIcketToRideGUI import AppGUI

# GUI imports
import tkinter as tk
from tkinter import ttk
from threading import Thread, Event  # Import Event for synchronization

# You can choose the player you want by changing these lines with other constructors
## p1 = CFActionEvalAI("CFAE")
# p2 = CFCombinedAI("CF Combined")
p1 = CFBaseAI("CF Base AI")
# For example
## p2 = CFBaseAI("CF Base AI")
# p2 = RandomAI("R2")
# p2 = AdversarialAI("Adversarial AI")
# p2 = RandomAI("random AI")

## You can use Console Player to play with AI, be sure to enable GUI
p2 = ConsolePlayer("Human")
## p3 = RandomAI("R3")
## p4 = AdversarialAI("Adversarial AI")
## p5 = RandomAI("R2")
## p6 = RandomAI("R1")

players = [p1, p2]
use_gui = True
iterations = 2

def run_gui(player, greeting_done_event):
    root = tk.Tk()
    app_gui = AppGUI(root)
    player.set_gui(app_gui)
    #print(f"GUI is set for player: {player.gui}")  # Debug print to confirm GUI is set

    def on_greeting_done():
        greeting_done_event.set()
        root.quit()  # Close the GUI event loop

    app_gui.greeting_screen(on_greeting_done)

    root.mainloop()

def main():
    if use_gui:
        greeting_done_event = Event()

        # Run the GUI setup in the main thread
        run_gui(p2, greeting_done_event)

        # Wait for the greeting to be done
        greeting_done_event.wait()

    # Continue running the other code in the main thread
    driver = LogDriver(use_gui=use_gui, players=players, print_debug=False, iterations=iterations, switch_order=True,
                       replay_deck=True, replay_destinations=True)
    driver.run_game()

if __name__ == "__main__":
    main()
