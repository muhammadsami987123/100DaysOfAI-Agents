from agent import JarvisMusicController

def main():
    controller = JarvisMusicController()
    while True:
        command = controller.listen_for_command()
        controller.process_command(command)

if __name__ == "__main__":
    main()
