from cognitive_substrate import Substrate

if __name__ == "__main__":
    substrate = Substrate()
    while(True):
        user_input = input("\033[1;37m" + "\nWaiting for user input\n")
        if user_input == "exit":
            exit()
        elif user_input == "":
            response = substrate.self_guide()
            print(f"\033[0;35m Final Answer:\n{response}")
        else:
            response = substrate.process_input(user_input)
            print(f"\033[0;35m Final Answer:\n{response}")