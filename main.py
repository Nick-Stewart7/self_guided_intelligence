import time
import threading
import queue
from cognitive_substrate import Substrate

class IdleSystem:
    def __init__(self, idle_timeout=30):
        self.idle_timeout = idle_timeout  # seconds before considered idle
        self.last_activity_time = time.time()
        self.running = True
        self.state = 'active'
        self.input_queue = queue.Queue()
        
    def background_monitor(self):
        """Thread function that monitors for idle state and does background work"""
        while self.running:
            current_time = time.time()
            time_since_activity = current_time - self.last_activity_time
            
            # Check if we've been idle long enough
            if time_since_activity >= self.idle_timeout and self.state != 'idle':
                self.state = 'idle'
                print("\033[0;33m" + "\nSystem idle - Starting background pondering..." + "\033[0m")
                
                # Do background processing
                substrate = Substrate()
                result = substrate.self_guide()
                
                print("\033[0;35m" + f"\nBackground pondering result:\n{result}" + "\033[0m")
                print("\033[1;37m" + "\nWaiting for user input" + "\033[0m")
            
            # Don't hog the CPU
            time.sleep(1000)
    
    def input_reader(self):
        """Thread function that reads user input"""
        while self.running:
            try:
                # Using a short timeout allows checking if we should exit
                user_input = input("\033[1;37m" + "\nWaiting for user input\n" + "\033[0m")
                self.input_queue.put(user_input)
                self.last_activity_time = time.time()  # Update activity time
                self.state = 'active'  # Reset state to active
            except EOFError:
                # Handle EOF (Ctrl+D on Unix, Ctrl+Z on Windows)
                self.running = False
    
    def start(self):
        """Start the system with monitoring and input threads"""
        # Start background monitor thread
        monitor_thread = threading.Thread(target=self.background_monitor)
        monitor_thread.daemon = True  # Thread will exit when main program exits
        monitor_thread.start()
        
        # Start input reader in a separate thread
        input_thread = threading.Thread(target=self.input_reader)
        input_thread.daemon = True
        input_thread.start()
        
        substrate = Substrate()
        
        # Main loop that processes input
        while self.running:
            try:
                # Wait for input with timeout so we can check if we should exit
                user_input = self.input_queue.get(timeout=0.5)
                
                if user_input.lower() == "exit":
                    self.running = False
                    print("Exiting system...")
                    break
                elif user_input == "":
                    response = substrate.self_guide()
                    print("\033[0;35m" + f"Final Answer:\n{response}" + "\033[0m")
                else:
                    response = substrate.process_input(user_input)
                    print("\033[0;35m" + f"Final Answer:\n{response}" + "\033[0m")
                    
            except queue.Empty:
                # No input received within timeout, continue loop
                pass
            except KeyboardInterrupt:
                # Handle Ctrl+C
                self.running = False
                print("Interrupted. Exiting system...")
                break

if __name__ == "__main__":
    system = IdleSystem(idle_timeout=1000)  # Set to 10 seconds for testing, adjust as needed
    system.start()