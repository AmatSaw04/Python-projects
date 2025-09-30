import pyautogui
import time
import sys


def main():
    """
    Automates the Chrome Dinosaur game by detecting obstacles and game-over states.
    """
    print("Starting the Dino Bot...")
    print("Press Ctrl+C to stop the bot at any time.")

    # --- 1. SETUP ---
    try:
        # Find the game window and activate it.
        window = pyautogui.getWindowsWithTitle("Chrome Dinosaur Game")[0]
        window.activate()
        time.sleep(1)  # Give the window a moment to come into focus
    except IndexError:
        print("ERROR: Game window not found. Please open the game in your browser.")
        sys.exit()

    # Locate the dinosaur image on the screen to establish our coordinates.
    try:
        dino_location = pyautogui.locateOnScreen('./images/dinosaur.png', confidence=0.7)
    except pyautogui.ImageNotFoundException:
        print("ERROR: Could not find 'dinosaur.png'. Make sure it's in an 'images' subfolder.")
        sys.exit()

    if dino_location is None:
        print("ERROR: Dinosaur not found on the screen. Is the game visible?")
        sys.exit()

    print(f"Dinosaur found at: {dino_location}")

    # --- 2. DYNAMICALLY DEFINE REGIONS ---
    # Define the obstacle detection zone relative to the dinosaur's position.
    # This zone is a rectangle in front of and slightly above the dinosaur.
    obstacle_region = (
        dino_location.left + dino_location.width,
        dino_location.top - 20,  # Look slightly higher for birds
        150,  # How far ahead to look
        dino_location.height + 20
    )

    # Define the game over region relative to the window's center.
    game_over_region = (
        window.left + window.width // 2 - 100,
        window.top + window.height // 2 - 50,
        200,
        100
    )

    # Define the background color of the game area.
    # You might need to adjust this if your screen has a different color profile.
    BACKGROUND_COLOR = (247, 247, 247)

    # --- 3. START GAME AND RUN MAIN LOOP ---
    pyautogui.press('space')
    time.sleep(0.5)

    try:
        while True:
            # --- Obstacle Detection ---
            # Take a screenshot of the area in front of the dinosaur.
            obstacle_screenshot = pyautogui.screenshot(region=obstacle_region)

            # Check every few pixels for any color that is not the background.
            for x in range(0, obstacle_screenshot.width, 5):
                for y in range(0, obstacle_screenshot.height, 5):
                    pixel_color = obstacle_screenshot.getpixel((x, y))
                    if pixel_color != BACKGROUND_COLOR:
                        pyautogui.press('up')  # Jump!
                        print("Obstacle detected! Jumping...")
                        time.sleep(0.3)  # Brief pause to avoid multiple detections of the same obstacle
                        break  # Exit the pixel-checking loops
                else:
                    continue
                break

            # --- Game Over Detection ---
            # Check if the "Game Over" image has appeared.
            try:
                if pyautogui.locateOnScreen('./images/game_over.png', region=game_over_region, confidence=0.8):
                    print("Game Over detected. Stopping bot.")
                    break  # Exit the main while loop
            except pyautogui.ImageNotFoundException:
                pass  # Game is still running, do nothing.

    except KeyboardInterrupt:
        print("\nBot stopped by user.")


if __name__ == "__main__":
    main()